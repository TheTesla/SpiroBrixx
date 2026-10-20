#!/bin/bash
# SPDX-FileCopyrightText: 2023-2026 Stefan Helmert <stefan@entroserv.de>
#
# SPDX-License-Identifier: CERN-OHL-S-2.0


find ~/.cache/pypoetry/virtualenvs/ -name "*.nbi" | xargs rm
find ~/.cache/pypoetry/virtualenvs/ -name "*.nbc" | xargs rm

