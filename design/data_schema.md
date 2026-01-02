# Google Sheets Data Schema
**Sheet Name**: `Job_Application_Master`

## Columns Configuration

| Index | Header Name | Data Type | Description |
|:---:|:---|:---|:---|
| A | `job_id` | String | SHA256 Hash of Job URL (Unique Key) |
| B | `date_found` | Timestamp | ISO 8601 DateTime of ingestion |
| C | `company` | String | Company Name |
| D | `role_title` | String | Normalized Job Title |
| E | `location` | String | City, Remote, or Hybrid |
| F | `domain` | Enum | `Data Science`, `Business`, `Software Engineering` |
| G | `level` | Enum | `Intern`, `Associate`, `Junior`, `Mid`, `Senior` |
| H | `priority_score` | Number | Calculated 1-5 (5 = Highest Config) |
| I | `ats_score` | Number | 0.00 to 1.00 |
| J | `job_url` | URL | Direct link to job post |
| K | `source` | String | e.g., `LinkedIn Alert`, `Careers Page`, `Indeed` |
| L | `status` | Enum | `New`, `Scored`, `Tailoring`, `Ready(Email)`, `Ready(Portal)`, `Applied`, `Skipped` |
| M | `apply_method` | Enum | `Email`, `Portal` |
| N | `contact_email` | String | Extracted email for application |
| O | `app_notes` | Text | LLM reasoning or manual notes |
| P | `resume_link` | URL | GDrive Link to **Tailored** Resume |
| Q | `cover_letter_link`| URL | GDrive Link to Cover Letter |
| R | `applied_date` | Timestamp | When the application was sent |
| S | `response_status` | Enum | `Pending`, `Interview`, `Assessment`, `Rejected`, `Offer` |
| T | `last_contact` | Timestamp | Date of last email interaction |
| U | `thread_id` | String | Gmail Thread ID for conversation tracking |

## Enum Definitions
### Priority Logic (Calculated)
- **Mid-Level** + **Target Domain** = 5 (High)
- **Junior** + **Target Domain** = 4
- **Associate** = 3
- **Intern** = 1 (Low)

### Status Lifecycle
1. `New`: Just ingested.
2. `Scored`: ATS / Classifiers run.
3. `Tailoring`: Generating docs.
4. `Ready(Email)`: Docs ready, waiting for dispatch.
5. `Ready(Portal)`: Docs ready, user notified to apply manually.
6. `Applied`: Email sent.

## 2. System_Logs Sheet
*(For error tracking)*
- `timestamp`
- `workflow_name`
- `error_message`
- `job_id` (optional)
