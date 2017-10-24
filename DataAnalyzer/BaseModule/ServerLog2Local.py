# coding=utf-8

import sys
import paramiko
# import json
import traceback
import time
# import tqdm


class RemoteServerOperation(object):
    def __init__(self, hostname, username, private_key_file, password='zjtachao@0801'):
        self.host = hostname
        self.user = username
        self.pwd = password
        self.pkf = private_key_file

    def pwd_connect(self):
        """Password Connection"""
        try:
            paramiko.util.log_to_file('./paramiko.log')     # 创建SSH连接日志文件（只保留前一次连接的详细日志，以前的日志会自动被覆盖）
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()                     # 读取know_host
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ssh.connect(host,username='root',allow_agent=True,look_for_keys=True)
            ssh.connect(hostname=self.host, username=self.user, password=self.pwd, allow_agent=True)
            return ssh
        except:
            traceback.print_exc()
            return None

    def rsa_connect(self):
        """RSA Connection"""
        try:
            paramiko.util.log_to_file('./paramiko.log')     # 创建SSH连接日志文件（只保留前一次连接的详细日志，以前的日志会自动被覆盖）
            key = paramiko.RSAKey.from_private_key_file(self.pkf)
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.host, username=self.user, pkey=key)
            return ssh
        except:
            traceback.print_exc()
            return None

    def execute_commands(self, ssh_connect, command):
        """execute commands and return results"""
        results = ""
        try:
            stdin, stdout, stderr = ssh_connect.exec_command(command)
            results = stdout.read()
        except:
            traceback.print_exc()
            pass
        return results

    def target_file(self, wcadid_list, rantime_list):
        target_file_dict = {}
        try:
            for i, adids in enumerate(wcadid_list):
                for adid in adids.split("/"):
                    target_file_dict[adid] = ['-'.join([y if len(y) >= 2 else "0"+y
                                                        for y in x.split("/")])+".log.rm" for x in rantime_list[i].split("-")]
        except:
            traceback.print_exc()
            pass
        return target_file_dict

    def get_remote_data(self, ssh_connect, remote_path, local_path, target_file_dict):
        """get data from remote server"""
        try:
            ftp = ssh_connect.open_sftp()
            for dirs in ['click', 'exposure']:
                listdir = [x for x in ftp.listdir(remote_path+dirs) if len(x) == 17]
                # print listdir
                self.execute_commands(ssh_connect, 'touch xcy_tmp; rm xcy_tmp; touch xcy_tmp')
                for adid, target in target_file_dict.items():
                    sub_listdir = [x for x in listdir if target[0] <= x <= target[1]]
                    # print sub_listdir
                    for filename in sub_listdir:
                        cmd = 'grep "\\\"wcAdId\\\":\\\"%s\\\"" %s >> ./xcy_tmp' % (adid, remote_path+dirs+"/"+filename)
                        self.execute_commands(ssh_connect, cmd)
                ftp.get("./xcy_tmp", local_path+dirs+"/"+dirs)
                print('%s download complete!' % dirs)
            ftp.close()
        except:
            traceback.print_exc()
            pass


if __name__ == '__main__':

    st_time = time.time()

    wcadid_list = ['115', '128', '75', '76', '163/171', '178', '175', '177', '255/256']
    rantime_list = ['2016/11/16-2016/11/17', '2016/11/17-2016/11/17', '2016/11/3-2016/11/5', '2016/11/4-2016/11/5', '2016/12/1-2016/12/3', '2016/12/2-2016/12/3', '2016/12/3-2016/12/3', '2016/12/4-2016/12/4', '2016/12/16-2016/12/17']

    server_operator = RemoteServerOperation('123.206.19.146', 'root', '/Users/XI/.ssh/id_rsa')
    ssh_connect = server_operator.pwd_connect()
    # ssh_connect = server_operator.rsa_connect()
    target_file_dict = server_operator.target_file(wcadid_list, rantime_list)
    server_operator.get_remote_data(ssh_connect, "/opt/Jarvis/report/logs/", "../../../", target_file_dict)
    ssh_connect.close()

    print("Downloading Cost: ", time.time() - st_time)

