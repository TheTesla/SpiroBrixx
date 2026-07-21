#!/bin/bash

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR/src/mech/spirobrixx/"
OUTPUT_DIR="$SCRIPT_DIR/gen/mech/spirobrixx/"
poetry install
poetry run python3 make.py --output_dir=$OUTPUT_DIR

