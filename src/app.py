
import streamlit as st
import pandas as pd
import os
import datetime
from checker import NetworkRuleChecker
from engine import DiagnosticEngine

# --- Page Configuration ---
st.set_page_config(
    page_title="NetSage AI - Troubleshooter",
    page_icon="🌐",
    layout="wide"
)

# --- Path Configurations ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
CASES_FILE = os.path.join(DATA_DIR, "cases.csv")
REVIEW_LOG_FILE = os.path.join(LOGS_DIR, "audit_log.csv")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Helper function to initialize seed dataset if missing
def load_or_init_cases():
    if not os.path.exists(CASES_FILE):
        demo_cases = pd.DataFrame([
            {
                "case_id": "NET-001",
                "symptom": "PC gets IP but cannot reach server in VLAN 30",
                "topology": "Router-on-a-Stick with Switch Core",
                "show_output": "FastEthernet0/1 is up. Trunk allowed VLANs: 10, 20",
                "expected_fault": "Missing VLAN 30 on trunk link",
                "layer": "Layer 2",
                "concept": "VLAN/Trunking",
                "severity": "High"
            },
            {
                "case_id": "NET-002",
                "symptom": "Branch router cannot reach Internet subnet",
                "topology": "Edge Router connected to ISP Gateway",
                "show_output": "Gateway of last resort is not set. Codes: C - connected, S - static",
                "expected_fault": "Missing default route",
                "layer": "Layer 3",
                "concept": "Routing",
                "severity": "Critical"
            },
            {
                "case_id": "NET-003",
                "symptom": "Server farm interface is unreachable",
                "topology": "Distribution switch to Server Farm",
                "show_output": "GigabitEthernet0/2 is administratively down, line protocol is down",
                "expected_fault": "Interface is shut down",
                "layer": "Layer 1",
                "concept": "Interface State",
                "severity": "Medium"
            }
        ])
        demo_cases.to_csv(CASES_FILE, index=False)
        return demo_cases
    return pd.read_csv(CASES_FILE)

def load_reviews():
    if not os.path.exists(REVIEW_LOG_FILE):
        df = pd.DataFrame(columns=["timestamp", "case_id", "decision", "human_corrected_root_cause", "reviewer_notes"])
        df.to_csv(REVIEW_LOG_FILE, index=False)
        return df
    return pd.read_csv(REVIEW_LOG_FILE)

def save_review(case_id, decision, corrected_cause, notes):
    df = load_reviews()
    new_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "case_id": case_id,
        "decision": decision,
        "human_corrected_root_cause": corrected_cause,
        "reviewer_notes": notes
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(REVIEW_LOG_FILE, index=False)

# --- Application Layout ---
st.title("🌐 NetSage AI: Network Troubleshooting Assistant")
st.caption("Packet Tracer Diagnostic Engine with Mandatory Human-in-the-Loop Review")

cases_df = load_or_init_cases()
reviews_df = load_reviews()

# --- Top Dashboard Metrics ---
col1, col2, col3, col4 = st.columns(4)

total_cases = len(cases_df)
total_reviews = len(reviews_df)
accepted_count = len(reviews_df[reviews_df["decision"] == "Accepted"]) if total_reviews > 0 else 0
agreement_rate = (accepted_count / total_reviews * 100) if total_reviews > 0 else 0.0

col1.metric("Total Cases Loaded", total_cases)
col2.metric("Reviews Completed", total_reviews)
col3.metric("Accepted Diagnoses", accepted_count)
col4.metric("AI-Human Agreement", f"{agreement_rate:.1f}%")

st.divider()

# --- Tabs ---
tab_diag, tab_analytics, tab_responsible_ai = st.tabs([
    "🔍 AI Diagnosis & Human Review", 
    "📊 Issue & Severity Analytics", 
    "🛡️ Responsible AI Log (Human Corrections)"
])

