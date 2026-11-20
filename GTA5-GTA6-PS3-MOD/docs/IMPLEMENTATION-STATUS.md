## Project target
GTA V digital Europe, title ID NPEB01283, planned update 1.27, PS3 HEN.

## Artwork and tooling committed
- Project manifest, asset manifest, path/hash/policy validators, regression tests, preview renderer, native integration/release gate specification, PS3 resource-format research, and GitHub Actions workflow definition.
- SVG validator hardened to reject DTD/entity declarations, non-local resource references, external CSS URLs/imports, duplicate registry paths, and invalid/excessive dimensions.
- CSS safety checks are centralized and regression-tested for local SVG fragments, external URL forms, and case-insensitive `@import` declarations.
- Resource research found a published PS3 HUD example using `update.rpf/common/data/ui/hudcolor.dat` and `.gfx` files in `scaleform_generic.rpf`; that example is explicitly for update 1.12, so it is only a lead and does not establish 1.27 compatibility. See [RESOURCE-FORMAT-RESEARCH.md](RESOURCE-FORMAT-RESEARCH.md).
- Twelve original 1280×720 SVG interface concepts: driving HUD, pause menu, loading screen, title screen, schematic map, phone, settings, mission briefing, vehicle gallery, save/load, notification cards, and controller interaction prompts.
- All twelve SVG assets are registered as source-only artwork. None is integrated into GTA V, and compatibility with update 1.27 remains unverified.
- The preview renderer reads the asset registry and generates a PNG preview for every registered SVG. These previews are review artifacts only, not PS3 game textures.

## What the screens mean
The map SVG is a schematic interface mockup. It is not a recreation of the real San Andreas map, contains no game geography, and is not navigable. The loading, title, phone, settings, briefing, gallery, save/load, notification, interaction-prompt, HUD, and pause-menu SVGs are static concept artwork; they do not respond to controller input or load live game data.

## Still required for a complete cosmetic mod
1. Confirm the installed GTA V build and exact update 1.27 state for NPEB01283.
2. Determine and validate the actual PS3-compatible texture/UI resource formats and archive layout for that exact build.
3. Convert approved original artwork into correctly sized and encoded resources.
4. Design a real in-game map/minimap presentation using permitted original assets; a static mockup is not enough.
5. Integrate screens into the correct game UI resources while preserving a rollback copy.
6. Build a distributable package containing only original mod files and a safe installer/manifest; never bundle the game, title update, keys, RAP/RIF, or copyrighted Rockstar assets.
7. Run automated validation and test installation, boot, menus, map, loading, and gameplay on actual PS3 HEN hardware.

## Explicitly not completed
No game archive has been patched. No native PS3 UI resource has been built. No actual San Andreas map replacement exists. No installer or PKG exists. No compatibility or hardware test has passed. The GitHub Actions workflow is configured in the repository, but its execution result has not been verified here.

## Release gate
Do not label the project playable, installable, compatible, or complete until the exact target build is verified, all payload resources pass validation, and the package is tested on real PS3 hardware. The current repository is an artwork/tooling prototype, not the finished mod.
