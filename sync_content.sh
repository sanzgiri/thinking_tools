#!/bin/bash
mkdir -p site/src/data
mkdir -p site/content
cp tools.json site/src/data/
cp -r content/* site/content/ 2>/dev/null || :
echo "Synced content and tools.json"
