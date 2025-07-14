#!/bin/sh

source .venv/bin/activate

glib-compile-resources \
  --target=data/oracles.gresource \
  --sourcedir=data \
  "data/oracles.gresource.xml"

pyinstaller oracles.spec

rm -r "dist/Lazuli Launcher"

test -f "dist/Lazuli Launcher Installer.dmg" && rm "dist/Lazuli Launcher Installer.dmg"
create-dmg \
  --background "data/background_macos_installer.png" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --text-size 15 \
  --icon "Lazuli Launcher.app" 120 185 \
  --hide-extension "Lazuli Launcher.app" \
  --app-drop-link 480 185 \
  "Lazuli Launcher Installer.dmg" \
  "dist/"

mv "Lazuli Launcher Installer.dmg" "dist/"