"""
Security Scanner — Production Implementation

Handles three threat vectors:
  1. Secrets leaking — pattern-based detection (GitHub, OpenAI, AWS, etc.)
  2. Authorization — only authorized users can issue requests
  3. Destructive acts require confirmation

Secrets detection uses regex patterns for known secret formats.
No vault file is used — patterns catch known formats like ghp_, sk-, AKIA, etc.
"""

import json
import math
import os
import re
from pathlib import Path
from typing import List

# Production paths
WORKSPACE = Path("/home/clawbot/.openclaw/workspace")
OPENCLAW_CONFIG = Path("/home/clawbot/.openclaw/openclaw.json")

# System paths that require confirmation (never allowed without explicit override)
SYSTEM_PATHS = ["/etc", "/usr", "/bin", "/sbin", "/var", "/boot", "/dev", "/sys", "/proc"]

# Pattern-based secret detection (compiled once at module load)
PATTERNS = {
    # GitHub tokens (flexible length to handle various token formats)
    "github_token": re.compile(r'\bghp_[a-zA-Z0-9]{20,}\b'),
    "github_fine_grained_token": re.compile(r'\b(gho|ghu|ghs|ghr)_[a-zA-Z0-9]{20,}\b'),
    
    # OpenAI / Anthropic
    "openai_key": re.compile(r'\bsk-[a-zA-Z0-9_-]{20,}\b'),
    "anthropic_key": re.compile(r'\bsk-ant-[a-zA-Z0-9]{20,}\b'),
    "anthropic_project_key": re.compile(r'\bsk-proj-[a-zA-Z0-9]{20,}\b'),
    
    # AWS (flexible length to handle various key formats)
    "aws_access_key": re.compile(r'\b(AKIA|ABIA|ASIA|AROA)[A-Z0-9]{10,}\b'),
    
    # Google
    "google_api_key": re.compile(r'\bAIza[0-9A-Za-z_-]{35,}\b'),
    
    # Slack
    "slack_bot_token": re.compile(r'\bxox[baprs]-[0-9a-zA-Z,-]{10,}\b'),
    
    # Telegram bot tokens
    "telegram_bot_token": re.compile(r'\b\d{8,10}:[a-zA-Z0-9_-]{35}\b'),
    
    # NPM (flexible length)
    "npm_token": re.compile(r'\bnpm_[a-zA-Z0-9]{20,}\b'),
    
    # Perplexity
    "perplexity_token": re.compile(r'\bpplx-[a-zA-Z0-9]{20,}\b'),
    
    # Private keys (PEM blocks)
    "pem_private_key": re.compile(r'-----BEGIN\s+(PRIVATE|RSA|EC)\s+KEY-----'),
    
    # Database connection strings
    "postgres_connection": re.compile(r'\bpostgres://[^\s]+\b'),
    "mysql_connection": re.compile(r'\bmysql://[^\s]+\b'),
    "mongodb_connection": re.compile(r'\bmongodb(\+srv)?://[^\s]+\b'),
    "redis_connection": re.compile(r'\bredis://[^\s]+\b'),
    "amqp_connection": re.compile(r'\bamqp://[^\s]+\b'),
}


def _shannon_entropy(s: str) -> float:
    """Calculate Shannon entropy of a string (bits per character)."""
    if not s:
        return 0.0
    frequency = {}
    for c in s:
        frequency[c] = frequency.get(c, 0) + 1
    entropy = 0.0
    length = len(s)
    for count in frequency.values():
        p = count / length
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def _detect_high_entropy(content: str, threshold: float = 4.5, min_length: int = 20) -> List[str]:
    """Detect high-entropy strings that might be secrets."""
    detected = []
    # Split content into tokens and check each word-like string
    tokens = re.findall(r'[a-zA-Z0-9#\$@!%^&*()?+\-=_{}\[\]\\|/.,;:"\']{20,}', content)
    for token in tokens:
        if _shannon_entropy(token) >= threshold:
            detected.append("high_entropy_secret")
            break  # Only report once per content
    return detected


def scan_file_for_secrets(file_path: Path) -> List[str]:
    """
    Scan a file for pattern-based secrets.
    Returns list of matched secret type names.
    """
    if not file_path.exists():
        return []
    content = file_path.read_text(errors="ignore")
    return scan_content_for_secrets(content)


def scan_content_for_secrets(content: str) -> List[str]:
    """
    Scan raw content string for secrets using pattern detection.
    Returns list of matched secret type names.
    """
    matched = []
    seen = set()  # Avoid duplicates

    # 1. Pattern-based detection
    for pattern_name, pattern in PATTERNS.items():
        if pattern.search(content):
            if pattern_name not in seen:
                matched.append(pattern_name)
                seen.add(pattern_name)

    # 2. High-entropy detection
    for entropy_type in _detect_high_entropy(content):
        if entropy_type not in seen:
            matched.append(entropy_type)
            seen.add(entropy_type)

    return matched


def check_message_for_secrets(message: str) -> bool:
    """
    Check if a message contains any pattern-matched secrets.
    Returns True if message is safe to send, False if it contains secrets.
    """
    matched = scan_content_for_secrets(message)
    return len(matched) == 0


def is_authorized(sender_id: int, channel: str) -> bool:
    """
    Check if a sender is authorized to issue requests on a given channel.
    Returns True if authorized, False otherwise.
    """
    with open(OPENCLAW_CONFIG) as f:
        config = json.load(f)

    channels = config.get("channels", {})
    channel_config = channels.get(channel, {})

    # Discord authorization
    if channel == "discord":
        allow_from = channel_config.get("allowFrom", [])
        # IDs may be stored as strings or ints
        allowed_ids = [int(x) if isinstance(x, str) else x for x in allow_from]
        return sender_id in allowed_ids

    # Telegram authorization
    elif channel == "telegram":
        # Check allowFrom or dmPolicy
        allow_from = channel_config.get("allowFrom", [])
        allowed_ids = [int(x) if isinstance(x, str) else x for x in allow_from]
        return sender_id in allowed_ids

    return False


def requires_confirmation(action: str, target_path: Path) -> bool:
    """
    Determine if an action on a target path requires user confirmation.
    Actions outside workspace require confirmation. System files never allowed.
    Returns True if confirmation required, False otherwise.
    """
    target_str = str(target_path)

    # System files always require confirmation
    for sys_path in SYSTEM_PATHS:
        if target_str.startswith(sys_path):
            return True

    # Workspace files do not require confirmation
    if target_str.startswith(str(WORKSPACE)):
        return False

    # Anything outside workspace requires confirmation
    return True