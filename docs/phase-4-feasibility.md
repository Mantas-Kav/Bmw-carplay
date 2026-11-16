# Phase 4 — FSC feasibility and open-source landscape

Research date: 2026-11-16. This document separates published claims from independently verified behavior.

## Most relevant public projects

### evocode
https://github.com/FreZZZeR/evocode

- Scope: NBT EVO QNX ID4/ID5/ID6, not MGU.
- Maintainers report offline FSC cryptographic functions proven against real data.
- Maintainers explicitly state FSC on-car apply/read/disable routines have **not** been validated on a live head unit.
- Firmware/trust-anchor replacement is a separate high-risk operation.
- Review license, provenance, dependencies, and test data before reuse. We have not audited the implementation.

### NBT EVO reversing
https://github.com/vandelayautollc/nbt-evo-reversing

- Explains distinction between BMW-signed FSC and changing the trusted verification key.
- Describes head-unit bricking risk if modifying live firmware.
- Research notes are not a safe production installation procedure.

### BMW ISTA/P manual
https://www.manuallib.com/download/2023-10-15/BMW%20Group%20Online%20Service%20System%20ISTA%20P%20User%20Manual.pdf

- Older BMW documentation describes XML enabling-code and DER certificate import packages.
- This is **not** evidence that raw NBT EVO CarPlay FSC files have the same format.
- Importing a package is distinct from activating the feature.

### BMW component-protection bulletin
https://static.nhtsa.gov/odi/tsbs/2018/MC-10136310-9999.pdf

- Trusted VIN/component protection can invalidate FSC authorizations after head-unit/BDC swapping.
- Avoid swapping vehicle modules to experiment.

## Approach comparison

| Approach | Potential | Fundamental obstacle | Current status |
| --- | --- | --- | --- |
| Officially authorized FSC | Legitimate feature enablement | Access, pricing, eligibility | No supplier agreement |
| Independent offline FSC analysis | Read and classify permitted samples | Format validation and representative samples | Preliminary classifier built |
| Owner-controlled CA / modified trust anchor | Third-party research suggests possible | Firmware modification, recovery, legal and customer risk | Not validated by us |
| Coding only | May enable display options on already-authorized systems | Does not create FSC authorization | Not a standalone activation solution |

## Feasibility decision

Do **not** market or sell an independent activation generator yet. A self-signed file cannot authorize CarPlay on an unmodified unit trusting BMW's key. Published owner-CA research depends on a changed trust anchor, which is a distinct high-risk operation.

Next work:
1. Review the license and source quality of evocode; decide whether a clean-room implementation is necessary.
2. Build **offline-only** synthetic fixtures and a parser for *documented* fields, without pretending the synthetic format is BMW's.
3. Obtain a lawfully shareable FSC example or an authorized test setup.
4. Design recovery, compatibility, and consent requirements before any write to hardware.
5. Assess official license distribution as an alternative business model.

No proprietary FSC data, customer VINs, or private keys should be committed to this public repository.
