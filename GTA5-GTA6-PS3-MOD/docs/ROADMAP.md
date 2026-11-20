# Roadmap

This is a staged project. A feature is not complete until its files exist, its compatibility is documented, and it has passed the relevant tests.

## Phase 0 — Establish the target
- [x] Record target platform: PS3 HEN.
- [x] Record target title ID: NPEB01283 (European digital).
- [ ] Confirm the exact GTA V update/build installed on the console.
- [ ] Record free disk space and current installed mods.
- [ ] Establish a backup and rollback procedure.

## Phase 1 — Technical baseline
- [ ] Identify the game's supported file formats and archive layout for this exact build.
- [ ] Verify which modding/editing tools can safely handle the target files.
- [ ] Create a manifest of original files and hashes before changes.
- [ ] Build a clean, reversible test package containing no game content.

## Phase 2 — First playable conversion modules
- [ ] Original visual/timecycle configuration, if supported by the target build.
- [ ] One small original or licensed vehicle asset, only after format and memory tests.
- [ ] One small world-detail/prop asset, only after format and memory tests.
- [ ] Conservative handling and traffic tuning where supported.
- [ ] Test boot, loading, gameplay stability, and rollback after each module.

## Phase 3 — Expansion
- [ ] Additional compatible vehicles and world details.
- [ ] Weather/lighting variants.
- [ ] Original UI/audio additions where formats and licenses permit.
- [ ] Performance profiling and asset-size budgets.

## Phase 4 — Release candidate
- [ ] Clean-install test on NPEB01283.
- [ ] Upgrade/update compatibility check.
- [ ] HEN installation and uninstall test.
- [ ] Hash manifest and release notes.
- [ ] PKG generation only after all prior checks pass.

## Out of scope
A literal port of GTA VI, its complete map, proprietary assets, source code, or online services. PS3 hardware cannot reproduce the full modern GTA VI experience.
