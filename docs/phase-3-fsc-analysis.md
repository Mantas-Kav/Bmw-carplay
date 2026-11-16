# Phase 3 — evidence-driven FSC file triage

## Source findings

BMW's ISTA/P documentation describes an FSC import package with an XML enabling-code file and a DER certificate file. It explicitly says importing is not itself activation; activation occurs later in the measures plan. **This documentation is older and does not establish the internal NBT EVO FSC format.**

- ISTA/P manual: https://www.manuallib.com/download/2023-10-15/BMW%20Group%20Online%20Service%20System%20ISTA%20P%20User%20Manual.pdf

A community E-Sys guide distinguishes NBT `0xDE` and NBT EVO `0xF0` extraction identifiers; these are navigation-related extraction examples, **not** proof of CarPlay FSC format.

- https://git.davidpetric.com/thepetric/BMW_coding/raw/commit/b49e627f9c222e366f5c8faefa94e728f4549afa/guides/BMW_FSC_Certificate_Extraction_Guide.pdf

Public reverse-engineering research states that NBT EVO FSC authorization relies on verification against an embedded public-key trust anchor. Replacing that trust anchor is distinct from obtaining a BMW-signed license and has technical/legal/warranty implications. We do **not** implement firmware modifications.

- https://github.com/vandelayautollc/nbt-evo-reversing
- https://github.com/FreZZZeR/evocode

## Implemented

`fsc_inspector.py` provides **read-only, offline, bounded** identification of XML, DER candidates, ZIP containers, and opaque `.fsc` or `.sig` candidates. It intentionally does not print VINs, parse undocumented fields, verify signatures, or claim activation capability.

Usage (when a permitted sample becomes available):

```sh
python fsc_inspector.py path/to/sample.fsc
```

The file is read locally and not uploaded. Do not commit any customer-specific or proprietary samples to the public repository.

## Status

- Format identification: preliminary, based on extensions and basic signatures
- Real FSC parsing: **blocked until a lawful, redistributable sample and documented layout are available**
- BMW cryptographic signature verification: **not implemented**
- FSC generation/activation: **not implemented**
- Hardware validation: **not performed**

## Decision gate

A commercial product needs a lawful license source or a separately evaluated, authorized integration model. A self-signed FSC will not be accepted by a unit still trusting BMW's original key. Before vehicle testing, evaluate legal rights, recovery equipment, and the risks of modifying the unit's trust store.
