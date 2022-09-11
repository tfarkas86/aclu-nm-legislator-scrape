#!/bin/bash

echo "repro-votes-csvs/$1,,,,,"
sed 's/^/,/' "repro-votes-csvs/$1"
echo ""

