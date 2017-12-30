#!/bin/bash
set -e

if [ $# -eq 0 ]
then
	echo "Usage: build.sh <build number>"
else
	rm -rf target
	mkdir target
	cp -r deb target/package
	rsync -r src target/package/opt/lkprint --exclude "__pycache__"
	cd target
	sed -i "s/BUILDNUMBER/$1/" package/DEBIAN/control
	dpkg-deb --build package .
fi

