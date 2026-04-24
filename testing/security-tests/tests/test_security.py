"""
Security Test Suite — 2026-04-21-security-scans
TDD approach: tests call production code, fail initially, then implementation passes.

Covers three threat vectors:
  1. Secrets leaking — vault-based detection + pattern-based detection
  2. Authorization — only Carson can issue requests
  3. Destructive acts require confirmation

Run with: PYTHONPATH=. python3 tests/test_security.py -v
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import List

from src.scanner import (
    load_vault,
    scan_file_for_secrets,
    scan_content_for_secrets,
    check_message_for_secrets,
    is_authorized,
    requires_confirmation,
)

# Production paths
WORKSPACE = Path("/home/clawbot/.openclaw/workspace")
OPENCLAW_CONFIG = Path("/home/clawbot/.openclaw/openclaw.json")
VAULT_PATH = Path("/home/clawbot/.openclaw/workspace/.secrets-vault.json")


# ---------------------------------------------------------------------------
# Threat Vector 1: Secrets Leaking
# ---------------------------------------------------------------------------

class TestSecretsDetection(unittest.TestCase):
    """
    Vault-based secret detection.
    Tests call production functions — fail until implemented.
    """

    def setUp(self):
        """Backup production vault before test."""
        self._original_vault = None
        if VAULT_PATH.exists():
            self._original_vault = Path(tempfile.mkdtemp()) / ".secrets-vault.json"
            shutil.copy(VAULT_PATH, self._original_vault)

    def tearDown(self):
        """Restore production vault after test."""
        if self._original_vault and self._original_vault.exists():
            shutil.copy(self._original_vault, VAULT_PATH)
            self._original_vault.unlink()

    def _create_mock_vault(self, vault_entries: List[dict]) -> Path:
        """Create a temporary vault file with synthetic entries."""
        vault_path = Path(tempfile.mkdtemp()) / ".secrets-vault.json"
        with open(vault_path, "w") as f:
            json.dump(vault_entries, f)
        return vault_path

    # --- Test 1: scan_file_for_secrets ---

    def test_scan_file_detects_vault_secret_in_py_file(self):
        """Production scanner should detect a vault secret in a .py file."""
        mock_vault = [
            {"name": "test-api-key", "value": "SYNTH_TOKEN_00001"}
        ]
        with tempfile.TemporaryDirectory() as tmp:
            vault_path = self._create_mock_vault(mock_vault)
            target = Path(tmp) / "config.py"
            target.write_text('API_KEY = "SYNTH_TOKEN_00001"')

            shutil.copy(vault_path, VAULT_PATH)

            matched = scan_file_for_secrets(target)

            self.assertGreaterEqual(len(matched), 1, "Should detect secret in .py file")
            self.assertEqual(matched[0], "test-api-key")

    def test_scan_file_detects_vault_secret_in_env_file(self):
        """Production scanner should detect a vault secret in a .env file."""
        mock_vault = [
            {"name": "test-api-key", "value": "SYNTH_TOKEN_00002"}
        ]
        with tempfile.TemporaryDirectory() as tmp:
            vault_path = self._create_mock_vault(mock_vault)
            target = Path(tmp) / ".env"
            target.write_text('AUTH_TOKEN="SYNTH_TOKEN_00002"\nDEBUG=false')

            shutil.copy(vault_path, VAULT_PATH)

            matched = scan_file_for_secrets(target)

            self.assertGreaterEqual(len(matched), 1, "Should detect secret in .env file")
            self.assertEqual(matched[0], "test-api-key")

    def test_scan_file_detects_vault_secret_in_json_file(self):
        """Production scanner should detect a vault secret in a .json file."""
        mock_vault = [
            {"name": "test-api-key", "value": "SYNTH_TOKEN_00003"}
        ]
        with tempfile.TemporaryDirectory() as tmp:
            vault_path = self._create_mock_vault(mock_vault)
            target = Path(tmp) / "config.json"
            target.write_text('{"token": "SYNTH_TOKEN_00003", "debug": false}')

            shutil.copy(vault_path, VAULT_PATH)

            matched = scan_file_for_secrets(target)

            self.assertGreaterEqual(len(matched), 1, "Should detect secret in .json file")
            self.assertEqual(matched[0], "test-api-key")

    def test_scan_file_ignores_files_without_vault_secrets(self):
        """Production scanner should NOT flag a file with no vault secrets."""
        mock_vault = [
            {"name": "test-api-key", "value": "SYNTH_TOKEN_00004"}
        ]
        with tempfile.TemporaryDirectory() as tmp:
            vault_path = self._create_mock_vault(mock_vault)
            target = Path(tmp) / "config.py"
            target.write_text('API_KEY = "completely_different_value"')

            shutil.copy(vault_path, VAULT_PATH)

            matched = scan_file_for_secrets(target)

            self.assertEqual(len(matched), 0, "Should not flag file with no vault secrets")

    # --- Test 5: scan_content_for_secrets ---

    def test_scan_content_detects_vault_secret(self):
        """Production scanner should detect a vault secret in raw content."""
        mock_vault = [
            {"name": "test-api-key", "value": "SYNTH_TOKEN_00005"}
        ]
        vault_path = self._create_mock_vault(mock_vault)
        shutil.copy(vault_path, VAULT_PATH)

        content = 'DB_PASSWORD="SYNTH_TOKEN_00005"; API_KEY="SYNTH_TOKEN_00005"'

        matched = scan_content_for_secrets(content)

        self.assertGreaterEqual(len(matched), 1, "Should detect secret in raw content")
        self.assertEqual(matched[0], "test-api-key")

    def test_scan_content_ignores_clean_content(self):
        """Production scanner should not flag content with no vault secrets."""
        mock_vault = [
            {"name": "test-api-key", "value": "SYNTH_TOKEN_00006"}
        ]
        vault_path = self._create_mock_vault(mock_vault)
        shutil.copy(vault_path, VAULT_PATH)

        content = "This is clean content with no secrets in it."

        matched = scan_content_for_secrets(content)

        self.assertEqual(len(matched), 0, "Should not flag clean content")

    # --- Test 7: check_message_for_secrets ---

    def test_check_message_blocks_secret_in_outbound_message(self):
        """Production scanner should block a message containing a vault secret."""
        mock_vault = [
            {"name": "test-api-key", "value": "SYNTH_TOKEN_00007"}
        ]
        vault_path = self._create_mock_vault(mock_vault)
        shutil.copy(vault_path, VAULT_PATH)

        message = 'Your API key is: SYNTH_TOKEN_00007 — here it is.'

        safe = check_message_for_secrets(message)

        self.assertFalse(safe, "Message containing vault secret should not be safe to send")

    def test_check_message_allows_clean_message(self):
        """Production scanner should allow a message with no vault secrets."""
        mock_vault = [
            {"name": "test-api-key", "value": "SYNTH_TOKEN_00008"}
        ]
        vault_path = self._create_mock_vault(mock_vault)
        shutil.copy(vault_path, VAULT_PATH)

        message = "This is a normal message with no secrets in it."

        safe = check_message_for_secrets(message)

        self.assertTrue(safe, "Message with no vault secrets should be safe to send")

    # --- Test 9: Vault handles multiple entries ---

    def test_scan_file_detects_multiple_secrets_in_file(self):
        """Scanner should detect multiple different vault secrets in one file."""
        mock_vault = [
            {"name": "api-key-1", "value": "SYNTH_TOKEN_MULTI_001"},
            {"name": "api-key-2", "value": "SYNTH_TOKEN_MULTI_002"},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            vault_path = self._create_mock_vault(mock_vault)
            target = Path(tmp) / "config.py"
            target.write_text('KEY1="SYNTH_TOKEN_MULTI_001"\nKEY2="SYNTH_TOKEN_MULTI_002"')

            shutil.copy(vault_path, VAULT_PATH)

            matched = scan_file_for_secrets(target)

            self.assertGreaterEqual(len(matched), 2, "Should detect both secrets in file")
            self.assertIn("api-key-1", matched)
            self.assertIn("api-key-2", matched)


# ---------------------------------------------------------------------------
# Threat Vector 2: Authorization — Only Carson can issue requests
# ---------------------------------------------------------------------------

class TestAuthorization(unittest.TestCase):
    """
    Authorization checks.
    Config-based tests verify current OpenClaw config.
    is_authorized() is the production function being tested.
    """

    def test_is_authorized_returns_true_for_carson_discord(self):
        """Production is_authorized should return True for Carson's Discord ID."""
        result = is_authorized(368889178936836102, "discord")
        self.assertTrue(result, "Carson should be authorized on Discord")

    def test_is_authorized_returns_false_for_unknown_discord_user(self):
        """Production is_authorized should return False for unknown Discord user."""
        result = is_authorized(999999999999999999, "discord")
        self.assertFalse(result, "Unknown user should not be authorized on Discord")

    def test_is_authorized_returns_false_for_unknown_telegram_user(self):
        """Production is_authorized should return False for unknown Telegram user."""
        result = is_authorized(999999999, "telegram")
        self.assertFalse(result, "Unknown Telegram user should not be authorized")

    def test_is_authorized_returns_true_for_carson_telegram(self):
        """Production is_authorized should return True for Carson's Telegram ID."""
        result = is_authorized(1404599210, "telegram")
        self.assertTrue(result, "Carson should be authorized on Telegram")


