# PS3 resource-format research (GTA V)

## Findings that are useful, but not yet a compatibility proof

A published PS3 HUD modification documents two relevant GTA V resource locations:

- `update.rpf/common/data/ui/hudcolor.dat`
- `update.rpf/ps3/patch/data/cdimages/scaleform_generic.rpf` for `.gfx` interface resources.

That publication explicitly labels its PS3 release as game version **1.12**, not 1.27. It is evidence that GTA V on PS3 uses editable HUD colour data and Scaleform/GFX interface resources; it is **not** evidence that the same file paths, resource names, layouts, or binary formats are unchanged in update 1.27.

Source: https://www.gta5-mods.com/misc/pre-release-hud-ps3-1-12

A PS3 GTA V modding-toolkit repository separately documents a workflow involving an update 1.27 working copy of `update.rpf`, a LibertyV RPF editor, a console texture editor, and RASM script tools. This is useful as a lead for the general archive/script toolchain, but its README is not a format specification and does not prove that any particular asset or script works with this project's target title ID and HEN setup.

Source: https://github.com/FranCangelDev/GTA-V-Modding-Files-PS3

## Consequence for this project

The twelve project SVG files are artwork sources only. They cannot be copied into `update.rpf` and expected to render in GTA V. In particular:

- A HUD replacement needs a correctly authored and compiled Scaleform/GFX resource, plus any required supporting data.
- A colour-only HUD change may use `hudcolor.dat`, but that cannot implement a full redesigned HUD.
- Texture replacements need the exact PS3 RAGE texture-dictionary format and verified dimensions, pixel format, mipmap, alpha, and archive metadata.
- The static map SVG is not a GTA V map resource and cannot replace the in-game map/minimap.

## Safe implementation sequence

1. Obtain a user-owned copy of the exact installed NPEB01283 game/update files and verify the update from the console.
2. Inventory the matching `update.rpf` and relevant nested archives without modifying them.
3. Identify the actual HUD/GFX and texture entries in that exact build; record names, sizes, hashes, and archive paths.
4. Establish a round-trip test on a disposable copy: extract one known resource, parse it, rebuild it unchanged, and confirm the archive opens.
5. Only then build one small original HUD test resource. Do not start by replacing every screen.
6. Verify on hardware before expanding to loading, phone, settings, map, or other screens.

## Current status / hard blockers

- Exact installed game update: **not supplied or verified**.
- A 1.27 archive inventory from the user's own NPEB01283 installation: **not supplied**.
- Native Scaleform/GFX authoring and round-trip toolchain: **not integrated or validated in this repository**.
- PS3 texture-dictionary conversion: **not implemented**.
- In-game map implementation: **not implemented**.
- PKG installer and PS3 test: **not implemented / not run**.

No native files should be guessed from a 1.12 tutorial or from a community archive labelled 1.27. Do not overwrite the user's game files. The project must remain clearly marked as a source-artwork prototype until the above evidence exists.
