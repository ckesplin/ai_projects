"""
Pattern-based Secret Detection — 2026-04-24
Tests for regex/entropy secret detection (defense in depth beyond vault matching).

Run with: PYTHONPATH=. python3 tests/test_pattern_detection.py -v
"""

import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from typing import List

from src.scanner import (
    scan_content_for_secrets,
    check_message_for_secrets,
)

# Production paths
VAULT_PATH = Path("/home/clawbot/.openclaw/workspace/.secrets-vault.json")


class TestPatternBasedDetection(unittest.TestCase):
    """
    Pattern-based secret detection using regex and entropy.
    Complements vault-based detection with defense-in-depth.
    """

    def setUp(self):
        """Create a clean temp vault before each test."""
        self.temp_vault = Path(tempfile.mkdtemp()) / ".secrets-vault.json"
        with open(self.temp_vault, "w") as f:
            json.dump([], f)  # Empty vault for pattern tests

    def tearDown(self):
        """Clean up temp vault."""
        if self.temp_vault.exists():
            self.temp_vault.unlink()

    def _replace_vault(self, vault_path: Path):
        """Replace production vault with test vault."""
        import shutil
        shutil.copy(vault_path, VAULT_PATH)

    # --- GitHub tokens (ghp_, gho_, ghu_, ghs_, ghr_) ---

    def test_detects_github_token_prefix(self):
        """Should detect GitHub token with ghp_ prefix."""
        self._replace_vault(self.temp_vault)
        content = "ghp_abc123xyz456def789ghi000aaaabbbbcccc"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect ghp_ token")

    def test_detects_github_fine_grained_token(self):
        """Should detect GitHub fine-grained token with gho_ prefix."""
        self._replace_vault(self.temp_vault)
        content = "gho_abc123xyz456def789ghi000aaaabbbbccccdddd"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect gho_ token")

    def test_detects_github_personal_access_token(self):
        """Should detect GitHub PAT with ghu_ prefix."""
        self._replace_vault(self.temp_vault)
        content = "ghu_abc123xyz456def789ghi000aaaabbbbccccdddde"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect ghu_ token")

    def test_detects_github_server_access_token(self):
        """Should detect GitHub server access token with ghs_ prefix."""
        self._replace_vault(self.temp_vault)
        content = "ghs_abc123xyz456def789ghi000aaaabbbbccccdddd"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect ghs_ token")

    def test_detects_github_refresh_token(self):
        """Should detect GitHub refresh token with ghr_ prefix."""
        self._replace_vault(self.temp_vault)
        content = "ghr_abc123xyz456def789ghi000aaaabbbbccccddddeee"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect ghr_ token")

    # --- OpenAI / Anthropic keys (sk-, sk-ant-, sk-proj-) ---

    def test_detects_openai_secret_key(self):
        """Should detect OpenAI sk- prefix."""
        self._replace_vault(self.temp_vault)
        content = "sk-ZephyrIsAwesome1234567890abcdefghijklmnopqrstuvwxyz"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect sk- key")

    def test_detects_anthropic_secret_key(self):
        """Should detect Anthropic sk-ant- prefix."""
        self._replace_vault(self.temp_vault)
        content = "sk-ant-api03-abc123xyz456def789ghi000aaaabbbbccccdddd"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect sk-ant- key")

    def test_detects_anthropic_project_key(self):
        """Should detect Anthropic sk-proj- prefix."""
        self._replace_vault(self.temp_vault)
        content = "sk-proj-abc123xyz456def789ghi000aaaabbbbccccdddd"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect sk-proj- key")

    # --- AWS keys (AKIA, ABIA, ASIA, AROA) ---

    def test_detects_aws_access_key_id(self):
        """Should detect AWS AKIA prefix."""
        self._replace_vault(self.temp_vault)
        content = "AKIAABCDEFGHIJKLMNOPQ"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect AKIA key")

    def test_detects_aws_abia_key(self):
        """Should detect AWS ABIA prefix."""
        self._replace_vault(self.temp_vault)
        content = "ABIAABCDEFGHIJKLMNOPQRS"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect ABIA key")

    def test_detects_aws_asia_key(self):
        """Should detect AWS ASIA prefix."""
        self._replace_vault(self.temp_vault)
        content = "ASIAABCDEFGHIJKLMNOPQRS"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect ASIA key")

    def test_detects_aws_aroa_key(self):
        """Should detect AWS AROA prefix."""
        self._replace_vault(self.temp_vault)
        content = "AROAABCDEFGHIJKLMNOPQRS"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect AROA key")

    # --- Google API keys (AIza) ---

    def test_detects_google_api_key(self):
        """Should detect Google AIza prefix."""
        self._replace_vault(self.temp_vault)
        content = "AIzaSyDefGhiJklMnoPqrStuVwXyzABCDEF123456789"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect AIza key")

    # --- Slack tokens (xoxb-, xoxp-, xoxa-) ---

    def test_detects_slack_bot_token(self):
        """Should detect Slack xoxb- prefix."""
        self._replace_vault(self.temp_vault)
        content = "xoxb-abc123-def456-ghi789-jkl012mno345pqr"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect xoxb- token")

    def test_detects_slack_user_token(self):
        """Should detect Slack xoxp- prefix."""
        self._replace_vault(self.temp_vault)
        content = "xoxp-abc123-def456-ghi789-jkl012mno345pqr678"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect xoxp- token")

    def test_detects_slack_app_token(self):
        """Should detect Slack xoxa- prefix."""
        self._replace_vault(self.temp_vault)
        content = "xoxa-abc123-def456-ghi789"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect xoxa- token")

    # --- Telegram bot tokens ---

    def test_detects_telegram_bot_token(self):
        """Should detect Telegram bot token pattern."""
        self._replace_vault(self.temp_vault)
        content = "123456789:ABCdefGHIjklMNO-pqrSTUvwxYZ0123456789"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect Telegram bot token")

    # --- NPM tokens (npm_) ---

    def test_detects_npm_token(self):
        """Should detect NPM npm_ prefix."""
        self._replace_vault(self.temp_vault)
        content = "npm_abc123xyz456def789ghi000aaaabbbbccccddddeee"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect npm_ token")

    # --- Perplexity tokens (pplx-) ---

    def test_detects_perplexity_token(self):
        """Should detect Perplexity pplx- prefix."""
        self._replace_vault(self.temp_vault)
        content = "pplx-abc123xyz456def789ghi000aaaabbbbccccdddd"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect pplx- token")

    # --- Private key blocks (PEM) ---

    def test_detects_pem_private_key(self):
        """Should detect PEM private key block."""
        self._replace_vault(self.temp_vault)
        content = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUtU7W1vqD
