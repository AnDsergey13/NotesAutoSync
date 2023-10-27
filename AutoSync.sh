# Google translator used
# Go to the folder where the script itself is located and get the path (pwd)
# Переходим в папку, где находится сам скрипт и получаем путь(pwd)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Substitute the path to run the python file
# Подставляем путь для запуска python файла
python "$SCRIPT_DIR/AutoSync.py"
