#!/bin/bash

# deletes the temp directory
function cleanup {
  rm -rf "$WORK_DIR"
  echo "Deleted TEMP working directory $WORK_DIR"
}

# register the cleanup function to be called on the EXIT signal
trap cleanup EXIT

# check args
if [[ $# -ne 1 ]]; then
  echo "Incorrect # of program arguments: $#; specify output location"
  exit 1
fi

WORK_DIR=$(mktemp -d)
PLUGIN="$WORK_DIR/plugin.matchday"
# create temp dir
if [[ ! "$WORK_DIR" || ! -d "$WORK_DIR" ]]; then
  echo "Could not create TEMP directory"
  exit 1
fi
mkdir "$PLUGIN"

# copy & zip files
echo "Copying files..."
cp ./main.py "$PLUGIN"
cp ./addon.xml "$PLUGIN"
cp ./LICENSE "$PLUGIN"
cp -r ./resources "$PLUGIN"
echo "Zipping..."
cd "$WORK_DIR" || exit 1
zip -qr "$1/plugin.matchday.zip" "."
echo "Done."
