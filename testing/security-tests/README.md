# Security Test Suite

Test suite for `2026-04-21-security-scans` clarity map.

## Structure

```
security-tests/
├── pytest.ini              # pytest configuration
├── tests/
│   └── test_security.py  # All test cases
├── README.md             # This file
└── SPEC.md               # Spec source (clarity map decisions)
```

## Running

```bash
cd /home/clawbot/.openclaw/workspace/security-tests
python3 -m pytest tests/ -v
```

## Test Coverage

### Threat Vector 1: Secrets Leaking
- `TestSecretsDetection` — 8 tests
  - Detects: API keys, tokens, AWS keys, private keys, passwords, account numbers
  - Verifies scanner runs over workspace files without errors
  - Ignores safe content (false positive checks)

### Threat Vector 2: Authorization
- `TestAuthorization` — 6 tests
  - Discord: groupPolicy=allowlist, allowFrom contains Carson (368889178936836102), guild-level user restriction, dmPolicy=allowlist
  - Telegram: dmPolicy or allowFrom exists, 1404599210 in allowFrom

### Threat Vector 3: Destructive Acts
- `TestDestructiveActsGuard` — 5 tests
  - Workspace boundary is correct
  - System files are outside workspace
  - External transmission allowlist is empty or defined
  - Confirmation prompt format is documented
  - Dangerous system paths are not inside workspace

## Dependencies

- Python 3.12+
- pytest

```bash
pip install pytest
```
