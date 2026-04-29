"""
Security Test Suite — Pattern-based Secrets Detection + Authorization + Destructive Acts

Tests cover three threat vectors:
  1. Secrets leaking — pattern-based detection (regex for known formats)
  2. Authorization — only Carson can issue requests
  3. Destructive acts require confirmation

Run with: PYTHONPATH=. python3 tests/test_security.py -v
"""

import json
import os
import tempfile
import unittest
from pathlib import Path

# Re-import scanner module
from src import scanner

# Production paths
WORKSPACE = Path("/home/clawbot/.openclaw/workspace")
OPENCLAW_CONFIG = Path("/home/clawbot/.openclaw/openclaw.json")


# ---------------------------------------------------------------------------
# Threat Vector 2: Authorization — Only Carson can issue requests
# ---------------------------------------------------------------------------

class TestAuthorization(unittest.TestCase):
    """
    Authorization checks.
    Config-based tests verify current OpenClaw config.
    scanner.is_authorized() is the production function being tested.
    """

    def test_is_authorized_returns_true_for_carson_discord(self):
        """Production is_authorized should return True for Carson's Discord ID."""
        result = scanner.is_authorized(368889178936836102, "discord")
        self.assertTrue(result, "Carson should be authorized on Discord")

    def test_is_authorized_returns_false_for_unknown_discord_user(self):
        """Production is_authorized should return False for unknown Discord user."""
        result = scanner.is_authorized(999999999999999999, "discord")
        self.assertFalse(result, "Unknown user should not be authorized on Discord")

    def test_is_authorized_returns_false_for_unknown_telegram_user(self):
        """Production is_authorized should return False for unknown Telegram user."""
        result = scanner.is_authorized(999999999, "telegram")
        self.assertFalse(result, "Unknown Telegram user should not be authorized")

    def test_is_authorized_returns_true_for_carson_telegram(self):
        """Production is_authorized should return True for Carson's Telegram ID."""
        result = scanner.is_authorized(1404599210, "telegram")
        self.assertTrue(result, "Carson should be authorized on Telegram")


# ---------------------------------------------------------------------------
# Threat Vector 3: Destructive Acts require confirmation
# ---------------------------------------------------------------------------

class TestDestructiveActsGuard(unittest.TestCase):
    """
    Destructive action guard.
    scanner.requires_confirmation() is the production function being tested.
    """

    def test_requires_confirmation_false_for_workspace_file(self):
        """Actions on files inside workspace should NOT require confirmation."""
        workspace_file = WORKSPACE / "test.txt"
        result = scanner.requires_confirmation("write", workspace_file)
        self.assertFalse(result, "Workspace files should not require confirmation")

    def test_requires_confirmation_true_for_files_outside_workspace(self):
        """Actions on files outside workspace should require confirmation."""
        outside_file = Path("/tmp/some_other_file.txt")
        result = scanner.requires_confirmation("write", outside_file)
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
            result = scanner.requires_confirmation("write", sys_file)
            self.assertTrue(result, f"{sys_file} should always require confirmation")


# ---------------------------------------------------------------------------
# Threat Vector 1: Secrets Detection (pattern-based)
# Uses test_pattern_detection.py for comprehensive pattern tests
# ---------------------------------------------------------------------------

class TestMessageScanning(unittest.TestCase):
    """
    Message content scanning for secrets.
    scanner.check_message_for_secrets() is the production function.
    """

    def test_check_message_blocks_github_token(self):
        """check_message_for_secrets should block GitHub tokens."""
        message = "Your GitHub token is: ghp_abc123xyz456def789ghi000aaaabbbbcccc"
        safe = scanner.check_message_for_secrets(message)
        self.assertFalse(safe, "Message with GitHub token should not be safe")

    def test_check_message_blocks_openai_key(self):
        """check_message_for_secrets should block OpenAI keys."""
        message = "API key: sk-ZephyrIsAwesome1234567890abcdefghijklmnopqrstuvwxyz"
        safe = scanner.check_message_for_secrets(message)
        self.assertFalse(safe, "Message with OpenAI key should not be safe")

    def test_check_message_blocks_aws_key(self):
        """check_message_for_secrets should block AWS keys."""
        message = "AWS credentials: AKIAABCDEFGHIJKLMNOPQ"
        safe = scanner.check_message_for_secrets(message)
        self.assertFalse(safe, "Message with AWS key should not be safe")

    def test_check_message_allows_clean_message(self):
        """check_message_for_secrets should allow normal messages."""
        message = "Hello! This is a normal message with no secrets in it."
        safe = scanner.check_message_for_secrets(message)
        self.assertTrue(safe, "Message without secrets should be safe")


class TestFileScanning(unittest.TestCase):
    """
    File content scanning for secrets.
    scanner.scan_file_for_secrets() is the production function.
    """

    def test_scan_file_detects_github_token(self):
        """scan_file_for_secrets should detect GitHub tokens in files."""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "config.py"
            target.write_text('GITHUB_TOKEN = "ghp_abc123xyz456def789ghi000aaaabbbbcccc"')

            matched = scanner.scan_file_for_secrets(target)

            self.assertGreaterEqual(len(matched), 1, "Should detect GitHub token")
            self.assertIn("github_token", matched)

    def test_scan_file_detects_database_connection_string(self):
        """scan_file_for_secrets should detect database connection strings."""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "config.json"
            target.write_text('{"db": "postgres://user:password@host:5432/database"}')

            matched = scanner.scan_file_for_secrets(target)

            self.assertGreaterEqual(len(matched), 1, "Should detect database connection")
            self.assertIn("postgres_connection", matched)

    def test_scan_file_ignores_clean_code(self):
        """scan_file_for_secrets should not flag normal code."""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "app.py"
            target.write_text('''
def hello():
    print("Hello, World!")

response = requests.get("https://api.example.com/data")
print(response.json())
''')

            matched = scanner.scan_file_for_secrets(target)

            self.assertEqual(len(matched), 0, "Should not flag normal code")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)