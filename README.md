# Telebot
GIT Должен быть установлен

Нужно установить Python версии 3.11.9

Нужно создать venv и установить все зависимости

Обязательно нужно подставить токен бота в tgbot.py (6781423114:AAGw_CbVilczpzOb3szz4FD-fBv3b_eIPdY)

Сам бот https://t.me/Story54Bot

Для работы необходимо установить локальный сервер Stable Diffusion, строго следуя приложенной инструкции в репозитории:
https://github.com/serpotapov/stable-diffusion-portable

Для работы Stable Diffusion необходимо установить модель:

https://civitai.com/models/7241/mix-pro-v4

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
После запуска держать комендную панель открытой, до завершения работы программы.

Помещаем языковую модель в папку models не меняя её названия 

Ссылка на языковую модель - https://drive.google.com/file/d/1gHZTK0rvmcDURxqVUGPfPdj85ZJ4EpXA/view?usp=sharing

Запускаем файл tgbot.py 

НАСТРОЙКА

Наш продукт имеет возможность по настройке количества глав, для настройки стоит указать количество глав в константе MAX_PARTS

ВОЗМОЖНОСТИ

-- Генерация полной истории состоящей из различного количества глав вместе с иллюстрацией и озвучкой текста

-- Генерация полной истории с персонажем пользователя состоящей из различного количества глав вместе с иллюстрацией и озвучкой текста
    для инициализации нужно выбрать персонажа в меню персонажей
    
-- Откат на главу, на пример если вас не устраивает глава которая была только что сгенерирована можно прописать /back во время создания истории

-- Сохранение персонажей, для создания\выбора персонажа нужно перейти в соответствующее меню

-- Сохранение историй, для сохранения истории нужно нажать в конце рассказа сохранить историю, для дальнейшего просмтора нужно выбрать соответствующий пункт меню

-- МУЛЬТИПЛЕЕР

    Для создания комнаты с мультиплеером нужно прописать команду /create [название комнаты]
    
    Для присоединения к комнате нужно прописать команду /lion [название комнаты]
    
    Для общения в групповом чате пользователям нужно перед сообщениями добавлять /group_chat [название комнаты]
    
    Генерация истории в комнате проводиться единожды не сохраняя контекст
    
    Для инициализации создания истории нужно написать в грапповой чат prompt [промпт для истории]

      после 2х сообщений с промптами создание истории автоинициаллизируется. 

Ну и промпты можно конечно тоже редактировать


