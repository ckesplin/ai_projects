---
name: plan
description: >
  Planning skill — removes ambiguity from vague requests through reactive questioning.
  Triggered when a user types `/plan` with or without a topic. Asks the highest-leverage
  questions first, classifies every answer as Stated, Deferred, or Declined, and spawns
  follow-up questions until no gaps remain. Supports shelving, resuming, listing, exporting,
  and deleting sessions. Never guess — every unknown is either answered or explicitly deferred.
---

# Plan — Epistemic Clarity Engine

*Plan is forethought made systematic. No assumption should survive a Plan session.*

---

## What Plan Is

Plan removes ambiguity from vague requests by asking questions until every gap is resolved — either by the user stating a preference, explicitly deferring to the agent, or actively declining a feature.

**The core problem:** Vague requests lead to implementation choices made by assumption instead of by decision. Plan ensures nothing is guessed.

---

## Commands

| Command | Description |
|:---|:---|
| `/plan [topic]` | Start a new planning session. If no topic is given, ask "What do you want to plan?" first, then begin questioning. |
| `/plan shelve` | Pause and exit the active planning context. The session has already been saved incrementally — shelving only stops the conversation. |
| `/plan list` | List all saved sessions, separated into **Complete** and **Incomplete**. |
| `/plan continue [session name]` | Resume a session by name. If no name is given, show all incomplete sessions and ask which one to continue. |
| `/plan export [session name]` | Export a **complete** session as a clarity map in a Markdown file. Incomplete sessions cannot be exported. |
| `/plan delete [session name]` | Permanently remove a session from memory. Confirm before deleting. |

---

## The Three Outcomes

Every question must end in one of three outcomes:

| Outcome | Meaning | Who Decides |
|:---|:---|:---|
| **Stated** | User has a specific preference | User |
| **Deferred** | User has no preference — agent chooses | Agent |
| **Declined** | User actively does not want this | User |

**Termination condition:** The session is complete when there are no unanswered questions and no unstated assumptions remaining. Every gap has resolved to Stated, Deferred, or Declined. If any question is still ambiguous and not deferred — keep asking.

---

## Question Types

| Type | Trigger | Purpose |
|:---|:---|:---|
| **Specifying** | Answer is vague or broad | Get specific: "A portfolio" → what kind, what content |
| **Enumerating** | Answer implies a list without count | Set a boundary: "projects" → how many, which ones |
| **Clarifying** | Answer has competing elements | Resolve tension: "peers + employers" → same content or different priority |
| **Assumption-testing** | Answer implies something unstated | Surface hidden decisions: "live website" → what hosting, what domain |
| **Deferral-testing** | Answer is "I don't know / whatever" | Confirm it's a true deferral, not avoidance |
| **Preference-testing** | Answer is subjective | Calibrate standard: "clean and simple" → what does that look like |

---

## Spawning Rule

**Any time an answer contains or implies something unknown, that spawns a question.**

Question order is reactive — not a fixed sequence. If answering AUDIENCE spawns a sub-question about FORMAT, ask it immediately before returning to the original sequence.

Every answer can spawn follow-up questions. If an answer implies a gap, ask about it.

---

## Starting Frame

When a session begins, use the following as the highest-leverage starting questions. Adapt based on responses — this is a frame, not a fixed sequence:

```
GOAL       — What exactly should this do / achieve?
AUDIENCE   — Who is the primary user / audience?
FORMAT     — What format / platform / output?
SUCCESS    — How will we know when this is done?
TIMELINE   — What is the deadline / urgency?
DATA       — What data / content is needed?
```

---

## Session Flow

```
/plan [topic]
    │
    ▼
Ask highest-leverage questions reactively
    │
    ▼
Classify each answer: Stated / Deferred / Declined
Spawn follow-up questions as needed
    │
    ▼
Termination: no unanswered questions, no unstated assumptions
    │
    ▼
Session marked Complete
    │
    ▼
/plan export [session name]  →  Clarity map as Markdown file
```

---

## Deferred Decisions — How I Choose

When you defer to me, I choose based on:

- Your stated preferences elsewhere in the session
- Industry best practice for the use case
- Simplest solution that achieves the stated goal
- Minimizing future change cost

I will tell you what I decided and why. If you disagree, you override.

---

## When to Use Plan

**Use Plan when:**
- Request is vague ("Build me something", "Make it better")
- You don't have specific preferences and are OK with me choosing
- Multiple stakeholders with different expectations
- High-stakes implementation (expensive, time-consuming)
- Past projects failed due to miscommunication

**Plan is not needed when:**
- Request is already specific enough to act on without guessing
- Quick prototype / throwaway code
- You have explicit, complete requirements in mind

---

## Session Name Schema

Session names follow the format:

```
YYYY-MM-DD-topic-slug
```

The topic is lowercased and spaces are replaced with hyphens. If two sessions share the same date and topic slug, append a increasing integer ID to disambiguate:

```
2026-04-11-portfolio-site
2026-04-11-api-redesign
2026-04-11-api-redesign-2   ← collision resolved
```

The session name is generated automatically when the session starts and shown to the user immediately.

---

## Storage

```
~/.agent-factory/plan/
├── clarity-ledger.jsonl    # All sessions (append-only log)
└── sessions/
    └── {session_name}.json # Individual session state
```

Sessions are saved incrementally — after every answer, after every new question is formed, and after every outcome is determined. There is no manual save step. `/plan shelve` only exits the planning context; all progress is already persisted.

Each session file stores: the original request, all questions asked, each answer or deferral, the outcome for every question (Stated / Deferred / Declined), and the session status (complete / incomplete).

---

## Export Format

Exported clarity maps are Markdown files with the following structure:

```markdown
# Clarity Map: [Session Name]

**Request:** [original request]
**Status:** Complete
**Exported:** [date]

---

## Decisions

| Question | Answer | Outcome |
|:---|:---|:---|
| What is the goal? | Build a developer portfolio | Stated |
| What is the target audience? | Recruiters and peers | Stated |
| What format? | Web app | Stated |
| What hosting platform? | Agent chose Vercel (simplest for static React) | Deferred |
| Include a blog section? | Not wanted | Declined |

---

## Deferred Decisions

- **Hosting platform:** Vercel — chosen for simplicity and zero-config React deployment.

---

## Declined Features

- Blog section
```

Only sessions with status **Complete** may be exported.

---

## Rules

- Never guess. Every unknown is either answered (Stated), handed back to the agent (Deferred), or removed from scope (Declined).
- Ask one question at a time. Do not present multiple questions simultaneously.
- If the user says "I don't know" or "whatever" or something similar to those, use a deferral-testing question to confirm it is a genuine deferral before marking it as Deferred.
- A session is complete only when every question has a final outcome. Ambiguous answers do not count.
- `/plan export` is only available for complete sessions. If the user attempts to export an incomplete session, inform them which questions remain open.
- `/plan delete` always requires explicit confirmation before removing a session.
