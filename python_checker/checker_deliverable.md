# NetSage AI — Python Rule Checker Deliverable

## Purpose
This is the deterministic validation layer for the current project. It is
designed around the existing `cases.csv` and the interface expected by the
current `app.py`.

## App Compatibility

The current application uses:

```python
checker = NetworkRuleChecker(case_row["show_output"])
rule_results = checker.evaluate_rules()
```

The supplied checker therefore implements `evaluate_rules()` and also keeps
`run_all_checks()` as a compatibility API.

## Checks

The checker covers evidence patterns for:
- interfaces/SVI down
- DHCP pool exhaustion and relay
- DNS lookup
- OSPF
- ACL
- NAT
- VLAN/trunking
- addressing
- static routing
- wireless/RADIUS
- DAI
- port security
- VTP
- HSRP
- IPv6 RA
- CDP

## Dataset Evaluation

Total cases: 30

Cases with deterministic findings:
30

Deterministic finding coverage:
100.0%

See `checker_evaluation.csv` for the case-by-case output.

## Important

A rule match is a deterministic finding, not proof that an AI diagnosis is
correct. The current `engine.py` still contains a mock JSON response and a
TODO for an actual LLM API call. The final submission should not claim a real
LLM integration unless the team implements and tests one.
