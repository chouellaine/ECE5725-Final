import subprocess

def record_stud():
    cmd = "arecord --device=hw:1,0 --format S16_LE --rate 44100 --duration 5 -c1 stud.wav"
    subprocess.check_output(cmd, shell=True)

def record_prof():
    cmd = "arecord --device=hw:1,0 --format S16_LE --rate 44100 --duration 5 -c1 prof.wav"
    subprocess.check_output(cmd, shell=True)
