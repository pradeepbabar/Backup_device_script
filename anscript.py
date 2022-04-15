import paramiko
import time
import subprocess

host = '10.10.20.70'
username = 'admin'
password = 'admin'

cmd1 = ["terminal length 0 \n",
        "sh run \n",
        "exit \n",
        " \n"]

session = paramiko.SSHClient()

session.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def cisco_exec(host, commands):
    try:
        print(f"\n{'#' * 50}\nConnecting to the Device {host} \n{'#' * 50}")
        session.connect(hostname=host,
                        username=username,
                        password=password,
                        port='2221',
                        )

        DEVICE_ACCESS = session.invoke_shell()
        for command in commands:
            DEVICE_ACCESS.send(f'{command}\n')
            time.sleep(.5)
            output = DEVICE_ACCESS.recv(65000)
            print(output.decode(), end='')
        session.close()

        with open("output.txt", "w") as f:
            subprocess.check_call(["python", "anscript.py"], stdout=f)





    except:
        print("Unable to connect to the Device")


cisco_exec('10.10.20.70', cmd1)
