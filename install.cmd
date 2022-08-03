:: Installs (updates) plugin files in Kodi installation directory.
@echo off

echo Installing Matchday Plugin for Kodi...
:: Kodi addon directory
Set "kodi-dir=%APPDATA%\Kodi\addons\plugin.matchday\"
Set "work-dir=%~dp0"
:: Top-level files & dirs
Set "main=%work-dir%\main.py"
Set "addon=%work-dir%\addon.xml"
Set "resources=%work-dir%\resources"

echo Copying data from %main% to %kodi-dir%...
echo Installing addon...
COPY %main% %kodi-dir%
COPY %addon% %kodi-dir%
echo Installing resources...
XCOPY /y /s /q %resources% "%kodi-dir%resources\"
echo Done.
