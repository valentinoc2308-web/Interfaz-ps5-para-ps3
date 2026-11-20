# PS3 compatibility baseline

## Confirmed target
- Platform: PlayStation 3
- Console environment: HEN
- GTA V title ID: **NPEB01283**
- Region: Europe
- Distribution: digital

## Still required before building installable files
1. Exact GTA V update version/build shown by the console.
2. Whether the game is currently clean or has REV/other modifications installed.
3. A verified backup of the files that a module intends to replace.
4. Hashes of original files to detect mismatches and support restoration.

## Why this matters
Two installations with the same title ID may differ because of updates, modified files, or installed patches. A file replacement made for a different build can cause startup failures, black screens, crashes, or corrupted game data.

## Performance constraints
PS3 has a strict memory and CPU/GPU budget. Every added asset must be small, tested in-game, and measured for loading and frame-time impact. High-resolution PC assets and modern console assets are not suitable as-is.

## Test record
No in-console compatibility test has been performed by this repository yet. Do not interpret the target declaration as a successful compatibility test.
