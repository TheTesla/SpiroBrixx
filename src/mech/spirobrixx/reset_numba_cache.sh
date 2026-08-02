#!/bin/bash

find ~/.cache/pypoetry/virtualenvs/ -name "*.nbi" | xargs rm
find ~/.cache/pypoetry/virtualenvs/ -name "*.nbc" | xargs rm

