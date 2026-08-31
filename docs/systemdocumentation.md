# NetSage AI — System Documentation

## 1. Overview
NetSage AI is an AI-assisted Cisco/Packet Tracer troubleshooting helper. It combines structured case evidence, a deterministic rule engine, an AI prompt layer, and mandatory human review.

## 2. Architecture

```text
Packet Tracer / Lab Case
        |
        v
   cases.csv
        |
        +----------------------+
        |                      |
        v                      v
Deterministic Checker      AI Prompt Layer
        |                      |
        +----------+-----------+
                   |
                   v
          Structured Diagnosis
                   |
                   v
             Human Review
          Accepted / Edited / Rejected
                   |
                   v
             Audit Log
                   |
                   v
               Dashboard