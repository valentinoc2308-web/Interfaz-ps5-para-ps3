# Build tools

No binary build or PKG-generation script is included yet.

The first tool added here must be selected only after the exact NPEB01283 game build and file formats are verified. Tooling must:
- preserve untouched files;
- create a manifest and hashes;
- reject mismatched title IDs/builds;
- stage changes outside the original game directory;
- support rollback;
- never bundle copyrighted Rockstar game data or license files.

A PKG must not be advertised as installable until it has been built and tested on a PS3 HEN console with the target game.
