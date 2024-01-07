#!/bin/bash

rm -rf PhotosRemBG

rembg p Photos PhotosRemBG

mogrify -trim PhotosRemBG/*

mkdir -p PhotosWhiteBG/PhotosRemBG/

for FILE in PhotosRemBG/*; do convert $FILE -background white -alpha remove -alpha off PhotosWhiteBG/$FILE; done

mv PhotosWhiteBG/PhotosRemBG/* PhotosWhiteBG/.

rm -r PhotosWhiteBG/PhotosRemBG/

