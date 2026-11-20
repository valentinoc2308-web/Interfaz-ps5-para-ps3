# Original interface concept assets

All source assets are original project artwork, 1280×720 SVGs. They are editable design references, not game-ready PS3 textures.

- `modern_hud_concept.svg` — driving HUD concept.
- `modern_pause_menu.svg` — pause/menu concept.
- `loading_screen.svg` — loading-screen concept.
- `title_screen.svg` — title/start-screen concept.
- `map_screen.svg` — schematic map-interface concept only; it is not the real San Andreas map, has no accurate streets/geography, and is not interactive.
- `phone_ui.svg` — phone interface concept.
- `settings_screen.svg` — settings interface concept.
- `mission_briefing.svg` — mission briefing concept.
- `vehicle_gallery.svg` — vehicle category/garage gallery concept.
- `save_load_screen.svg` — save/load slot concept.
- `notification_cards.svg` — objective, message, and point-of-interest notification concepts.
- `interaction_prompts.svg` — contextual controller-button prompt concept.

## Integration status
All twelve files are registered in `assets/asset-manifest.json`. None has been inserted into GTA V or converted into the exact texture/resource formats required by the target PS3 game build. They do not implement controller navigation, game data, a real map, loading logic, or in-game event hooks.

Before integration, the project must verify the exact NPEB01283 game/update build, identify the permitted resource formats and dimensions, convert and validate each asset, and test the result on PS3 hardware. Do not distribute Rockstar game files, title updates, console keys, RAP/RIF files, or third-party copyrighted assets.
