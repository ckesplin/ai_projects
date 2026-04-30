"""
OpenClaw Secrets Audit Test

Verifies that openclaw secrets audit passes — no plaintext secrets,
no unresolved refs, no shadowed refs, no legacy residue.

Run with: PYTHONPATH=. python3 tests/test_openclaw_secrets_audit.py -v
"""

import subprocess
import unittest


class TestOpenClawSecretsAudit(unittest.TestCase):
    """
    OpenClaw built-in secrets audit.
    Runs `openclaw secrets audit --check` to verify secrets are clean.
    """

    def test_audit_passes_with_clean_status(self):
        """openclaw secrets audit should pass with clean status."""
        result = subprocess.run(
            ["openclaw", "secrets", "audit", "--check"],
            capture_output=True,
            text=True,
        )
        
        self.assertEqual(
            result.returncode, 0,
            f"SECRETS_AUDIT_FAILED: exit code {result.returncode}\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )
        
        self.assertIn("plaintext=0", result.stdout)
        self.assertIn("unresolved=0", result.stdout)
        self.assertIn("shadowed=0", result.stdout)
        self.assertIn("legacy=0", result.stdout)

    def test_audit_json_output_is_valid(self):
        """openclaw secrets audit --json should return valid JSON with clean status."""
        result = subprocess.run(
            ["openclaw", "secrets", "audit", "--json"],
            capture_output=True,
            text=True,
        )
        
        self.assertEqual(result.returncode, 0)
        
        import json
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            self.fail(f"Invalid JSON output: {e}\nOutput: {result.stdout}")
        
        self.assertEqual(data.get("status"), "clean")
        self.assertEqual(data.get("summary", {}).get("plaintextCount"), 0)
        self.assertEqual(data.get("summary", {}).get("unresolvedRefCount"), 0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)