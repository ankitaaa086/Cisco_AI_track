
import sys
import csv
from pathlib import Path
import pytest

# Add project root to sys.path so we can import from src
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.checker import NetworkRuleChecker
from src.engine import DiagnosticEngine

@pytest.fixture
def base_dir():
    return Path(__file__).resolve().parent.parent

@pytest.fixture
def engine():
    # Initializing with a mock key to test the heuristic fallback
    return DiagnosticEngine(api_key="mock_key")

def test_cases_dataset_integrity(base_dir):
    """Verify that cases.csv exists and has all required columns[cite: 7]."""
    cases_file = base_dir / "data" / "cases.csv"
    
    # Skip if the user hasn't generated the seed data via app.py yet
    if not cases_file.exists():
        pytest.skip("cases.csv not found. Run app.py first to generate seed data.")

    required_fields = {
        "case_id", "symptom", "topology", "show_output",
        "expected_fault", "layer", "concept", "severity"
    }

    with open(cases_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert set(reader.fieldnames) >= required_fields, f"Missing required fields: {required_fields - set(reader.fieldnames)}"
        rows = list(reader)
        
        for i, row in enumerate(rows, 1):
            assert row["case_id"], f"Row {i} has empty case_id[cite: 7]"
            assert row["symptom"], f"Case {row['case_id']} has empty symptom[cite: 7]"

def test_checker_layer1_admin_down():
    """Verify that the rule checker catches administratively down interfaces."""
    output = "GigabitEthernet0/0.10 is administratively down, line protocol is down"
    checker = NetworkRuleChecker(output)
    results = checker.evaluate_rules()
    
    assert results["has_rule_violations"] is True
    assert results["count"] == 1
    assert any("administratively down" in violation.lower() for violation in results["violations"])

def test_checker_layer2_vlan_trunking():
    """Verify that the rule checker catches missing VLANs on a trunk."""
    output = "FastEthernet0/1 is up. Allowed VLANs: 10, 20"
    checker = NetworkRuleChecker(output)
    
    # Check if VLAN 30 is missing
    is_missing = checker.check_trunk_vlan_mismatch(target_vlan="30")
    assert is_missing is True

def test_checker_layer3_missing_route():
    """Verify that the rule checker detects a missing default gateway."""
    output = "show ip route\nGateway of last resort is not set. Codes: C - connected"
    checker = NetworkRuleChecker(output)
    results = checker.evaluate_rules()
    
    assert results["has_rule_violations"] is True
    assert any("gateway of last resort" in violation.lower() for violation in results["violations"])

def test_engine_schema_compliance(engine):
    """Verify that DiagnosticEngine returns strict JSON schema compliant outputs[cite: 7]."""
    symptom = "PC gets IP but cannot reach server in VLAN 30"
    topology = "Router-on-a-Stick with Switch Core"
    show_output = "FastEthernet0/1 is up. Trunk allowed VLANs: 10, 20"
    
    # Run diagnosis using the heuristic fallback
    diag = engine.run_diagnosis(symptom, topology, show_output)

    # Validate output dictionary schema matches expectations
    assert "root_cause" in diag
    assert "layer" in diag
    assert "confidence" in diag
    assert "evidence" in diag
    assert "next_command" in diag
    assert "fix_steps" in diag
    
    # Validate specific heuristic logic fired for this input
    assert "VLAN" in diag["root_cause"]