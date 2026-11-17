# Workshop assignment: build, verify, and audit MiniPOSIX

You are developing a **small library**, not a POSIX framework. Use OpenCode as a collaborator, but check its suggestions against tests and documentation. The goal is to learn how to verify AI-assisted work in a domain you may not know yet.

## Before coding

Rate your starting familiarity from **0 (none)** to **3 (comfortable)**. Keep the answers in your team's notes; they are for reflection, not grading.

| Topic | 0–3 | One thing you already know or need to look up |
| --- | --- | --- |
| C++ ownership and move semantics | | |
| POSIX file descriptors and pipes | | |
| AI coding agents | | |

Read [README.md](README.md), run the tool checks, configure `clang22-debug`, and run the smoke and functional tests separately. A smoke pass with functional failures is the intended initial state.

## Audit A: an AI agent in an unfamiliar domain

**Question:** Can your team use an agent to build a small library and verify its behavior without already knowing POSIX?

Implement the contract in the public headers:

- `miniposix::UniqueFd` owns at most one file descriptor. Its default state is invalid. The destructor closes an owned descriptor. `get()` observes it, `release()` transfers the raw descriptor out without closing it, and `reset()` replaces or clears ownership. Moving transfers ownership and invalidates the source. Copying is disabled.
- `miniposix::Pipe::create()` creates one read end and one write end or reports the operating-system error with `std::system_error`. `read_end()` and `write_end()` expose references to their owning `UniqueFd` objects; call `.get()` to pass a raw descriptor to POSIX I/O. The headers define the exact signatures and error behavior.
- Correct behavior includes resource lifetime, not just return values. A test should be able to show that an old descriptor is closed after ownership changes. You may add focused public tests while you work.

Useful terms to look up: `open`, `close`, `pipe`/`pipe2`, `read`, `write`, `errno`, RAII, move constructor, move assignment, and `std::system_error`. Read the relevant documentation before accepting an agent's explanation. The optional I/O helper exercise must distinguish end-of-file, interrupted calls, errors, and short transfers if you choose to attempt it. `fork`, `exec`, signal handling, `poll`, and an event loop are outside the required implementation.

Suggested sequence:

1. Ask OpenCode to explain the contract and propose an implementation and test plan. Make it identify any assumptions about ownership or error paths.
2. Approve commands deliberately. Inspect the diff and explain each change to a teammate.
3. Build, run the smoke test, then run functional tests. For a failure, inspect the real descriptor behavior and revise the code or test as needed.
4. Consult POSIX/C++ documentation to verify at least one claim made by the agent. Record a mistake or an uncertain claim, even if the code ultimately works.
5. Commit, push, open a PR **to `main` in your own fork**, and inspect the Actions result. A green CI result is feedback, not proof of complete correctness.

Keep a short log of your attempts. Add rows as needed:

| Attempt | Failing test or observed behavior | Help needed? | AI mistake or uncertain claim | Evidence and reason for the correction |
| --- | --- | --- | --- | --- |
| 1 | | | | |
| 2 | | | | |

This exercise records what your team observed. It cannot establish that AI replaces domain knowledge without a broader controlled study.

Before moving to Audit B, check that you have a successful build, a passing smoke test, a reasoned explanation of any functional failures, and a branch pushed to your fork with a PR and CI results. A typical bug to investigate is a descriptor that looks correctly stored in the wrapper but remains open after ownership is replaced.

## Audit B: correctness and performance

Once the functional tests pass, use the provided pipe benchmark and CSV analysis described in [README.md](README.md). The benchmark should complete for each buffer size, verify the bytes transferred, and save repeat measurements. It handles short I/O and avoids depending on timing thresholds in CI.

In your team's notes, answer:

1. Which buffer size had the highest median throughput in your run? Was the ordering stable across repeats?
2. What parts of the transfer are included in the timing? Why is this **not** a measurement of the `UniqueFd` wrapper alone?
3. Which observations might change on another machine or under a different system load? If you used `perf stat`, which counters were available and what did they add?
4. What would you change in the experiment before claiming that one variant is generally faster?

If your library is unfinished, use the instructor's reference variant or a supplied CSV for the analysis portion. Report the provenance of the data. Do not invent measurements. You can ask AI to suggest interpretations, but check them against the raw CSV, repeats, and measurement conditions.

## Afternoon exercise: compare AI answers and design a verification workflow

Choose one specific question about POSIX behavior that matters to your implementation, such as descriptor ownership, end-of-file, or short `read`/`write` calls. Ask the **same question** in two separate agent conversations (or with two available models). Save both answers. Compare their checkable claims, including any claim on which they disagree; agreement alone is not evidence.

For at least one important claim, record the exact claim, what each answer says, a link to relevant POSIX/Linux documentation, a focused test and its observed result, and your team's decision: **accept, revise, or reject**. A small standalone test is fine if your library is unfinished. Note any uncertainty the documentation or test cannot resolve. A test demonstrates behavior in its tested conditions; explain when you need a documented rule as well.

Draw a small workflow from question or code change through agent answers, documentation lookup, focused test, and a clearly marked **human decision point**. Show where an accepted change goes next (for example, review and CI) and where a rejected or uncertain claim goes for revision. Bring the two answers, evidence record, test result, and workflow sketch to the final discussion.

## Finish and discuss

Show the instructor your fork's PR, local test results, attempt log, CSV/plot or supplied-data analysis, and a brief explanation of one agent suggestion you accepted or rejected. Mark what you could not verify. For the final architecture discussion, sketch one possible extension, such as a subprocess or an event-driven interface, and identify which new ownership or error cases it would introduce; no implementation is required.
