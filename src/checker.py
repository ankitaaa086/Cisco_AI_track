
import re

class NetworkRuleChecker:
    def __init__(self, device_output: str):
        self.output = device_output.lower()

    def check_interfaces_down(self) -> list:
        """Detects if any interface is administratively down."""
        faults = []
        pattern = r"(\w+\d/\d+)\s+is administratively down"
        matches = re.findall(pattern, self.output)
        for match in matches:
            faults.append(f"Interface {match} is down.")
        return faults

    def check_subnet_mismatch(self, expected_subnet: str) -> bool:
        """Checks for wrong subnet masks."""
        return expected_subnet not in self.output

    def run_all_checks(self) -> dict:
        """Executes all deterministic checks returning a summary."""
        return {
            "interface_faults": self.check_interfaces_down(),
            "has_basic_errors": len(self.check_interfaces_down()) > 0
        }