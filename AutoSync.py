import sysconfig
import time
import subprocess
import os


def getTimeDate():
	"""
	Gets the current time and date in a convenient format
	Получает текущее время и дату в удобном формате
	"""
	return time.strftime("%H:%M:%S %d.%m.%Y", time.localtime())


def CreateCommit():
	"""
	Result. A commit is created with the OS type and the current time:
		Arch 13:12:21 17.01.2022
		Android 13:12:21 17.01.2022
		Windows 13:12:21 17.01.2022

	Результат. Создаётся коммит с типом ОС и текущем временем:
		Arch 13:12:21 17.01.2022
		Android 13:12:21 17.01.2022
		Windows 13:12:21 17.01.2022
	"""
	nameCommit = f"{COMMIT}'{CURRENT_OS[1]} {getTimeDate()}'"
	createCommit = subprocess.Popen(nameCommit, stdout=subprocess.PIPE, shell=True)
	createCommit.wait()


def Push():
	push = subprocess.Popen(PUSH, stdout=subprocess.PIPE, shell=True)
	push.wait()


def getCurrentOS():
	"""
	Automatic detection of the operating system (OS). Required to create a commit
	Автоматическое определение операционной системы(ОС). Требуется для создания коммита
	"""
	TYPE_OS = [
		[0, "Arch"],
		[1, "Android"],
		[2, "Windows"]
	]

	if sysconfig.get_platform() == "linux-x86_64":
		return TYPE_OS[0]
	elif sysconfig.get_platform() == "linux-aarch64":
		return TYPE_OS[1]
	else:
		return TYPE_OS[2]  # Windows and other


CURRENT_OS = getCurrentOS()

# Sync update time in seconds
# Время обновления синронизации в секундах
TIME_UPDATE = 30

STATUS = "git status"
ADD = "git add ."
COMMIT = "git commit -m "
PUSH = "git push"
REMOTE = "git remote show origin"
FETCH = "git fetch --all"
RESET = "git reset --hard origin/master"

# Getting the absolute path to the current file
# Получение абсолютного пути к текущему файлу
current_file_path = os.path.abspath(__file__)

# Getting the name of the current file
# Получение имени текущего файла
file_name = os.path.basename(current_file_path)

# We form a path without the name of the file itself. Analogue output of the pwd command
# Формируем путь без имени самого файла. Аналог вывода команды pwd
pwd = current_file_path.replace(f"/{file_name}", "")

# Let's go to the folder. For git to find the repository
# Переходим в папку. Чтобы git нашёл репозиторий
os.chdir(pwd)

while True:
	# Checking for internet availability
	# Проверка на наличие интернета
	try:
		subprocess.check_call(["ping", "-c 1", "www.google.com"])
		print("***** Internet connect !!! *****")
	except subprocess.CalledProcessError as err:
		print(f"***** Internet DISconnect !!! *****\n{err}")
		time.sleep(TIME_UPDATE)
		continue

	# Checking if there were any changes in the remote repository
	# Проверяем, были ли какие-то изменения в удалённом репозитории
	try:
		remote = subprocess.Popen(REMOTE, stdout=subprocess.PIPE, shell=True)
		remote.wait()
		# We get the answer, and convert it to a string
		# Получаем ответ, и преобразуем в строку
		output_remote = remote.communicate()[0].decode("utf-8")

		# If there are changes in the remote repository, then we do FETCH and RESET. This is necessary in order to avoid errors when merging.
		# Если есть изменения в удалённом репозитории, то делааем FETCH и RESET. Это необходимо для того, чтобы избежать ошибок при слиянии.
		if ("локальная ветка устарела" in output_remote) or ("local out of date" in output_remote):
			fetch = subprocess.Popen(FETCH, stdout=subprocess.PIPE, shell=True)
			fetch.wait()
			reset = subprocess.Popen(RESET, stdout=subprocess.PIPE, shell=True)
			reset.wait()
			print("***** PULL COMPLITE *****")
		# If there are no changes in the remote repository, then PULL is not necessary
		# Если изменений нет в удалённом репозитории, то PULL делать не надо
		elif ("уже актуальна" in output_remote) or ("up to date" in output_remote):
			print("***** NOT NEEDED PULL *****")
		else:
			print("Текст приёма не распознан! The reception text is not recognized!")
			print(output_remote)
	except:
		print("Неизвестная ошибка. Возможно нет интернета")
		time.sleep(TIME_UPDATE)
		continue

	# We check with git status whether there have been any changes in the local repository
	# Проверяем с помощью git status, были ли какие-то изменения в локальном репозитории
	status = subprocess.Popen(STATUS, stdout=subprocess.PIPE, shell=True)
	status.wait()
	# We get the answer, and convert it to a string
	# Получаем ответ, и преобразуем в строку
	output_status = status.communicate()[0].decode("utf-8")

	# If the necessary phrases are found in the message, then
	# Если найдены необходимые фразы в сообщении, то
	if ("ничего не добавлено в коммит" in output_status) or ("которые не в индексе для" in output_status) or ("no changes added to commit" in output_status) or ("to include in what will be committed" in output_status):
		# Adding changes to the commit
		# Добавляем изменения в коммит
		add = subprocess.Popen(ADD, stdout=subprocess.PIPE, shell=True)
		add.wait()
		# Creating a new commit
		# Создаём новый коммит
		CreateCommit()
		# Making a PUSH to a remote repository
		# Делаем PUSH на удалённый репозиторий
		Push()
		print("***** PUSH COMPLITE *****")
	# If there were no changes, then there is no need to do PUSH
	# Если изменений не было, то и делать PUSH не нужно
	elif ("нечего коммитить" in output_status) or ("nothing to commit" in output_status):
		print("***** NOT NEEDED PUSH *****")
	else:
		CreateCommit()
		Push()
		print("***** Forced COMMIT and PUSH. Error message, below *****")
		print(output_remote)

	time.sleep(TIME_UPDATE)
