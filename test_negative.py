# Создать отдельный файл для негативных тестов. Функцию
# проверки вынести в отдельную библиотеку. Повредить архив
# (например, отредактировав его в текстовом редакторе).
# Написать негативные тесты работы архиватора с командами
# распаковки (e) и проверки (t) поврежденного архива.
import yaml

from sshcheckers import ssh_checkout

# folderin = "/home/user/tst"
# folderout = "/home/user/out"
# folderext = "/home/user/folder1"
# folderbad = "/home/user/folder2"
with open("config.yaml") as fy:
    data = yaml.safe_load(fy)


def test_step1():
    assert ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                        f"cd {data['folderbad']}; 7z e arx2.7z -o{data['folderext']} -y", "ERRORS"), "test1 FAIL"


def test_step2():
    assert ssh_checkout(data['ip_user'], data['user'], data['passwd'], f"cd {data['folderbad']}; 7z t arx2.7z",
                        "ERRORS"), "test1 FAIL"
