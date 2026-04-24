"""
Security Scanner — Production Implementation
Implements the functions defined in test_security.py
"""

import json
from pathlib import Path
from typing import List

# Production paths
WORKSPACE = Path("/home/clawbot/.openclaw/workspace")
OPENCLAW_CONFIG = Path("/home/clawbot/.openclaw/openclaw.json")
VAULT_PATH = Path("/home/clawbot/.openclaw/workspace/.secrets-vault.json")

# System paths that require confirmation (never allowed without explicit override)
SYSTEM_PATHS = ["/etc", "/usr", "/bin", "/sbin", "/var", "/boot", "/dev", "/sys", "/proc"]


def load_vault() -> List[dict]:
    """Load the secrets vault. Returns list of {name, value} entries."""
    if not VAULT_PATH.exists():
        return []
    with open(VAULT_PATH) as f:
        return json.load(f)


def scan_file_for_secrets(file_path: Path) -> List[str]:
    """
    Scan a file for vault secret values.
    Returns list of matched secret NAMES (not values).
    """
    if not file_path.exists():
        return []
    content = file_path.read_text(errors="ignore")
    return scan_content_for_secrets(content)


def scan_content_for_secrets(content: str) -> List[str]:
    """
    Scan raw content string for vault secret values.
    Returns list of matched secret NAMES.
    """
    vault = load_vault()
    if not vault:
        return []
    matched = []
    for entry in vault:
        name = entry.get("name", "unknown")
        value = entry.get("value", "")
        if value and value in content:
            matched.append(name)
    return matched


def check_message_for_secrets(message: str) -> bool:
    """
    Check if a message contains any vault secret values.
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