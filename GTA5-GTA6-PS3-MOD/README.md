# GTA V → GTA VI-inspired Mod (PS3)

**Target:** Grand Theft Auto V, PS3, European digital release **NPEB01283**.  
**Environment:** PS3 Super Slim + HEN.  
**Planned game update:** **1.27** (not yet confirmed installed or tested).  
**Status:** Early source/tooling implementation — **not a playable mod or installable PKG**.

This is an original, compatibility-focused conversion project. It aims to bring selected *ideas and atmosphere* associated with a modern Vice City-era open-world game to GTA V on PS3, while respecting the PS3's memory, CPU, GPU, storage, and modding constraints.

## Current implementation

- Machine-readable target and module manifest: [mod/manifest.json](mod/manifest.json).
- Payload validator with path-safety and SHA-256 checks: [tools/validate_project.py](tools/validate_project.py).
- Regression tests: [tools/test_validate_project.py](tools/test_validate_project.py).
- Original HUD and pause-menu source artwork: [HUD](assets/ui/modern_hud_concept.svg) · [Pause menu](assets/ui/modern_pause_menu.svg), registered in [assets/asset-manifest.json](assets/asset-manifest.json).
- SVG validation and PNG preview build: [tools/validate_assets.py](tools/validate_assets.py), [tools/build_hud_preview.py](tools/build_hud_preview.py).
- Automated Python checks and HUD preview artifact: [.github/workflows/gta5-ps3-mod-checks.yml](../../.github/workflows/gta5-ps3-mod-checks.yml).
- Implementation record: [docs/IMPLEMENTATION-STATUS.md](docs/IMPLEMENTATION-STATUS.md).

The validator checks project files only. It does not modify GTA V, prove game compatibility, or build a PKG.

## Important limits

- A full GTA VI map, complete game systems, proprietary models, textures, audio, missions, or source code cannot be transplanted wholesale into GTA V on PS3.
- No Rockstar game files, copyrighted GTA VI assets, title updates, keys, RAP files, or full game packages are included.
- A working PKG requires testing against the exact installed game build and legally obtained user-owned files.
- This repository will contain original code, configuration, documentation, and assets that can legally be redistributed.

## Planned modules

1. **Foundation & compatibility** — identify the exact GTA V build and safe backup/restore workflow.
2. **Visual refresh** — conservative timecycle, weather, lighting, and original texture replacements where technically feasible.
3. **Vehicles** — a small, tested set of original or properly licensed vehicle assets; no GTA VI model dumps.
4. **World atmosphere** — original signage, props, and location-inspired details sized for PS3.
5. **Gameplay tuning** — handling, traffic/pedestrian tuning, HUD/UI ideas, and configuration where supported by PS3 tools.
6. **Packaging** — reproducible build instructions and PKG only after the mod is validated on NPEB01283.

## Compatibility policy

The target title ID is NPEB01283 and the planned update is 1.27. Neither title ID nor a community archive label proves compatibility: the installed update/build and existing modifications must be checked before any files are installed.

## Safety / installation

Never overwrite the original game without a verified backup. Do not install files made for another title ID or region. Do not use a package if its source or contents are unknown.

See [roadmap](docs/ROADMAP.md), [compatibility notes](docs/COMPATIBILITY.md), [test plan](docs/TEST-PLAN-1.27.md), [asset policy](docs/ASSET-POLICY.md), and [native integration/release gates](docs/INTEGRATION-GATES.md).
