# Roadmap

A feature is not complete until its files exist, compatibility is documented, and relevant tests have passed. The project targets GTA V PS3 NPEB01283 with update 1.27 planned, not yet verified on-console.

## Phase 0 — Establish the target
- [x] Record target platform: PS3 HEN.
- [x] Record target title ID: NPEB01283 (European digital).
- [x] Record planned update target: 1.27 (not installed/verified yet).
- [ ] Confirm the exact GTA V update/build installed on the console.
- [ ] Record current installed mods and establish a backup/rollback procedure.

## Phase 1 — Technical baseline
- [x] Create a machine-readable project manifest.
- [x] Add payload path and SHA-256 validation tooling.
- [x] Add regression tests for unsafe paths and non-distributable game/package files.
- [x] Add automated Python checks in GitHub Actions.
- [ ] Identify supported file formats and archive layout for the exact installed build.
- [ ] Verify which tools can safely handle the target files.
- [ ] Record hashes of user-owned original files before any changes.
- [ ] Complete a reversible test package containing no game content.

## Phase 2 — First playable conversion modules
- [ ] Original visual/timecycle configuration, if supported by the target build.
- [x] Create original HUD and pause-menu interface source artwork with automated previews.
- [ ] Convert interface artwork to a verified PS3-supported texture format and test it in-game.
- [ ] One small original or licensed cosmetic vehicle asset, only after format and memory tests.
- [ ] One small world-detail/prop asset, only after format and memory tests.
- [ ] Conservative handling and traffic tuning where supported.
- [ ] Test boot, loading, gameplay stability, and rollback after each module.

## Phase 3 — Expansion
- [ ] Additional compatible cosmetic vehicles and world details.
- [ ] Weather/lighting variants.
- [ ] Original UI/audio additions where formats and licenses permit.
- [ ] Performance profiling and asset-size budgets.

## Phase 4 — Release candidate
- [ ] Clean-install test on NPEB01283 / update 1.27.
- [ ] Upgrade/update compatibility check.
- [ ] HEN installation and uninstall test.
- [ ] Hash manifest and release notes.
- [ ] PKG generation only after all prior checks pass.

## Out of scope
A literal port of GTA VI, its complete map, proprietary assets, source code, or online services. PS3 hardware cannot reproduce the full modern GTA VI experience. The project is limited to original/licensed offline cosmetic and presentation changes.
