# Telebot
Для работы необходимо установить локальный сервер Stable Diffusion:
https://github.com/AUTOMATIC1111/stable-diffusion-webui
Запускается через webui-user.bat, в сам bat нужно дописать:
```
set COMMANDLINE_ARGS=--xformers --autolaunch --listen --api
```
Вид готового webui-user.bat:
```
@echo off
if not exist python (echo Unpacking Git and Python... & mkdir tmp & start /wait git_python.part01.exe & del git_python.part01.exe & del git_python.part*.rar)
set pypath=home = %~dp0python
if exist venv (powershell -command "$text = (gc venv\pyvenv.cfg) -replace 'home = .*', $env:pypath; $Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding($False);[System.IO.File]::WriteAllLines('venv\pyvenv.cfg', $text, $Utf8NoBomEncoding);")

for /d %%i in (tmp\tmp*,tmp\pip*) do rd /s /q "%%i" & del /q tmp\tmp* & rd /s /q pip\cache

set APPDATA=tmp
set USERPROFILE=tmp
set TEMP=tmp
set PYTHON=python\python.exe
set GIT=git\cmd\git.exe
set PATH=git\cmd
set VENV_DIR=venv
set COMMANDLINE_ARGS=--xformers --autolaunch --listen --api
git pull origin master
call webui.bat
```

Для работы GPT4all необходимо установить модель:
https://civitai.com/models/7241/mix-pro-v4
