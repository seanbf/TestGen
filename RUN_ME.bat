@ECHO off
:start
SET ThisScriptsDirectory=%~dp0
@ECHO on
py -m streamlit run %ThisScriptsDirectory%\TestGen.py