y3K5z3F2f8g9H2iJk4Jl0qU7wX+YzB0I8hVW3pQnF7sN2vL9xK2mR4fT6yB8jWk
-----END PRIVATE KEY-----"""
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect PEM private key")

    def test_detects_rsa_private_key(self):
        """Should detect RSA private key block."""
        self._replace_vault(self.temp_vault)
        content = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA0Z3VS5K9N6U7x2Q8fH4mY6pL2kJjdgF8hK0l9V7qW3nR5sX
-----END RSA PRIVATE KEY-----"""
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect RSA private key")

    def test_detects_ec_private_key(self):
        """Should detect EC private key block."""
        self._replace_vault(self.temp_vault)
        content = """-----BEGIN EC PRIVATE KEY-----
MHQCAQEEIFzQZXz3VS5K9N6U7x2Q8fH4mY6pL2kJjdgF8hK0l9V7qW3nR5sXO
-----END EC PRIVATE KEY-----"""
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect EC private key")

    # --- Database connection strings ---

    def test_detects_postgres_connection_string(self):
        """Should detect PostgreSQL connection string."""
        self._replace_vault(self.temp_vault)
        content = "postgres://user:password@host:5432/database"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect postgres://")

    def test_detects_mysql_connection_string(self):
        """Should detect MySQL connection string."""
        self._replace_vault(self.temp_vault)
        content = "mysql://user:password@host:3306/database"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect mysql://")

    def test_detects_mongodb_connection_string(self):
        """Should detect MongoDB connection string."""
        self._replace_vault(self.temp_vault)
        content = "mongodb+srv://user:password@cluster.mongodb.net/database"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect mongodb+srv://")

    def test_detects_redis_connection_string(self):
        """Should detect Redis connection string."""
        self._replace_vault(self.temp_vault)
        content = "redis://default:password@host:6379"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect redis://")

    def test_detects_amqp_connection_string(self):
        """Should detect AMQP connection string."""
        self._replace_vault(self.temp_vault)
        content = "amqp://user:password@host:5672/vhost"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect amqp://")

    # --- High-entropy string detection ---

    def test_detects_high_entropy_string(self):
        """Should detect high-entropy string that looks like a secret."""
        self._replace_vault(self.temp_vault)
        # String with high entropy (>4.5 bits per char = likely random/secret)
        content = "xKj9#mPq3$vL2@nZo8!WkR4&FyB7^hT6*gD1"
        matched = scan_content_for_secrets(content)
        self.assertGreaterEqual(len(matched), 1, "Should detect high-entropy string")

    # --- False positive prevention ---

    def test_allows_normal_text_without_secrets(self):
        """Should NOT flag normal text without secret patterns."""
        self._replace_vault(self.temp_vault)
        content = "This is just normal text about Python programming and API design."
        matched = scan_content_for_secrets(content)
        self.assertEqual(len(matched), 0, "Should not flag normal text")

    def test_allows_urls_without_credentials(self):
        """Should NOT flag URLs without embedded credentials."""
        self._replace_vault(self.temp_vault)
        content = "Check out https://github.com/openclaw/openclaw for more info."
        matched = scan_content_for_secrets(content)
        self.assertEqual(len(matched), 0, "Should not flag URLs without credentials")

    def test_allows_code_without_secrets(self):
        """Should NOT flag normal code without secret patterns."""
        self._replace_vault(self.temp_vault)
        content = """
def hello():
    print("Hello, World!")

response = requests.get("https://api.example.com/data")
print(response.json())
"""
        matched = scan_content_for_secrets(content)
        self.assertEqual(len(matched), 0, "Should not flag code without secrets")

    # --- Message blocking ---

    def test_check_message_blocks_pattern_secret(self):
        """check_message_for_secrets should block messages with pattern secrets."""
        self._replace_vault(self.temp_vault)
        message = "Your GitHub token is: ghp_abc123xyz456def789ghi000aaaabbbbcccc"
        safe = check_message_for_secrets(message)
        self.assertFalse(safe, "Message with pattern secret should not be safe")

    def test_check_message_allows_clean_message(self):
        """check_message_for_secrets should allow messages without secrets."""
        self._replace_vault(self.temp_vault)
        message = "Hello! This is a normal message with no secrets."
        safe = check_message_for_secrets(message)
        self.assertTrue(safe, "Message without secrets should be safe")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)
