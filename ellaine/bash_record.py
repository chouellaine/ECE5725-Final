import subprocess

def record_stud():
    subprocess.call("recordstud.sh", shell=True)

def record_prof():
    subprocess.call("recordprof.sh", shell=True)
