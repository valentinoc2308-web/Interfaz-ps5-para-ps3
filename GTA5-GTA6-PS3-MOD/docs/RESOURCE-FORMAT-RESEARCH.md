# PS3 resource-format research (GTA V)

## Findings that are useful, but not yet a compatibility proof

A published PS3 HUD modification documents two relevant GTA V resource locations:

- `update.rpf/common/data/ui/hudcolor.dat`
- `update.rpf/ps3/patch/data/cdimages/scaleform_generic.rpf` for `.gfx` interface resources.

That publication explicitly labels its PS3 release as game version **1.12**, not 1.27. It is evidence that GTA V on PS3 uses editable HUD colour data and Scaleform/GFX interface resources; it is **not** evidence that the same file paths, resource names, layouts, or binary formats are unchanged in update 1.27.

Source: https://www.gta5-mods.com/misc/pre-release-hud-ps3-1-12

A PS3 GTA V modding-toolkit repository documents a workflow involving an update 1.27 working copy of `update.rpf`, a LibertyV RPF editor, a console texture editor, and RASM script tools. It is useful as a lead for the general archive/script toolchain, but its README does not prove that any particular asset or script works with this project's target title ID and HEN setup.

Source: https://github.com/FranCangelDev/GTA-V-Modding-Files-PS3

## Newly identified texture-editor candidate

The public RAGE Console Texture Editor Python port advertises direct reading and editing of PS3 `.ctd` texture dictionaries, RPF7 browsing, texture replacement, mipmap generation, and repacking. It documents PS3 CTD as big-endian with zlib compression.

Critical caveat: the same project explicitly labels PS3 CTD conversion/rebuild as **experimental** and says RSX behaviour has not been confirmed in-game on real PS3 hardware. The project reports some in-game verification on Xbox 360, which must not be mistaken for PS3 verification. This is therefore a candidate for a disposable proof-of-concept only, not a validated dependency or a ready-made solution.

Source: https://github.com/SoLjAhh/RAGE-Console-Texture-Editor-Python-Port-

A separate texture toolkit lists PS3 CTD support as read-only, reinforcing that write support is not universal across tools.

Source: https://github.com/Hancapo/texfury

## Consequence for this project

The twelve project SVG files are artwork sources only. They cannot be copied into `update.rpf` and expected to render in GTA V. In particular:

- A HUD replacement needs a correctly authored and compiled Scaleform/GFX resource, plus any required supporting data.
- A colour-only HUD change may use `hudcolor.dat`, but that cannot implement a full redesigned HUD.
- Texture replacements need the exact PS3 RAGE texture-dictionary format and verified dimensions, pixel format, mipmap, alpha, and archive metadata.
- The static map SVG is not a GTA V map resource and cannot replace the in-game map/minimap.

## Safe implementation sequence

1. Verify the exact installed title ID and game update on the user's own console.
2. Work only from a user-owned copy of the exact matching game/update files; inventory `update.rpf` and relevant nested archives without modifying originals.
3. Identify the actual HUD/GFX and texture entries in that exact build; record names, sizes, hashes, and archive paths.
4. Establish a round-trip test on a disposable copy: extract one known CTD, parse it, save it unchanged, and compare its structure; separately confirm the RPF archive can be reopened.
5. Only after a successful round-trip, build one small original HUD/texture test resource. Do not start by replacing every screen.
6. Verify the isolated change on PS3 hardware before expanding to loading, phone, settings, map, or other screens.

## Current status / hard blockers

- Exact installed game update: **not supplied or verified**.
- A matching archive inventory from the user's own NPEB01283 installation: **not supplied**.
- Native Scaleform/GFX authoring and round-trip toolchain: **not integrated or validated in this repository**.
- PS3 CTD write/rebuild path: **candidate tool identified, but experimental and not hardware-verified**.
- In-game map implementation: **not implemented**.
- PKG installer and PS3 test: **not implemented / not run**.

No native files should be guessed from a 1.12 tutorial or from a community archive labelled 1.27. Do not overwrite the user's game files. The project must remain clearly marked as a source-artwork prototype until the above evidence exists.

## Follow-up: concrete editor and packaging research (2026-11-20)

### RAGE Console Texture Editor Python port

Repository inspected: https://github.com/SoLjAhh/RAGE-Console-Texture-Editor-Python-Port-

The README documents the following capabilities:

- PS3 texture dictionaries use the `.ctd` extension, `7CSR` magic, big-endian fields, and zlib compression.
- The editor claims it can browse PS3/Xbox 360 RPF7 archives, extract entries, open CTDs, replace/add/remove textures, generate mipmaps, and repack dictionaries.
- It supports DXT1, DXT2_3, DXT4_5, DXT5A, DXN, and 8_8_8_8 encodings.
- Encrypted RPF browsing requires a user-supplied key file; the project does not distribute keys.
- Its own verification section explicitly classifies PS3 CTD rebuilding as experimental and not confirmed on PS3 hardware. Its stated in-game verification is primarily Xbox 360; do not transfer that claim to PS3.

This is materially more promising than a read-only extractor, but it does not remove the need for a PS3 round-trip and hardware test. It is not yet approved as a production dependency. A candidate test must use a disposable copy and an unchanged save/reopen comparison before any replacement texture is attempted.

### PS3 GTA V tool collection

Repository inspected: https://github.com/FranCangelDev/GTA-V-Modding-Files-PS3

Its README describes a Windows-based workflow around LibertyV for RPF archives, a console texture editor, RASM script tools, an ASM modloader source, and an update 1.27 working copy. This is a useful tool-discovery index, not a compatibility certificate for NPEB01283. Its README asks users to start from an update 1.27 copy, but does not demonstrate a completed build for this project's exact digital title ID or this user's console.

### PKG toolchain distinction

The PS3DEV/PSL1GHT toolchain is for building native PS3 homebrew executables and packages. Its presence alone does not transform SVG mockups or GTA V UI assets into a game patch. A mod installer package still needs a valid, original install payload and a correctly defined installation target. The project release gate therefore remains in place.

### Practical next experiment (not yet performed)

1. Confirm the installed title ID and update from the console's own game information; do not infer update 1.27 from a mod archive label.
2. Obtain a read-only inventory of the user's own extracted resources, identifying the matching update archive and candidate CTDs/GFX files without sharing proprietary archives.
3. On a separate disposable copy, use the candidate editor to open one CTD and save it unchanged. Reopen it and compare dimensions, texture count, formats, mip counts, and file structure. Record hashes before and after; a changed hash alone is not proof of corruption, so compare parsed structure too.
4. If the unchanged round-trip succeeds, replace one non-critical texture with a small original test graphic while preserving the original texture's dimensions, format, alpha behaviour, and mip structure. Reopen the result in the editor.
5. Only then can a matching RPF integration and PS3 hardware test be considered. Keep the original files and a rollback copy untouched.

No such experiment has been run in this repository: no matching user resource dump has been supplied, and no PS3 hardware test has been performed. Therefore no CTD, GFX, RPF, or PKG is being claimed as built or working.

## Additional public PS3 HUD evidence checked (2026-11-20)

A second public reference, [Pre-Release HUD 1.1](https://www.gta5-mods.com/misc/pre-release-hud-ps3-1-12), provides concrete PS3 install paths for a limited HUD colour / Scaleform replacement:

- `update.rpf/common/data/ui/hudcolor.dat`
- `update.rpf/ps3/patch/data/cdimages/scaleform_generic.rpf` for the relevant `.gfx` files.

Important limitations in the same publication and its discussion:

- The downloadable PS3 build is explicitly version 1.12, not 1.27.
- The author states that a PS3 1.27 version was not being made at that time.
- The author also states the release had only been tested in RPCS3, while a commenter asks whether it is for emulation; therefore it is not evidence of successful real-console installation.
- The documented files are a narrow HUD modification, not a complete replacement for pause, phone, map, title, loading, settings, or mission screens.

The original [GTA V Console Texture Editor](https://github.com/SamuelCFW/GTA-V-Console-Texture-Editor) README separately lists PS3 support for `.ctd`, `.chm`, `.csf`, and unpacked `.gfx` / `.sys` resources, and warns that replacement textures must retain the original parameters. This supports using the tool as a format inspection/editing candidate, but does not establish that arbitrary new full-screen UI resources can be authored or that the user's installed update accepts them.

### Decision for this project

Do not copy the 1.12 HUD files into the planned 1.27 package. Do not use an RPCS3-only result as a real-PS3 compatibility claim. The sensible first target is a single small, reversible HUD element in the exact user's build; only after that works should the project expand to other screens. The user's willingness to perform the final console test can remove the requirement for the assistant to personally test hardware, but it cannot replace the need to produce a correctly formatted native resource and a reproducible install payload.