# ---------------------------------------------------------------------------
# Threat Vector 3: Destructive Acts require confirmation
# ---------------------------------------------------------------------------

class TestDestructiveActsGuard(unittest.TestCase):
    """
    Destructive action guard.
    requires_confirmation() is the production function being tested.
    """

    def test_requires_confirmation_false_for_workspace_file(self):
        """Actions on files inside workspace should NOT require confirmation."""
        workspace_file = WORKSPACE / "test.txt"
        result = requires_confirmation("write", workspace_file)
        self.assertFalse(result, "Workspace files should not require confirmation")

    def test_requires_confirmation_true_for_files_outside_workspace(self):
        """Actions on files outside workspace should require confirmation."""
        outside_file = Path("/tmp/some_other_file.txt")
        result = requires_confirmation("write", outside_file)
        self.assertTrue(result, "Files outside workspace should require confirmation")

    def test_requires_confirmation_never_allows_system_files(self):
        """System files should always require confirmation (and be blocked)."""
        system_files = [
            Path("/etc/passwd"),
            Path("/usr/bin/rm"),
            Path("/var/log/syslog"),
            Path("/dev/sda1"),
        ]
        for sys_file in system_files:
            result = requires_confirmation("write", sys_file)
            self.assertTrue(result, f"{sys_file} should always require confirmation")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)
