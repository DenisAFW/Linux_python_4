import pytest
import yaml
from sshcheckers import ssh_checkout
import random
import string
from datetime import datetime
from sshcheckers import ssh_checkout

with open('config.yaml', encoding='utf-8') as fy:
    data = yaml.safe_load(fy)


@pytest.fixture
def make_folders():
    return ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                        "mkdir {} {} {} {}".format(data["folderin"], data["folderout"], data["folderext"],
                                                   data["folderbad"]), "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["folderin"], data["folderout"],
                                                            data["folderext"], data["folderbad"]), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                        "cd {}; dd if=/dev/urandom of={} bs=1K count=1 iflag=fullblock".format(data["folderin"],
                                                                                               filename),
                        ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    test_filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                        "cd {}; mkdir {}".format(data["folderin"], subfoldername), ""):
        return None, None
    if not ssh_checkout(data['ip_user'], data['user'], data['passwd'],
                        "cd {}/{}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folderin"],
                                                                                                  subfoldername,
                                                                                                  test_filename,
                                                                                                  data["bs"]), ""):
        return subfoldername, None

    return subfoldername, test_filename


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield print("Stop: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
