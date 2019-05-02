import wave
import sys
import matplotlib.pyplot as plt
import numpy as np


spf = wave.open('test2.wav','r')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
i = 0

fs = spf.getframerate()
note_entry = []
time1 = 0
time2 = 0
for element in signal:
    if element > 400:
        time1 = i
        if (time1-time2)/fs > 0.3:
            time2 = time1
            note_entry.append(i/fs)
    time2 = time1
    i = i+1

#print(note_entry)


Time=np.linspace(0, len(signal)/fs, num=len(signal))

plt.figure(1)
plt.title('Signal Wave...')
plt.plot(Time,signal)
plt.show()

