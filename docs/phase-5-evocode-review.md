# Phase 5 — offline evaluation of evocode FSC code

Reviewed upstream repository: https://github.com/FreZZZeR/evocode
Reviewed source: `evocode/fsc.py`, `tests/test_anchors.py`, `pyproject.toml`, README.
Review date: 2026-11-16.

## Direct source observations

- `fsc.py` declares a **60-byte body** and **128-byte signature** (188 bytes total).
- `build_body` stores a two-byte application number at offsets 2–3, big-endian, and upgrade index at offsets 4–5.
- `parse` exposes version, application, upgrade index, FSC ID, VIN and creation date.
- `verify` checks an RSA e=3 / MD5 PKCS#1 v1.5 envelope against a supplied modulus; it is not proof that a particular BMW unit trusts that modulus.
- `test_anchors.py` contains four synthetic tests for multiple candidate trust anchors, identifying the matching anchor, modulus recovery, and absent-anchor behavior.
- Upstream package declares Apache-2.0 and a standard-library-only core; optional extras have dependencies.
- Upstream README says FSC on-car application is **not yet validated on a live head unit**.

## Our independent offline experiment

`fsc_layout.py` reads **exactly 188 bytes**, extracts only non-sensitive fields from the upstream-described layout, and explicitly reports that no signature or vehicle compatibility has been verified. It does not depend on, execute, or copy upstream signing code.

`tests/test_fsc_layout.py` uses synthetic data only. Passing tests validate our parser's handling of that example layout, **not** authenticity or applicability to genuine BMW FSC files.

## Code review risks

1. The upstream `parse` function does not first enforce a minimum/expected FSC length, so short inputs may yield partial values or an unpacking exception.
2. The upstream `verify` function indexes into the decoded envelope without complete defensive bounds checks; malformed inputs deserve separate robustness tests.
3. The upstream anchor tests generate keys and sign synthetic files; this is not independent verification on physical NBT EVO hardware.
4. The trust-anchor modification and firmware-writing paths present high vehicle-bricking and authorization risks and are outside this offline assessment.
5. An Apache-2.0 source license does not grant rights to BMW firmware or remove contractual, regulatory, or trademark concerns.

## Decision

**Offline FSC layout analysis is feasible. Independent commercial CarPlay activation is still unproven.** Next validation requires an authorized sample and a hardware/firmware test plan with recovery safeguards. Do not ship a generator or promise activation to customers.