# ==================== TAB 1: DIAGNOSIS & REVIEW ====================
with tab_diag:
    selected_case_id = st.selectbox("Select Case to Troubleshoot:", cases_df["case_id"].tolist())
    case_row = cases_df[cases_df["case_id"] == selected_case_id].iloc[0]

    c_left, c_right = st.columns([1, 1])

    with c_left:
        st.subheader("📋 Case Details")
        st.markdown(f"**Symptom:** {case_row['symptom']}")
        st.markdown(f"**Topology:** `{case_row['topology']}`")
        st.markdown(f"**Concept Tag:** `{case_row['concept']}` | **Severity:** `{case_row['severity']}`")
        st.text_area("Show Command Output", case_row["show_output"], height=160, disabled=True)

        # Deterministic Rules
        checker = NetworkRuleChecker(case_row["show_output"])
        rule_results = checker.evaluate_rules()
        if rule_results["has_rule_violations"]:
            st.error(f"⚠️ **Deterministic Rule Checker Found Faults:**")
            for violation in rule_results["violations"]:
                st.write(f"- {violation}")
        else:
            st.success("✅ Deterministic Rule Checker: No basic syntax/port errors found.")

    with c_right:
        st.subheader("🤖 AI Diagnostic Recommendation")
        engine = DiagnosticEngine()
        
        if st.button("Generate AI Diagnosis", type="primary"):
            diagnosis = engine.run_diagnosis(case_row["symptom"], case_row["topology"], case_row["show_output"])
            st.session_state[f"diag_{selected_case_id}"] = diagnosis

        diagnosis = st.session_state.get(f"diag_{selected_case_id}", None)

        if diagnosis:
            st.info(f"**Root Cause:** {diagnosis.get('root_cause')}")
            st.write(f"**OSI Layer:** `{diagnosis.get('layer')}` | **Confidence:** `{diagnosis.get('confidence')}`")
            st.write(f"**Evidence:** {diagnosis.get('evidence')}")
            st.write(f"**Next Verification:** `{diagnosis.get('next_command')}`")
            st.code(diagnosis.get('fix_steps'), language="bash")

            st.divider()
            st.subheader("👤 Human Review Decision")
            with st.form(f"review_form_{selected_case_id}"):
                decision = st.radio("Decision:", ["Accepted", "Edited", "Rejected"], horizontal=True)
                corrected_root_cause = st.text_input("Corrected Root Cause (if edited/rejected):", value=diagnosis.get('root_cause') if decision == "Accepted" else "")
                review_notes = st.text_area("Reviewer Audit Notes / Justification:")
                
                submitted = st.form_submit_button("Submit Human Review")
                if submitted:
                    save_review(selected_case_id, decision, corrected_root_cause, review_notes)
                    st.success(f"Audit log updated for {selected_case_id} with decision '{decision}'!")
                    st.rerun()

# ==================== TAB 2: ANALYTICS ====================
with tab_analytics:
    st.subheader("📈 Case Distributions & Performance")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("##### Issue Themes (Concepts)")
        theme_counts = cases_df["concept"].value_counts()
        st.bar_chart(theme_counts)

    with col_chart2:
        st.markdown("##### Severity Breakdown")
        sev_counts = cases_df["severity"].value_counts()
        st.bar_chart(sev_counts)

    if not reviews_df.empty:
        st.markdown("##### Review Decision Breakdown")
        decision_counts = reviews_df["decision"].value_counts()
        st.bar_chart(decision_counts)

# ==================== TAB 3: RESPONSIBLE AI LOG ====================
with tab_responsible_ai:
    st.subheader("🛡️ Responsible AI Log (Human Corrections & Overrides)")
    st.caption("Documents cases where the AI diagnosis was edited or rejected by a human reviewer.")

    if not reviews_df.empty:
        corrections_df = reviews_df[reviews_df["decision"].isin(["Edited", "Rejected"])]
        if not corrections_df.empty:
            st.dataframe(corrections_df, use_container_width=True)
        else:
            st.info("No AI corrections logged yet. Complete reviews where the AI output requires correction.")
    else:
        st.info("No audit logs available.")