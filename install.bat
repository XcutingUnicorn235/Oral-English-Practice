@echo off
REM Oral English Practice — Windows installer (fallback)
REM Usage: double-click this file, or run it in cmd.
REM
REM RECOMMENDED instead of this script: install as a Claude Code plugin —
REM   /plugin marketplace add XcutingUnicorn235/Oral-English-Practice
REM   /plugin install oral-english-practice@xcutingunicorn235
REM   (gives one-command install + automatic updates).
REM
REM This script is the manual fallback: it copies the skill folder into
REM   %USERPROFILE%\.claude\skills\ so Claude Code can find it.
REM   Your practice DATA is created separately on first use
REM   (defaults to %USERPROFILE%\oral-english-practice-log\) — this script does NOT
REM   touch any data, so re-running it is safe.

setlocal
chcp 65001 >nul

set "SRC=%~dp0"
set "DST=%USERPROFILE%\.claude\skills\oral-english-practice"

echo.
echo === Oral English Practice — install ===
echo.
echo Source: %SRC%plugins\oral-english-practice\skills\oral-english-practice
echo Target: %DST%
echo.

if not exist "%USERPROFILE%\.claude\skills" mkdir "%USERPROFILE%\.claude\skills"
if not exist "%DST%" mkdir "%DST%"

xcopy /E /I /Y /Q "%SRC%plugins\oral-english-practice\skills\oral-english-practice" "%DST%" >nul
if errorlevel 1 (
    echo [FAILED] copy
) else (
    echo [DONE] skill copied
)

echo.
echo === Install complete ===
echo.
echo Next:
echo   1. Open Claude Code, type:  /oral-english-practice
echo      (or just say "I want to practice spoken English")
echo   2. It will give you the prompt to paste into the Claude APP (voice mode).
echo   3. After practicing, paste the app's report back into Claude Code —
echo      the skill logs it and tracks your progress.
echo.
echo Your practice-log folder will be created on first use at:
echo   %USERPROFILE%\oral-english-practice-log\
echo   (the skill prints the full path the first time it creates it.)
echo   (To use a different location, create a file named .oral-english-data-path
echo    in your home folder containing the path you want.)
echo.
pause
