#!/usr/bin/env python3
import fileinput
import inspect
import os
import re
import subprocess
from datetime import datetime
from multiprocessing import Process
from subprocess import PIPE

env = dict(os.environ)


def _print_line_number(number_of_outer_frame=1):
    cf = inspect.currentframe()
    frame = cf
    for ii in range(number_of_outer_frame):
        frame = frame.f_back

    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    print('\n'.join(['#' * 40, '[%s] LINE NUMBER: %d' % (timestamp, frame.f_lineno), '#' * 40]))


def _run(cmd, file_path_name=None, cwd=None, file_mode='a', run_env=env):
    def _f():
        if not file_path_name:
            _p = subprocess.Popen(cmd, cwd=cwd, env=run_env)
            _p.communicate()
            if _p.returncode != 0:
                raise Exception()
        else:
            with open(file_path_name, file_mode) as ff:
                _p = subprocess.Popen(cmd, stdout=ff, cwd=cwd, env=run_env)
                _p.communicate()
                if _p.returncode != 0:
                    raise Exception()

    _print_line_number(2)
    cmd_string = ' '.join(cmd)
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    print('\n'.join(['#' * 40, '[%s] COMMAND: %s' % (timestamp, cmd_string), '#' * 40]))

    pp = Process(target=_f)
    pp.start()
    pp.join()
    if pp.exitcode != 0:
        raise Exception()


def _file_line_replace(file_path_name, str_old, str_new, backup='.bak'):
    with fileinput.FileInput(file_path_name, inplace=True, backup=backup) as ff:
        for line in ff:
            new_line = re.sub(str_old, str_new, line)
            print(new_line, end='')


def main():
    provisioning_path = '/vagrant'
    hostname = 'dv-sixshop-my-local-1a-012345'
    _file_line_replace('/etc/sysconfig/network', '^HOSTNAME=localhost.localdomain$', 'HOSTNAME=%s' % hostname)
    with open('/etc/hosts', 'a') as ff:
        ff.write('127.0.0.1 %s\n' % hostname)
    _run(['hostname', hostname])
    _run(['/etc/init.d/network', 'restart'])

    _print_line_number()

    _print_line_number()

    _run(['fallocate', '-l', '2G', '/swapfile'])
    _run(['chmod', '600', '/swapfile'])
    _run(['mkswap', '/swapfile'])
    _run(['swapon', '/swapfile'])
    with open('/etc/fstab', 'a') as ff:
        ff.write('/swapfile	swap	swap	sw	0	0\n')

    _print_line_number()

    with open('/etc/server_info', 'w') as ff:
        ff.write('AWS_EC2_INSTANCE_ID=i-01234567\n')
        ff.write('AWS_EC2_AVAILABILITY_ZONE=my-local-1a\n')

    _print_line_number()

    subprocess.Popen(['chpasswd'], stdin=PIPE).communicate(b'root:1234qwer')
    _file_line_replace('/etc/ssh/sshd_config', '^#PermitRootLogin yes$', 'PermitRootLogin yes')
    _file_line_replace('/etc/ssh/sshd_config', '^PasswordAuthentication no$', 'PasswordAuthentication yes')
    _run(['/sbin/service', 'sshd', 'restart'])

    _print_line_number()

    _run(['yum', '-y', 'update'])
    file_path_name = '%s/requirements_rpm.txt' % provisioning_path
    if os.path.exists(file_path_name):
        with open(file_path_name, 'r') as ff:
            lines = ff.readlines()
            for ll in lines:
                _run(['yum', '-y', 'install', ll.strip()])
    _run(['yum', '-y', 'erase', 'java-1.7.0-openjdk'])

    _print_line_number()

    _run(['yum', '-y', 'erase', 'ntp*'])
    _run(['yum', '-y', 'install', 'chrony'])
    _run(['/sbin/service', 'chronyd', 'start'])
    _run(['/sbin/chkconfig', 'chronyd', 'on'])

    _print_line_number()

    cmd_common = ['cp', '--backup']
    file_list = list()
    for ff in file_list:
        cmd = cmd_common + ['%s/configuration' % provisioning_path + ff, ff]
        _run(cmd)

    ff_source = '/etc/tomcat8/tomcat8_vagrant.conf'
    ff_target = '/etc/tomcat8/tomcat8.conf'
    cmd = cmd_common + ['%s/configuration' % provisioning_path + ff_source, ff_target]
    _run(cmd)

    _print_line_number()

    _run(['/sbin/chkconfig', 'tomcat8', 'on'])
    _run(['reboot'])


if __name__ == "__main__":
    main()
