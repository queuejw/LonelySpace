#!/bin/bash
echo ===================
echo "Обновление системы и установка Python..."
echo ===================
sudo apt install update && sudo apt install update
sudo apt install python3-full
echo ===================
echo "Установка требуемых библиотек из requirements.txt..."
echo ===================
python3 -m pip install -r requirements.txt
echo ===================
echo "Всё готово! Можете закрыть это окно"
echo ===================