# NetSage AI — Responsible AI Audit Log

## Purpose
This log records human review of AI-generated network troubleshooting
diagnoses.

Required decisions:
- Accepted
- Edited
- Rejected

For Edited or Rejected cases, record the corrected root cause and why the AI
answer needed correction.

## Five Review Candidates

These are **not fabricated completed reviews**. They are five actual cases
from the supplied dataset that should be reviewed by the team:

| Case | Expected fault | Status |
|---|---|---|
| NET-004 | OSPF Hello Timer Mismatch | Pending actual human review |
| NET-005 | Extended ACL blocking HTTP traffic | Pending actual human review |
| NET-017 | NAT interface direction missing on internal interface | Pending actual human review |
| NET-025 | Uplink trunk port not configured as DAI trusted | Pending actual human review |
| NET-029 | IPv6 Router Advertisements (RA) suppressed | Pending actual human review |

## Completion Procedure

1. Generate the AI diagnosis.
2. Independently inspect the supplied evidence.
3. Select Accepted, Edited, or Rejected.
4. For Edited/Rejected, enter the corrected diagnosis and reason.
5. Record reviewer name and timestamp.

The project requirement asks for at least five cases where AI needed human
correction. Only mark such cases as completed after the team actually performs
the reviews.
