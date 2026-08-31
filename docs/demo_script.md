# NetSage AI — 5–10 Minute Demo Script

## 0:00–0:45 — Introduction
"NetSage AI is an AI-assisted troubleshooting helper for Cisco/Packet Tracer lab problems. It reads symptoms and show-command evidence, identifies likely causes and next steps, and keeps a human reviewer in the loop."[cite: 5]

## 0:45–1:30 — Dataset
Open `data/cases.csv`[cite: 5].
Explain that the dataset contains 30 structured troubleshooting cases covering multiple fault types such as VLAN, DHCP, DNS, routing, ACL, NAT and wireless[cite: 5].

## 1:30–2:15 — Architecture
Show:
- cases.csv
- diagnose_prompt.md
- rule checker
- diagnostic engine
- dashboard
- human review log[cite: 5]

Explain that deterministic checks provide predictable validation while the prompt layer provides the AI diagnosis contract[cite: 5].

## 2:15–4:00 — Live Broken Case
Open Packet Tracer and select a broken case[cite: 5].
Show the symptom and the relevant command output[cite: 5].

Example:
NET-001 — a PC cannot reach a server and the router sub-interface is administratively down[cite: 5].

Run the diagnosis and show:
- root cause
- evidence
- OSI layer
- confidence
- next command
- fix steps[cite: 5]

## 4:00–5:30 — Human Review
Show the diagnosis in the dashboard[cite: 5].
Select Accepted, Edited, or Rejected[cite: 5].
Explain why the reviewer is required to approve the recommendation[cite: 5].

## 5:30–7:00 — Fix and Verification
Apply the correct configuration in Packet Tracer only after review[cite: 5].
Run verification commands and demonstrate that connectivity is restored[cite: 5].

## 7:00–8:00 — Dashboard
Show issue types, severity and deterministic evaluation metrics[cite: 5].

## 8:00–9:00 — Responsible AI
Open the audit log[cite: 5].
Explain an example where the human reviewer corrected or edited the AI diagnosis[cite: 5].

## 9:00–10:00 — Conclusion
Summarize:
- 30 troubleshooting cases
- evidence-backed diagnosis
- deterministic validation
- human review
- auditable troubleshooting workflow[cite: 5]