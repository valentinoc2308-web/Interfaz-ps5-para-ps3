# GTA V PS3 1.27 — validation plan

This checklist is for the user's own NPEB01283 installation after the planned 1.27 update. It does not modify the game.

## Phase 0 — establish a clean baseline
- [ ] Update GTA V through a trusted, legitimate update path.
- [ ] Confirm the game starts and reaches normal gameplay before installing any mod.
- [ ] Confirm title ID NPEB01283 and update 1.27 on the console.
- [ ] Record whether REV or another mod is present.
- [ ] Keep a separate backup of original game data and saves.

## Phase 1 — compatibility inventory
- [ ] List only the specific files a proposed module needs to add or change.
- [ ] Confirm each file's origin and license.
- [ ] Record original file sizes and cryptographic hashes where applicable.
- [ ] Reject files from unknown builds or regions.
- [ ] Do not overwrite files when the target build cannot be identified.

## Phase 2 — small reversible test
- [ ] Start with one small, original-content change.
- [ ] Keep the change isolated and provide a documented removal/restore path.
- [ ] Check boot, loading, a short gameplay session, and save loading.
- [ ] Compare performance and stability against the clean baseline.
- [ ] Remove the test if any crash, black screen, or save issue appears.

## Phase 3 — release gate
A package may be called installable only after:
- [ ] All included files are accounted for and legally distributable.
- [ ] The package targets the verified title ID and update.
- [ ] Install and uninstall/rollback instructions are tested.
- [ ] The package is tested on real PS3 hardware.
- [ ] Known limitations are documented.

## Current result
**Not yet tested.** The 1.27 update is planned, not confirmed installed. This repository currently contains project documentation and planning files, not an installable PKG.
