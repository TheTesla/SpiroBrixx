#!/bin/bash

# SPDX-FileCopyrightText: 2023-2026 Stefan Helmert <stefan@entroserv.de>
#
# SPDX-License-Identifier: CERN-OHL-S-2.0

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

rm -rf "$SCRIPT_DIR/gen/"
