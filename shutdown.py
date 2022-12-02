import subprocess

def shutdown():
    subprocess.check_call(['sudo', 'poweroff'])
