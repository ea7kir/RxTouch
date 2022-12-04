import subprocess

# private functions

def deactivate_longmynd():
    pass

# public functions

def activate_longmynd():
    print('activating longmynd with:')

def shutdown():
    print('Doing the shutdown sequence.')
    deactivate_longmynd()
    #subprocess.check_call(['sudo', 'poweroff'])

