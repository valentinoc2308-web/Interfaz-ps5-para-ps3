## Project target
GTA V digital Europe, title ID NPEB01283, planned update 1.27, PS3 HEN.

## Artwork and tooling committed
- Project manifest, asset manifest, path/hash/policy validators, regression tests, preview renderer, native integration/release gate specification, PS3 resource-format research, and GitHub Actions workflow definition.
- SVG validator hardened to reject DTD/entity declarations, non-local resource references, external CSS URLs/imports, duplicate registry paths, and invalid/excessive dimensions.
- CSS safety checks are centralized and regression-tested for local SVG fragments, external URL forms, and case-insensitive `@import` declarations.
- Resource research found a published PS3 HUD example using `update.rpf/common/data/ui/hudcolor.dat` and `.gfx` files in `scaleform_generic.rpf`; that example is explicitly for update 1.12, so it is only a lead and does not establish 1.27 compatibility. See [RESOURCE-FORMAT-RESEARCH.md](RESOURCE-FORMAT-RESEARCH.md).
- A public archive catalogue now provides a useful lead: it lists a GTA RE:V 1.27 package with a separate NPEB01283 EBOOT.BIN entry and an update.rpf entry. Its own metadata does not prove the update.rpf is for NPEB01283, nor does it report a hardware test. The files are not being treated as validated project inputs. See the linked source in [RESOURCE-FORMAT-RESEARCH.md](RESOURCE-FORMAT-RESEARCH.md).
- New toolchain research identifies PS3 GTA V texture dictionaries as `.ctd` (`7CSR`, big-endian, zlib), not PC `.ytd`. A candidate editor claims CTD editing/repacking but labels PS3 rebuild experimental and not hardware-confirmed. See [PS3-CTD-TOOLCHAIN.md](PS3-CTD-TOOLCHAIN.md).
- Twelve original 1280×720 SVG interface concepts: driving HUD, pause menu, loading screen, title screen, schematic map, phone, settings, mission briefing, vehicle gallery, save/load, notification cards, and controller interaction prompts.
- All twelve SVG assets are registered as source-only artwork. None is integrated into GTA V, and compatibility with update 1.27 remains unverified.
- The preview renderer reads the asset registry and generates a PNG preview for every registered SVG. These previews are review artifacts only, not PS3 game textures.
- Added a read-only resource inventory utility with regression tests and a Spanish preparation guide. It can list candidate files and hash them, but cannot inspect nested RPF archives or establish the game update version.\n- Added regression tests for the fail-closed PKG release gate, including empty payload, wrong title ID, unverified hardware test, prohibited retail archive, symlink, and missing Makefile target cases.\n- Added a CTD write-safety assessment documenting why PS3 texture-dictionary rebuilding remains blocked until a validated writer, round-trip fixture, and real hardware test exist. See [CTD-WRITE-SAFETY.md](CTD-WRITE-SAFETY.md).\n- Extended the read-only resource inventory to record the first 16 bytes of each candidate file as a hexadecimal fingerprint, with a regression test and updated Spanish instructions. This helps compare candidate headers without parsing or modifying game archives.\n- Hardened the payload manifest validator: it now rejects symbolic links in payload paths, requires a real distribution-policy object, and validates SHA-256 as exactly 64 hexadecimal characters. Added a regression test for symlink rejection.

## What the screens mean
The map SVG is a schematic interface mockup. It is not a recreation of the real San Andreas map, contains no game geography, and is not navigable. The loading, title, phone, settings, briefing, gallery, save/load, notification, interaction-prompt, HUD, and pause-menu SVGs are static concept artwork; they do not respond to controller input or load live game data.

## Still required for a complete cosmetic mod
1. Confirm the installed GTA V build and exact update 1.27 state for NPEB01283.
2. Determine and validate the actual PS3-compatible texture/UI resource formats and archive layout for that exact build. In particular, verify a CTD extract/rebuild round-trip; the available candidate tool's PS3 write path is experimental.
3. Convert approved original artwork into correctly sized and encoded resources.
4. Design a real in-game map/minimap presentation using permitted original assets; a static mockup is not enough.
5. Integrate screens into the correct game UI resources while preserving a rollback copy.
6. Build a distributable package containing only original mod files and a safe installer/manifest; never bundle the game, title update, keys, RAP/RIF, or copyrighted Rockstar assets.
7. Run automated validation and test installation, boot, menus, map, loading, and gameplay on actual PS3 HEN hardware.

## Explicitly not completed
No game archive has been patched. No native PS3 UI resource has been built. No actual San Andreas map replacement exists. No installer or PKG exists. No compatibility or hardware test has passed. The GitHub Actions workflow is configured to compile-check the new PKG gate and its regression tests, but its execution result has not been verified here.

## Release gate
Do not label the project playable, installable, compatible, or complete until the exact target build is verified, all payload resources pass validation, and the package is tested on real PS3 hardware. The current repository is an artwork/tooling prototype, not the finished mod.

- Follow-up research (2026-11-20) inspected the RAGE Console Texture Editor Python port: it documents PS3 CTD read/edit/repack support, but explicitly marks PS3 rebuild experimental and not hardware-confirmed. Its RPF browser also depends on a user-supplied key for encrypted archives. This is now recorded as a candidate for a disposable unchanged round-trip test, not a validated build dependency. See [RESOURCE-FORMAT-RESEARCH.md](RESOURCE-FORMAT-RESEARCH.md).
- Follow-up research inspected a public PS3 GTA V tool collection documenting a Windows workflow with LibertyV, console texture editing, RASM/ASM tools, and an update 1.27 working copy. This is a discovery reference only; it does not prove NPEB01283 compatibility or provide a tested integration for this project.
- Clarified that PS3DEV/PSL1GHT can build native PS3 homebrew packages, but does not itself convert the SVG artwork into GTA V resources or define a valid GTA V installation payload.

- Checked a second public PS3 HUD release and its author discussion. The downloadable PS3 variant is explicitly 1.12; the author said a 1.27 PS3 build was not being made at that time, and reported testing only in RPCS3. Its documented paths (`hudcolor.dat` and `.gfx` inside `scaleform_generic.rpf`) are useful research leads, not a safe drop-in for this project's 1.27 target or proof of real-console compatibility. See [RESOURCE-FORMAT-RESEARCH.md](RESOURCE-FORMAT-RESEARCH.md).
- Confirmed the original GTA V Console Texture Editor README lists PS3 CTD/CSF and unpacked GFX/SYS support, while warning replacement textures must retain original parameters. This is a candidate resource editor, not a compiler for all the project's new UI screens.
- The user's willingness to perform the final PS3 test means the assistant does not need to claim a hardware test. It does not remove the requirement to create actual native resource files and a valid install payload first. The PKG gate remains closed until those exist; no experimental PKG has been fabricated from the SVG mockups.

- Added an automated RGBA8 export stage: CI now renders the original SVGs to PNG, exports deterministic row-major RGBA pixel buffers with dimensions and SHA-256 metadata, and uploads them as build artifacts. These are usable pixel-source intermediates for future native conversion, not CTD/CSF/GFX resources and not installable game files. See `tools/export_texture_sources.py`.
