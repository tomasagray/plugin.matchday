:: Exports plugin as a .zip file for installation in Kodi
@echo off

:: Zip path
Set zip-path=C:\Program Files\7-Zip
Set "zip=%zip-path%\7z.exe"

:: Kodi addon directory
Set "export-dir=%1"
Set "work-dir=%USERPROFILE%\Code\Source\IdeaProjects\plugin.matchday"
:: Top-level files & dirs
Set "main=%work-dir%\main.py"
Set "addon=%work-dir%\addon.xml"
Set "lic=%work-dir%\LICENSE"
Set "resources=%work-dir%\resources"

:: Zip plugin
Set "archive=%work-dir%\plugin.matchday"
:: Create tmp dir
echo Creating temporary directory...
IF EXIST %archive% (rmdir /S /Q %archive%)
mkdir %archive%
:: Copy files to tmp dir
echo Copying files to tmp dir
COPY %main% "%archive%\"
COPY %addon% "%archive%\"
COPY %lic% "%archive%\"
XCOPY /e /y %resources% "%archive%\resources\"
echo Zipping plugin...
"%zip%" a -tzip "%archive%.zip" "%archive%"
:: Copy archive to export dir
MOVE "%archive%.zip" %export-dir%
:: Remove temp files
echo Removing temporary files...
rmdir /s/q %archive%
echo Done.