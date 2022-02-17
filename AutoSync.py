import sysconfig
import time
import subprocess

# переписать для библиотеки pyinotify? 
# https://sysadmin.pm/pyinotify/

def getTimeDate():
	return time.strftime("%H:%M:%S %d.%m.%Y", time.localtime())

def CreateCommit():
	nameCommit = f"{COMMIT}'{CURRENT_OS[1]} {getTimeDate()}'"
	createCommit = subprocess.Popen(nameCommit, stdout=subprocess.PIPE, shell=True)
	createCommit.wait()

def Push():
	push = subprocess.Popen(PUSH, stdout=subprocess.PIPE, shell=True)
	push.wait()

# Тип ОС
TYPE_OS = [
	[0, "Arch"],
	[1, "Android"],
	[2, "Windows"]
]

# По умолчанию Arch
CURRENT_OS = TYPE_OS[0]

if sysconfig.get_platform() == "linux-x86_64": 
	CURRENT_OS = TYPE_OS[0]
elif sysconfig.get_platform() == "linux-aarch64": 
	CURRENT_OS = TYPE_OS[1]

# Время обновления проверки в секундах
TIME_UPDATE = 30

# Отправлять на сервер изменения 1 раз в 5 минут
# TIME_PUSH = 300

STATUS = "git status"
ADD = "git add ."
COMMIT = "git commit -m "
PUSH = "git push"
REMOTE = "git remote show origin"
FETCH = "git fetch --all"
RESET = "git reset --hard origin/master"


# timeWorkLoop = 120

# _start = round(time.time(), 0)
# while round(time.time(), 0) < _start + timeWorkLoop:
while 1:
	# Проверка на наличие интернета 
	try:
		subprocess.check_call(["ping", "-c 1", "www.google.com"])
		print("***** Internet connect !!! *****")
	except:
		print("***** Internet DISconnect !!! *****")
		time.sleep(TIME_UPDATE)
		continue

	# Проверяем, были ли какие-то изменения в удалённом репозитории
	try:
		remote = subprocess.Popen(REMOTE,stdout=subprocess.PIPE, shell=True)
		remote.wait()
		output_remote = remote.communicate()[0].decode("utf-8")

		# Есть изменения в удалённом репозитории
		if ("локальная ветка устарела" in output_remote) or ("local out of date" in output_remote):
			# print("++++++++++++++++++++++++Есть обновления. Получить?")
			fetch = subprocess.Popen(FETCH,stdout=subprocess.PIPE, shell=True)
			fetch.wait()
			reset = subprocess.Popen(RESET,stdout=subprocess.PIPE, shell=True)
			reset.wait()
			print("***** PULL COMPLITE *****")
		# Изменений нет в удалённом репозитории
		elif ("уже актуальна" in output_remote) or ("up to date" in output_remote):
			print("***** NOT NEEDED PULL *****")
		else:
			print("1. Текст приёма не распознан! The reception text is not recognized!")
			print(output_remote)
	except:
		print("Неизвестная ошибка. Возможно нет интернета")
		time.sleep(TIME_UPDATE)
		continue

	# Проверяем с помощью git status, были ли какие-то изменения в локальной папке
	status = subprocess.Popen(STATUS, stdout=subprocess.PIPE, shell=True)
	status.wait()
	# Получаем ответ, и преобразуем в строку
	output_status = status.communicate()[0].decode("utf-8")

	# Фразы, с которыми нужно комитить
	if ("ничего не добавлено в коммит" in output_status) or ("которые не в индексе для" in output_status) or ("no changes added to commit" in output_status) or ("to include in what will be committed" in output_status):
		#  Добавляем изменения в коммит
		add = subprocess.Popen(ADD, stdout=subprocess.PIPE, shell=True)
		add.wait()
		# Создаём новый коммит
		CreateCommit()
		# Пуш на сервер
		Push()
		print("***** PUSH COMPLITE *****")
	elif ("нечего коммитить" in output_status) or ("nothing to commit" in output_status):
		print("***** NOT NEEDED PUSH *****")
	else:
		CreateCommit()
		Push()
		print("***** Принудительный коммит и пуш. Тип ошибки ниже *****")
		print(output_remote)

	time.sleep(TIME_UPDATE)
