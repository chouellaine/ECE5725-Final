import subprocess

#Runs a bash script to record from the microphone. Stores as the student's recording.
def record_stud():
    cmd = "arecord --device=hw:1,0 --format S16_LE --rate 44100 --duration 5 -c1 stud.wav"
    subprocess.check_output(cmd, shell=True)
    
#Runs a bash script to record from the microphone. Stores as the professional's recording.
def record_prof():
    cmd = "arecord --device=hw:1,0 --format S16_LE --rate 44100 --duration 5 -c1 prof.wav"
    subprocess.check_output(cmd, shell=True)
