#!/bin/bash
set -e
rm -rf target
mkdir target
cp -r deb target/package
rsync -r src target/package/opt/lkprint --exclude "__pycache__"
cd target
dpkg-deb --build package .

