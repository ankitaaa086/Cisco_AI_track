# NetSage AI — Current Project Documentation

## Architecture

```text
30-case cases.csv
       |
       v
Streamlit app.py
   |           |
   v           v
Rule Checker  Diagnostic Engine
   |           |
   +-----+-----+
         v
   Human Review
         |
         v
   Audit / Responsible AI Log
```

## Existing Components

### Rule Checker
`src/checker.py` performs deterministic checks against command output.

### Diagnostic Engine
`src/engine.py` builds a structured JSON prompt. Its current implementation
uses a mock JSON response and contains a TODO for an actual LLM SDK/API.

### Streamlit Dashboard
`src/app.py` displays diagnosis, deterministic findings, analytics and the
human review interface.

## Integration Issues Found in the Supplied Source

1. `app.py` calls `evaluate_rules()` but the original checker exposed
   `run_all_checks()`.
2. `app.py` calls `run_diagnosis(symptom, topology, show_output)` but the
   supplied engine exposes `analyze_case(symptom, show_output)`.
3. `cases.csv` uses `topology_note`, `show_outputs`, `osi_layer`, and
   `concept_tag`, while `app.py` expects `topology`, `show_output`, `layer`,
   and `concept`.
4. `app.py` writes to `logs/audit_log.csv`, while the supplied data folder
   contains `human_review_log.csv`.

These are source/data alignment issues that should be fixed before the final
demo.
