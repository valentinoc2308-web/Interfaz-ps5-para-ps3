# Native PKG integration contract

The dedicated release workflow is `.github/workflows/gta5-ps3-mod-pkg.yml`.
It reuses the PS3DEV/PSL1GHT toolchain approach, but it is separate from the
Nova Launcher workflow and does not pretend that SVG artwork is a game mod.

## Required integration inputs

Before a real PKG can be produced, this directory must contain:

- `Makefile`: a native PS3 integration/build project with a `pkg` target.
- `COMPATIBILITY.json`: evidence for NPEB01283 / Europe / update 1.27, a
  successful native-resource round trip, a passed hardware test, and rollback.
- `PKGFILES/`: only original or properly licensed installable mod resources.

The workflow checks these gates before installing the SDK. If they are absent,
it stops and does not publish a fake PKG.

## Current state

These inputs are intentionally not fabricated. The repository currently has
source SVG concepts and research tools, not verified native GTA V resources.
The package workflow is therefore expected to stop at its first gate until the
real integration is supplied and tested.

Never put a retail GTA V EBOOT, update archive, license, RAP/RIF, act.dat,
IDPS, or proprietary Rockstar assets in this repository or generated artifact.
