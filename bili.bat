@echo off
echo ��ǰ�̷���%~d0
echo ��ǰ�̷���·����%~dp0
echo ��ǰ������ȫ·����%~f0
set "strc=pythonfromroot"
set "stra=%~sdp0%strc%"
echo "%stra%"
cd "%stra%"
python ontime-bili.py
cd %~sdp0
pause