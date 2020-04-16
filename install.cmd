@ECHO off

:: Kodi addon directory
Set "kodi-dir=%APPDATA%\Kodi\addons\plugin.matchday\"
Set "work-dir=%USERPROFILE%\Code\Source\IdeaProjects\plugin.matchday"
:: Top-level files & dirs
Set "main=%work-dir%\main.py"
Set "addon=%work-dir%\addon.xml"
Set "resources=%work-dir%\resources"

echo Copying data from %main% to %kodi-dir%...
COPY  %main% %kodi-dir%
COPY %addon% %kodi-dir%
XCOPY /e /y %resources% "%kodi-dir%resources\"

