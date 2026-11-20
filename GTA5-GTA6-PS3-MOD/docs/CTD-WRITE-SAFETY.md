# PS3 CTD write-safety assessment

## Decision

**Do not generate or install replacement CTD files yet.** The repository does not currently contain a validated PS3 CTD writer or a known-good round-trip fixture for the user's exact GTA V build.

## Evidence from public tool documentation

- [RAGE Console Texture Editor Python port](https://github.com/SoLjAhh/RAGE-Console-Texture-Editor-Python-Port-) documents PS3 CTD reading and rebuilding, but explicitly labels PS3 conversion/rebuild experimental and says RSX behaviour has not been confirmed in-game.
- [texfury](https://github.com/Hancapo/texfury) explicitly lists GTA V PS3 CTD as read/extract only and does not support writing that target.
- [GTA V Console Texture Editor source](https://github.com/SamuelCFW/GTA-V-Console-Texture-Editor) lists PS3 CTD support and warns that replacements should retain the original texture parameters.
- [GTA V PS3 modding toolkit collection](https://github.com/FranCangelDev/GTA-V-Modding-Files-PS3) describes a workflow for update 1.27, but its README is a tool collection/how-to, not proof that a particular resource has been rebuilt and tested on this project's NPEB01283 installation.

These references are leads, not a compatibility certification. Their claims must be checked against the exact files and hardware target.

## Safe next technical stage

1. Obtain a read-only inventory from the user's own extracted game resources.
2. Identify the exact title ID and installed update from trusted local metadata; do not infer it from a download page or filename.
3. Select one small, non-critical UI texture dictionary and preserve an untouched backup.
4. Inspect and export it without changing the archive.
5. Only attempt a rebuild after a tool supports PS3 writing and a fixture proves byte-structure round-trip behaviour.
6. Compare the rebuilt resource structurally, preserve original texture dimensions/format/mip parameters, and keep a rollback copy.
7. Test on a separate copy/install on actual PS3 HEN hardware before declaring compatibility.

## Current project boundary

The current SVG screens are original concept artwork, not PS3-native CTD/GFX assets. This repository does not include Rockstar archives, executables, keys, licenses, or retail update files. No CTD has been modified and no game installation should be changed by the current tooling.

## Release rule

A PKG release gate must remain closed until native resources, compatibility metadata, round-trip evidence, rollback evidence, and a real hardware test are available. A successful Python test suite alone cannot establish that a GTA V mod works in-game.
