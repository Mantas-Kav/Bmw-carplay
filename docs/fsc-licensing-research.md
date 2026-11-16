# FSC licensing research — Phase 2

## Confirmed findings

BMW service bulletin SI B65 13 16 describes NBT EVO (HU-H2) component protection, also called **Trusted VIN**. If a head unit or BDC is swapped into another vehicle, a VIN mismatch can trigger component protection and cancel FSC/SWT enable codes.

Primary source: https://static.nhtsa.gov/odi/tsbs/2018/MC-10142941-9999.pdf

The NBT EVO Apple CarPlay FSC application identifier is commonly documented as `0x0143`. This is an application identifier, **not** a signing key, a usable activation file, or proof that a car can be activated.

Community reference: https://car1337.com/threads/bmw-fsc-code-number-list-and-their-description.134/

## Working model (research hypothesis, not verified internal specification)

1. Feature authorization data identifies a permitted application.
2. Vehicle/head-unit identity and other metadata may constrain validity.
3. Cryptographic validation may determine whether authorization is accepted.
4. Installation transports the data to the unit; transport does not create authorization.

Do not assume a publicly described FSC file format fully specifies BMW's cryptographic verification.

## FSC vs USB installation packages

- FSC: feature-enabling authorization data, subject to validity checks.
- USB `.bin` file: generic filename extension; content could be an installer, data, or another format.
- ENET: communication path for head-unit operations, not a license issuer.
- Patches: modifications to validation behavior are different from manufacturer-authorized FSC issuance.

## Research plan

- [x] Record primary-source evidence for Trusted VIN / component protection.
- [x] Build an offline digital-signature demonstration with a locally generated example key.
- [ ] Locate an authorized, redistributable FSC example or sufficiently documented file structure.
- [ ] Implement **read-only** field parsing with tests, marking unknown fields explicitly.
- [ ] Validate compatibility claims using a consenting test vehicle and a safe, documented procedure.
- [ ] Evaluate whether an independent commercial solution is legally and technically feasible.

## Safety and commercial constraints

Do not place customer VINs, private keys, proprietary installers, or firmware dumps in this public repository. Do not swap head units between vehicles for testing. Do not run unknown USB installers on customer cars. A self-signed demonstration signature is **not** recognized by BMW.
