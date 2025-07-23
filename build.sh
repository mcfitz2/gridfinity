#!/bin/bash

set -e

BIN_DIR="bins"
OUT_DIR="dist"

mkdir -p "$OUT_DIR"

for scad_file in "$BIN_DIR"/*.scad; do
    base_name=$(basename "$scad_file" .scad)
    # Skip entrypoint.scad
    if [[ "$base_name" == "entrypoint" ]]; then
        continue
    fi
    stl_file="$OUT_DIR/$base_name.stl"
    echo "Building $scad_file -> $stl_file"
    openscad -o "$stl_file" "$scad_file"
done