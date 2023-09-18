# Добавить в проект тесты, проверяющие работу команд
# d (удаление из архива) и u (обновление архива). Вынести
# в отдельные переменные пути к папкам с файлами, с архивом
# и с распакованными файлами. Выполнить тесты с ключом -v.

import yaml
import subprocess
from sshcheckers import ssh_checkout
from deploy import deploy

with open('config.yaml', encoding='utf-8') as fy:
    data = yaml.safe_load(fy)


# def checkout(cmd, text):
#     result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
#     if text in result.stdout and result.returncode == 0:
#         return True
#     else:
#         return False
#
#
# def checkout_negative(cmd, text):
#     result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
#     if (text in result.stdout or text in result.stderr) and result.returncode != 0:
#         return True
#     else:
#         return False


def getout(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout


class TestPositive:

    def test_step0(self):
        if deploy():
            return print("Everything is Ok")
        else:
            return print("Test 0 is Failed")

    def test_step1(self, make_folders, clear_folders, make_files):
        # test1
        res = []

        res.append(ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                                "cd {}; 7z a {}/arx2".format(data["folderin"], data["folderout"]),
                                "Everything is Ok"))
        res.append(ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                                "ls {}".format(data["folderout"]), "arx2.7z"))
        assert all(res)

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                                "cd {}; 7z a {}/arx2".format(data["folderin"], data["folderout"]),
                                "Everything is Ok"))
        res.append(ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                                "cd {}; 7z e arx2.7z -o{} -y".format(data['folderout'], data['folderext']),
                                "Everything is Ok"))
        for item in make_files:
            res.append(
                ssh_checkout(data['ip_user'], data['user'], data['passwd'], "ls {}".format(data['folderext']), item))
        assert all(res), "test 2 FAIL"

    def test_step3(self):
        # test3
        assert ssh_checkout(data['ip_user'], data['user'], data['passwd'], f"cd {data['folderout']}; 7z t arx2.7z",
                            "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4
        assert ssh_checkout(data['ip_user'], data['user'], data['passwd'], f"cd {data['folderout']}; 7z d arx2.7z",
                            "Everything is Ok"), "test_4 FAIL"

    def test_step5(self, clear_folders, make_files):
        # test5
        res = []
        res.append(ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                                "cd {}; 7z a {}/arx2".format(data["folderin"], data['folderout']), "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                                    "cd {}; 7z l arx2.7z".format(data['folderout'], data['folderext']), item))
        assert all(res), "test 5 FAIL"

    # ----------------------------------------------------------------------------------------------

    # Доработать позитивные тесты таким образом, чтобы при
    # архивации дополнительно проверялось создание файла
    # архива, а при распаковке проверялось создание файлов.

    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test 6
        res = []
        res.append(ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                                "cd {}; 7z a {}/arx".format(data['folderin'], data['folderout']), "Everything is Ok"))
        res.append(
            ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                         "cd {}; 7z x arx.7z -o{} -y".format(data['folderout'], data["folderbad"]), "Everything is Ok"))

        for item in make_files:
            res.append(
                ssh_checkout(data['ip_user'], data['user'], data['passwd'], "ls {}".format(data["folderbad"]), item))

        res.append(ssh_checkout(data['ip_user'], data['user'], data['passwd'], "ls {}".format(data["folderbad"]),
                                make_subfolder[0]))
        res.append(ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                                "ls {}/{}".format(data["folderbad"], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test 6 FAIL"

    def test_step7(self):
        # test7
        assert ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                            "cd {}; 7z d arx.7z".format(data['folderout']), "Everything is Ok"), "test 7 FAIL"

    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for item in make_files:
            res.append(ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                                    "cd {}; 7z h {}".format(data['folderin'], item), "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data['folderin'], item)).upper()
            res.append(ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                                    "cd {}; 7z h {}".format(data['folderin'], item), hash))
        assert all(res), "test 8 FAIL"
