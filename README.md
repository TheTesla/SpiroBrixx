# SpiroBrixx Construction System

*Deutsche Version: [README.de.md](README.de.md)*

[![REUSE Compliance](https://github.com/TheTesla/SpiroBrixx/actions/workflows/reuse.yml/badge.svg)](https://github.com/TheTesla/SpiroBrixx/actions/workflows/reuse.yml)
[![License: CERN-OHL-S-2.0](https://img.shields.io/badge/License-CERN--OHL--S--2.0-blue.svg)](LICENSE)

![SpiroBrixx logo](doc/media/SpiroBrixxLogo/SpiroBrixxLogo.png)

The _SpiroBrixx_ building blocks enable makers, scientists and artists to prototype their mechanical engineering and lab projects in minutes.

_Cube-shaped blocks with four-start internal threads running parallel to all three spatial axes are screwed together at 90° steps without clearance. Because both joined parts carry internal threads, the connection is form-fit rather than friction-fit — it withstands high tensile loads and can be assembled and disassembled non-destructively with a screwdriver, no cutting, no dedicated tools._ A longer description of the motivation and design rationale is available in the [concept document](doc/src/SpiroBrixxKonzept.md) (German).

![A red SpiroBrixx screwbar with internal thread sockets on multiple faces](doc/media/photos_no_bg/IMG_20240107_144104.png)

## Prerequisites

* [Poetry](https://python-poetry.org/) (dependency management)
* Python 3.11+

## Build and Make

Just run:

```bash
./build.sh
```

This installs the Python dependencies and generates the 3D printable STL (or OBJ) files in `gen/mech/spirobrixx/`. The set of generated parts and the profile used are configured in `src/mech/spirobrixx/make.py`. Remove all generated files with:

```bash
./clean.sh
```

## Printing

Recommended print parameters:

* Material: PETG
* Dry the material at least 24 h before printing.
* Nozzle: 0.4 mm
* Inner perimeter: 0.8 mm
* Infill: 0.8 mm
* Standard values for all other parameters
* Short hot water annealing after printing: submerge the part in hot water (just below boiling) for a few minutes, then let it cool down slowly. This relieves internal print stresses.

## License

SpiroBrixx is licensed under the **CERN Open Hardware Licence Version 2 - Strongly Reciprocal (CERN-OHL-S-2.0)** — see [LICENSE](LICENSE) and [LICENSES/CERN-OHL-S-2.0.txt](LICENSES/CERN-OHL-S-2.0.txt).

This source describes Open Hardware and is licensed under the CERN-OHL-S v2.
You may redistribute and modify this source and make products using it under
the terms of the CERN-OHL-S v2. This source is distributed WITHOUT ANY EXPRESS
OR IMPLIED WARRANTY, INCLUDING OF MERCHANTABILITY, SATISFACTORY QUALITY AND
FITNESS FOR A PARTICULAR PURPOSE. Please see the CERN-OHL-S v2 for applicable
conditions.
