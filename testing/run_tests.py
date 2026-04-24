#!/usr/bin/env python3
import sys
import json
import atexit

sys.path.insert(0, "/home/clawbot/.openclaw/workspace/testing/security-tests")
from tests.test_security import *
import unittest

VAULT_PATH = "/home/clawbot/.openclaw/workspace/secrets/.secrets-vault.json"

def cleanup_vault():
    try:
        with open(VAULT_PATH, "w") as f:
            json.dump([], f)
        print("\n[teardown] Vault cleared")
    except Exception as e:
        print(f"\n[teardown] Could not clear vault: {e}")

atexit.register(cleanup_vault)

unittest.main(module='tests.test_security', argv=[''], exit=False, verbosity=2)