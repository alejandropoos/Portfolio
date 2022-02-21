@echo off
mode con:cols=60 lines=30

for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a" 
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%" 
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"

set "datestamp=%YYYY%%MM%%DD%" & set "timestamp=%HH%%Min%" 
set "fullstamp=%DD%-%MM%-%YYYY%_%HH%hs-%Min%min"

python %cd%\main.py > Logs\OutputConsola_%fullstamp%.txt 1
