# PS3 CTD toolchain research

## Platform distinction

GTA V PS3 texture dictionaries use the console-specific `.ctd` resource format, not the PC `.ytd` format. The candidate RAGE Console Texture Editor documents:

| Platform | Extension | Magic | Endianness | Compression |
|---|---|---|---|---|
| PC | `.ytd` | `RSC7` | Little-endian | zlib / raw DEFLATE |
| PS3 | `.ctd` | `7CSR` | Big-endian | zlib |
| Xbox 360 | `.xtd` | `7CSR` | Big-endian | LZX / XMem |

Source: https://github.com/SoLjAhh/RAGE-Console-Texture-Editor-Python-Port-

## Candidate editor: promising, not yet approved

The editor README claims support for opening CTD files and PS3 RPF7 archives, previewing textures, replacing/adding/removing textures, changing formats, generating mipmaps, and saving/repacking.

Important limitation stated by the project itself: PS3 CTD conversion and rebuild are experimental. The author says the structures are internally consistent but RSX GPU behaviour has not been confirmed in-game on PS3 hardware. Therefore this is a candidate for an isolated proof-of-concept, not a verified dependency or a guarantee that a PS3 texture replacement will work.

A separate toolkit lists GTA V PS3 CTD support as read-only, which confirms that write support differs between tools and must not be assumed:
https://github.com/Hancapo/texfury

## Separate archive/script toolchain lead

A PS3 GTA V toolkit README describes a Windows workflow with a LibertyV RPF editor, console texture editor, RASM decompiler/compiler, script assembler, and an update 1.27 working copy. It lists PS3 HEN/CFW and update 1.27 as requirements. This is a lead only; its README does not prove compatibility with the user's exact NPEB01283 installation:
https://github.com/FranCangelDev/GTA-V-Modding-Files-PS3

## What this means for our mod

- The SVG concepts cannot be copied into an RPF and rendered by the game.
- A texture-only replacement requires a valid PS3 CTD texture dictionary with the correct dimensions, format, mipmaps, alpha, compression, and archive metadata.
- Texture editing alone cannot replace Scaleform/GFX logic or create new controller-driven menus.
- The old PS3 HUD example references update 1.12, so its paths cannot be treated as proven for update 1.27. See [RESOURCE-FORMAT-RESEARCH.md](RESOURCE-FORMAT-RESEARCH.md).

## Next engineering gate

Before changing any game file:

1. Verify the exact installed title ID and update on the user's own console.
2. Obtain a user-owned copy of the matching update archive and inventory its UI and CTD entries.
3. On a disposable copy, extract one known CTD, parse it, save it unchanged, and compare its structure and hash behaviour.
4. Only after a successful round-trip, replace one small, non-critical texture with original artwork and verify the rebuilt resource offline.
5. Test the isolated change on PS3 hardware before claiming compatibility.

No game archive, CTD, Scaleform resource, installer, or PKG has been built by this project yet. No hardware test has passed.
