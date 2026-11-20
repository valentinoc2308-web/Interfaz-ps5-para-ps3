# Native integration and release gates

This document defines the evidence required before the visual concepts can be called an in-game mod.

## Current verified scope

- Target declaration: PS3 HEN, European digital GTA V title ID NPEB01283.
- Planned update: 1.27; the installed console build has not been verified.
- Twelve original 1280×720 SVG interface concepts are registered as source artwork.
- Automated source validation and preview generation are configured in GitHub Actions.
- The SVGs are not native PS3 textures, game UI resources, or working in-game screens.

## Required evidence before native conversion

1. A clean, user-owned copy of the exact game installation and confirmed title ID.
2. The installed update/build identified from the console, not inferred from a filename or community archive label.
3. A documented inventory of the exact UI/resource files used by that build.
4. Verified documentation or tool output for each resource's encoding, dimensions, palette/alpha behavior, compression, and archive constraints.
5. A reversible test fixture made only from original project artwork.
6. A successful parse/round-trip check for each converted resource before any game file is touched.

If any of these are missing, conversion must stop rather than guess a file format or overwrite an archive.

## Integration order

1. Choose one small, non-critical screen element.
2. Convert only original artwork to a format proven compatible with the target resource.
3. Validate dimensions, encoding, alpha, file size, and archive structure.
4. Stage the replacement outside the game directory and record hashes.
5. Preserve an untouched backup and a documented rollback route.
6. Test boot, loading, menu navigation, save loading, and a short offline session.
7. Repeat for another element only after the first passes.

The map concept is a static schematic mockup; it is not a real San Andreas map and cannot be treated as a working map replacement. A functional map requires a separate, compatible map/minimap implementation and its own test gate.

## Package release gate

A PKG must not be generated or advertised as installable until all of the following are true:

- The target update and title ID are confirmed.
- Every included file is original or properly licensed.
- No Rockstar game data, title update, executable, key, RAP/RIF, or other user license material is included.
- The package metadata and install destination are verified for the target.
- Install, launch, uninstall, and rollback have been tested on PS3 HEN hardware.
- The release includes a file manifest, hashes, limitations, and test results.

A source ZIP, SVG preview, GitHub Actions artifact, or empty package skeleton is not an installable game mod.

## Current blockers

- Exact installed update/build: unverified.
- Native UI/archive resource layout: not identified.
- Native texture conversion: not implemented or tested.
- In-game map implementation: absent.
- Game integration: absent.
- PKG installer: absent.
- Real-console validation: not performed.

These are genuine technical dependencies, not paperwork that can be marked complete without evidence.
