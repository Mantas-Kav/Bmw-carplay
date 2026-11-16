# BMW CarPlay Research

Research into BMW NBT EVO CarPlay compatibility and FSC licensing.

## First milestone

A read-only binary inspector for locally obtained, authorized research samples.

Run:

```bash
python inspector.py sample.bin
```

This tool reports file size, SHA-256, a hex preview, and printable strings. It does not verify BMW signatures, generate FSC licenses, unlock CarPlay, or modify a head unit.

Do not commit customer VINs, private keys, or proprietary activation packages.

## Roadmap

- [x] Create repository
- [x] Add read-only binary inspector
- [ ] Add synthetic test samples and automated tests
- [ ] Research documented FSC structures and head-unit compatibility
- [ ] Evaluate lawful licensing and installation methods
