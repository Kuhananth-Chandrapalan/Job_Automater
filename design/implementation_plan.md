# Phase-Wise Implementation Plan

## Phase 1: Skeleton & Data Layer (Days 1-2)
**Goal**: Get manual data flowing into a structured database.
1. **Google Sheets**: Create `Job_Application_Master` with defined schema (data validation enabled).
2. **Gmail/Drive**:
   - Create label `JobBot`.
   - Create Drive folder `Job_Automation/Resumes`.
3. **n8n Workflow 1 (Ingest)**:
   - Connect Gmail API.
   - Build parsing logic for 1-2 key sources (e.g., LinkedIn Alerts via email).
   - Verify deduplication logic (`job_id` hash).

## Phase 2: Intelligence Engine (Days 3-5)
**Goal**: Accurately score and prioritize jobs.
1. **Classifier**: Build `Workflow 2`. Test LLM prompts for Domain/Level detection.
2. **ATS Scorer**: 
   - Deploy `ats_scorer.py` as a local n8n-accessible service or convert logic to n8n JavaScript node.
   - Tune thresholds (run on 20 past jobs to verify 0.85 benchmark).
3. **Integration**: Connect Ingest -> Priority -> Score -> Sheet update loop.

## Phase 3: Content Generation (Days 6-8)
**Goal**: Generate high-quality, truthful resumes.
1. **Templates**: Create clean, ATS-parsed Google Doc templates.
2. **Prompt Engineering**: Refine "Truthful Tailoring" prompts (Workflow 4). Test for hallucinations.
3. **Pipeline**: Connect Sheet -> LLM -> Google Doc -> PDF Export.

## Phase 4: Execution & Monitoring (Days 9-10)
**Goal**: Close the loop by sending applications.
1. **Email Dispatch**: Build `Workflow 5`. Implement rate limiting (e.g., 2 emails/hour).
2. **Reply Monitor**: Build `Workflow 6`. Test against historical emails to verify classifier accuracy.
3. **Safety**: Add "Dry Run" mode where emails are drafted but not sent.

## Phase 5: Reliability & Optimization (Days 11+)
**Goal**: Set and forget.
1. **Error Handling**: Implement `Workflow 7` (Logging).
2. **Dashboards**: Build meaningful views in Google Sheets (e.g., "Funnel View").
3. **Backfill**: Import past month's job alerts to populate initial data.

---

## Critical Checkpoints
- **End of Phase 2**: Verify "Mid > Junior" priority logic is working.
- **End of Phase 3**: manual audit of 5 tailored resumes.
- **End of Phase 4**: Confirm "Dry Run" drafts look perfect before enabling auto-send.
