from sshcheckers import ssh_checkout, upload_files
import yaml

with open("config.yaml") as fy:
    data = yaml.safe_load(fy)


def deploy():
    res = []
    upload_files(data["ip_user"], data["user"], data["passwd"], data["local_path"], data["remote_path"])
    res.append(ssh_checkout(data["ip_user"], data["user"], data["passwd"],
                            f"echo {data['passwd']} | sudo -S dpkg -i {data['remote_path']}",
                            "Настраивается пакет"))
    res.append(ssh_checkout(data["ip_user"], data["user"], data["passwd"],
                            f"echo {data['passwd']} | sudo -S dpkg -s p7zip-full",
                            "Status: install ok installed "))
    return all(res)


if deploy():
    print("Деплой успешен")
else:
    print("Деплой неуспешен")
