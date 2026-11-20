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
