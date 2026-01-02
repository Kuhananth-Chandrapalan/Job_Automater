# n8n Workflow Designs

This system is divided into 7 independent, modular workflows.

---

## 1. Job Ingestion Workflow
**Trigger**: Gmail Trigger (Subject: "Job Alert") AND Cron (RSS Polling - Every 1hr)
1. **Fetch Data**: 
   - Gmail: Extract body HTML.
   - RSS: Extract feed items.
2. **Normalize**: Function Item node to map different sources to standard JSON object.
3. **Hash ID**: Crypto node -> SHA256 of `job_url`.
4. **Deduplicate**: 
   - Google Sheets Lookup node (Input: `job_id`).
   - If found: **Stop**.
   - If not found: **Proceed**.
5. **Write to Sheet**: Append row with `status` = `New`.

## 2. Job Classification & Priority Workflow
**Trigger**: Cron (Every 15 mins) -> Filter Sheet `status` = `New`
1. **Batch Read**: Get 10 rows.
2. **LLM Analysis** (Gemini/OpenAI):
   - Input: Title, Description.
   - Prompt: "Classify Domain (DS/Biz/SE), Level (Intern/Assoc/Jr/Mid), and extract Location."
3. **Calculate Priority**:
   - Function Node:
     ```js
     if (level == 'Mid') score = 5;
     else if (level == 'Junior') score = 4;
     else if (level == 'Associate') score = 3;
     else score = 1; // Intern
     ```
4. **Update Sheet**: Write columns `domain`, `level`, `priority_score`, `location`.

## 3. ATS Scoring Workflow
**Trigger**: Cron (Every 30 mins) -> Filter Sheet `status` = `New` (after classification runs)
*Ideally runs after classification to pick the right base resume.*
1. **Select Base Resume**: Switch Node based on `domain`.
   - DS -> Read `DS_Master.txt`
   - SE -> Read `SE_Master.txt`
2. **Score**: HTTP Request -> Local Python Service (or internal n8n Function).
   - Logic: Keyword Match (40%) + Experience (20%) + Title (20%).
3. **Decision Logic**:
   - Score >= 0.85: `status` = `Ready` (skip tailoring if apply method allows, else `Tailoring`)
   - Score 0.70-0.84: `status` = `Tailoring`
   - Score < 0.70: `status` = `Skipped`
4. **Update Sheet**: Write `ats_score`, `status`, `app_notes` (missing keywords).

## 4. Resume Tailoring Workflow
**Trigger**: Cron (Hourly) -> Filter Sheet `status` = `Tailoring`
1. **Get Job Data**: Title, Description, Missing Keywords.
2. **User Check**: (Optional) Send Slack snippet for approval if Priority < 3.
3. **LLM Tailor**:
   - Prompt: "Rewrite these bullet points using TRUTHFUL experience to match these keywords: [list]."
4. **Generate Document**: 
   - Google Docs Node -> Copy Template -> Replace Variables.
   - OR Python Script -> Edit DOCX.
5. **Export PDF**: Drive Node -> Export as PDF.
6. **Update Sheet**: 
   - `resume_link` = Drive URL.
   - `status` = `Ready(Email)` or `Ready(Portal)`.

## 5. Application Execution Workflow
**Trigger**: Cron (Hourly) -> Filter `status` LIKE `Ready%`
1. **Split Path**:
   - **Path A (Email)**:
     1. Generate Cover Letter (LLM).
     2. Gmail Node -> Send Email with PDF attachment.
     3. Update Sheet: `status` = `Applied`, `applied_date` = Now, `thread_id` = ID.
   - **Path B (Portal)**:
     1. Slack/Email Node -> "Ready to Apply: [Link]".
     2. Update Sheet: `status` = `User_Notified`.

## 6. Email Reply Monitoring Workflow
**Trigger**: Gmail Trigger (New Email)
1. **Filter**: Check existing `thread_id` in Sheet OR match Sender Domain.
2. **Classify**: LLM Node -> "Is this an Interview, Rejection, or Auto-Reply?"
3. **Update Sheet**:
   - If Interview: `response_status` = `Interview`. Send Alert!
   - If Rejection: `response_status` = `Rejected`.
4. **Move Email**: Gmail Node -> Apply Label `JobBot/Replies`.

## 7. Error Handling & Retry Workflow
**Trigger**: Called on Error Node (n8n Error Trigger)
1. **Log**: Append to `System_Logs` sheet.
2. **Analysis**: 
   - If `RateLimit`: Wait & Retry (handled by node settings).
   - If `AuthError`: Alert User immediately.
3. **Alert**: Send summary of failures to User via Email/Slack.
