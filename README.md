# NotesAutoSync

Скрипт для автоматической синхронизации заметок(информации) в Codeberg(GitHub) репозиторий, с помощью SSH.

## Инструкция для запуска

### **Linux** 
#### 1. Склонировать репозиторий к себе на устройство
```bash
    git clone https://codeberg.org/femto/NotesAutoSync.git
```
или
```bash
    git clone https://github.com/AnDsergey13/NotesAutoSync.git
```
#### 2. Перейти в папку со скриптом
```bash
    cd NotesAutoSync
```
#### 3. Скопировать python скрипт AutoSync.py, в корень синхронизируемого репозитория
```bash
    cp AutoSync.py /home/USER/Notes/AutoSync.py
    # Вместо /home/USER/Work/Notes/* ввести свой путь, где находятся заметки
    # где, USER - это имя вашего пользователя
```
#### 4. Перейти в папку с заметками
```bash
    cd /home/USER/Notes
```
#### 5. При необходимости, настройте задержку синхронизации заметок в AutoSync.py
```python
    # Время в секундах
    TIME_UPDATE = 30
```
❗❗❗ Перед тем как запускать python скрипт, нужно настроить [SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) **без пароля**, для синхронизируемого репозитория. Иначе скрипт работать не будет.

А для тестирование вашего SSH-соединения для Codeberg, вместо 
```bash
    ssh -T git@github.com
```
нужно писать
```bash
    ssh -T git@codeberg.org 
```

#### 6. Запуск синхронизации
```bash
    python AutoSync.py
```
---
### **Windows** - TODO
---
### **Android** - TODO