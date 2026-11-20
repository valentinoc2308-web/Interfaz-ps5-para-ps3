# PS3 compatibility baseline

## Confirmed project target
- Platform: PlayStation 3
- Console environment: HEN
- GTA V title ID: **NPEB01283**
- Region: Europe
- Distribution: digital
- Intended update: **1.27 (planned, not yet installed or verified)**

## Status
The user expects to update the game to 1.27 soon but does not know the currently installed version. Therefore 1.27 is the development target, not a confirmed installed build. No binary patch, replacement archive, or installable PKG should be labeled compatible until the console installation is checked.

## Verification checklist (when 1.27 is installed)
1. Confirm the game launches normally before adding the mod.
2. Confirm the title ID is NPEB01283.
3. Confirm the displayed game update/version is 1.27.
4. Record whether REV or any other game modification is installed.
5. Back up the original game data and any files a module may touch.
6. Record hashes for original files before making changes.
7. Test one small, reversible, original-content module at a time.
8. Verify boot, loading, gameplay, save behavior, and rollback before packaging.

## Why this matters
Installations with the same title ID can differ because of updates, modified files, or installed patches. A replacement made for a different build can cause startup failures, black screens, crashes, or damaged game data.

## Performance constraints
PS3 has a strict memory and CPU/GPU budget. Added assets must be small, tested in-game, and measured for loading and frame-time impact. High-resolution PC assets and modern-console assets are not suitable as-is.

## Test record
- Console version: pending
- Title ID on console: pending verification
- Clean launch on target version: not tested
- Mod compatibility: not tested
- Installable PKG: not available
