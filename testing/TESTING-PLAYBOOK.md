# TESTING PLAYBOOK — General Principles for Test Writing

_Built from lessons learned during security test development. Applies to all test writing._

---

## Core Principle: Tests Verify Behavior, Not State

A test should verify that a system does what it claims — not that it contains certain data or exists in a certain state. The goal is confidence in behavior, not proof of a snapshot.

---

## 1. Value-Based Detection Over Name-Based Detection

**Principle:** Detect the asset itself, not its container or variable name.

- The value `"sk-abc123def"` is the secret — not `API_KEY` or `auth_token`
- Detection that depends on variable names breaks when the same value appears in a different context
- Ask: "What exactly am I protecting?" — protect the value, not the label

**Anti-pattern:** Flagging a file because it contains `API_KEY = "..."`
**Correct pattern:** Flagging a file because it contains `"sk-abc123def"` regardless of the variable name

---

## 2. Denylist/Allowlist Over Pattern Guessing

**Principle:** When protecting specific values, maintain an explicit list. Pattern matching is a secondary layer, not the primary mechanism.

- Explicit vaults/denylists are precise and auditable
- Regex patterns are useful for catching unknown leaks (secondary detection) but are too noisy as the primary mechanism
- The vault is the source of truth; patterns are noise reduction

**Anti-pattern:** Relying entirely on regex like `API_KEY.*=.*['"][A-Za-z0-9]{20,}['"]`
**Correct pattern:** Check content against an explicit list of known secrets; use patterns only for unknown leaks

---

## 3. Tests Must Be Isolated From Production Data and State

**Principle:** Tests create their own temporary infrastructure. Synthetic data only. Nothing touches production resources.

- Create temporary vaults, files, and configs within the test
- Clean up after the test (use `tempfile.TemporaryDirectory()` or `tearDown`)
- Never load or reference real secrets in test code
- Tests should be reproducible on any machine without external dependencies

**Anti-pattern:** Loading `~/.secrets-vault.json` directly in a test
**Correct pattern:** `_create_mock_vault(tmp_dir, synthetic_entries)` — isolated to test scope

---

## 4. Never Echo Sensitive Values in Any Output Channel

**Principle:** Sensitive values — secrets, tokens, personal data, account numbers — must never appear as literal strings in any output.

- In messages: use `[KEY VALUE]` as the reference format
- In logs: reference by name or index, never by value
- In error messages: describe the problem, never reveal the data
- In test output: assertions verify presence/absence, never print the actual value

**Anti-pattern:** `print(f"Found secret: {secret_value}")` or `assertEqual(secret, "expected")`
**Correct pattern:** `assertIn(secret_name, matched_secrets)` or `self.assertGreaterEqual(len(matched), 1)`

---

## 5. Temporary Test Infrastructure Must Mirror Production Behavior

**Principle:** The test infrastructure (temp files, mock configs) should reflect how the production system actually works. Don't create artificial scenarios.

- Production reads from a vault file at a known path → test creates a temp vault at an analogous path
- Production checks content before sending → test verifies the check mechanism, not just the data
- The goal: test validates real behavior, not an idealized scenario

**Anti-pattern:** Hardcoding paths or behavior that doesn't match how the production system actually works
**Correct pattern:** Reproduce the production workflow in temp context so the test catches real integration issues

---

## 6. Confirm Before Modifying or Transmitting Sensitive Data

**Principle:** Any request to retrieve, modify, or transmit a sensitive value requires explicit user confirmation. The value itself is never echoed back.

- When a test simulates a "transmit secret" scenario, it should verify that the confirmation gate exists
- When a test simulates a "retrieve secret" request, it should verify the value is not echoed
- This applies at runtime — but tests should also verify the guard exists

---

## 7. Generalize Lessons After Each Test Review

**Principle:** When a test changes based on feedback, extract the underlying principle. The lesson is not "change this test" — it is "here is a principle that applies to all future tests."

- After each review, ask: "What is the general rule this change implies?"
- Update this playbook, not just the individual test
- Avoid repeating the same mistake across different test suites

---

## 8. TDD: Write Failing Tests Before Implementation

**Principle:** Tests define the expected behavior first. Implementation follows to make them pass.

- Write a test that calls the production interface (function, class, module) — not a mock helper within the test
- The test fails because the production code doesn't exist yet
- Implement the production code until the test passes
- Never write implementation code before a test that exercises it

**The correct sequence:**
1. Write the test — it references `scan_file_for_secrets(target)` or similar production interface
2. Verify the test fails (NameError, ImportError, or assertion failure)
3. Write the minimal implementation to make it pass
4. Repeat

**Anti-pattern:** Writing the implementation first and then writing tests that mock internal helpers
**Correct pattern:** `matched = scan_file_for_secrets(target)` — calling production code that doesn't exist yet, so the test fails

---

## 9. Tests Cover All Critical Behaviors

**Principle:** Every critical behavior must have a test. No behavior is "obviously correct" without a test.

- Happy path: the main expected behavior works
- Edge cases: empty files, missing vaults, unknown file types
- Error paths: permission denied, malformed content, vault not found
- Security boundaries: unauthorized access attempts, out-of-scope files

**Anti-pattern:** Testing only the happy path and assuming edge cases are handled
**Correct pattern:** Each critical behavior has a dedicated test — one scenario per test for clarity

---

## Test Structure Template

```python
class Test<Feature>(unittest.TestCase):
    """Verify <what this feature does>."""

    def _create_mock_<resource>(self, tmp_dir: Path, entries: List[dict]) -> Path:
        """Create isolated mock resource with synthetic test data."""
        # ... implementation
        return path

    def _<action>_with_<resource>(self, target: Path, resources: List[dict]) -> result:
        """Perform action against provided resources."""
        # ... implementation
        return result

    def test_<scenario>(self):
        """Expected behavior: <what should happen>."""
        mock_<resource> = [{"name": "<synthetic-name>", "value": "<SYNTHETIC_VALUE>"}]
        with tempfile.TemporaryDirectory() as tmp:
            resource_path = self._create_mock_<resource>(Path(tmp), mock_<resource>)
            target = Path(tmp) / "<target_file>"
            target.write_text("<content containing synthetic value>")

            result = self._<action>_with_<resource>(target, mock_<resource>)

            self.assert<Equal|Greater|IsInstance>(result, <expected>)
```

---

## Secrets Reference Format

When referring to secret values in any communication:

- Always use `[KEY VALUE]` — never the actual secret string
- Example: `The vault contains 3 entries — [KEY VALUE] referenced in 1 file`
- This applies to: messages, logs, error output, test output, documentation

---

## When to Write Tests

- Before implementing a feature: write tests that define expected behavior
- After a bug is found: write a test that would have caught it
- After a review change: generalize the lesson and update the playbook
- When the approach is unclear: write a test to clarify the expected behavior

---

_This playbook is a living document. Update it after every test review._
_Last updated: 2026-04-21_
