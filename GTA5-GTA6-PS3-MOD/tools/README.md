# Build and validation tools

## Implemented

- `validate_project.py`: checks the project manifest, target declaration, distribution policy, payload paths, and SHA-256 hashes.
- `test_validate_project.py`: regression tests for safe paths and blocked game/package file types.
- `validate_assets.py`: validates all registered original SVG interface artwork, dimensions, asset IDs, paths, and source-only status.
- `test_validate_assets.py`: regression tests for every registered SVG and the asset registry.
- `build_hud_preview.py`: renders every registered SVG into PNG previews and verifies PNG signatures and dimensions.

Run from this directory:

```sh
python -m unittest -v
python validate_project.py
python validate_assets.py
python -m pip install CairoSVG
python build_hud_preview.py
```

The PNG previews are design artifacts only. They are not converted to the PS3-native texture format and are not installed in GTA V.

## Not implemented yet

No game archive patcher, PS3 script compiler integration, HEN installer, or PKG-generation tool is included. Those steps must not be guessed: first verify the exact NPEB01283 update/build and the file formats used by that build.

Any future integration tool must:
- preserve untouched files;
- create a manifest and hashes;
- reject mismatched title IDs/builds;
- stage changes outside the original game directory;
- support rollback;
- never bundle copyrighted Rockstar game data or license files.

A PKG must not be advertised as installable until it has been built and tested on a PS3 HEN console with the target game.

- `inventory_game_resources.py`: read-only inventory of already-extracted user-owned game/update folders. Lists candidate RPF, CTD, GFX and HUD-colour files with sizes and optional SHA-256; never reads archive contents or changes files.
- `test_inventory_game_resources.py`: regression tests for candidate discovery and hash options.

To inventory an extracted copy (from this directory):

```sh
python inventory_game_resources.py /path/to/your/extracted/update -o resource-inventory.json
```

The report contains metadata only. A filename/hash does not prove title ID or update compatibility. Do not upload or publish game archives; if asking for help, share only the JSON metadata report.
