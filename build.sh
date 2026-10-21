#!/bin/bash

# SPDX-FileCopyrightText: 2023-2026 Stefan Helmert <stefan@entroserv.de>
#
# SPDX-License-Identifier: CERN-OHL-S-2.0

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR/src/mech/spirobrixx/"
OUTPUT_DIR="$SCRIPT_DIR/gen/mech/spirobrixx/"
poetry install
poetry run python3 make.py --output_dir=$OUTPUT_DIR

