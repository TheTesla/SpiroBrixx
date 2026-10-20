#!/bin/bash
# SPDX-FileCopyrightText: 2023-2026 Stefan Helmert <stefan@entroserv.de>
#
# SPDX-License-Identifier: CERN-OHL-S-2.0


find ~/.venv-default/ -name "*.nbi" | xargs rm
find ~/.venv-default/ -name "*.nbc" | xargs rm

