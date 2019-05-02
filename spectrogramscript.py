import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.io import wavfile

sample_rate, samples = wavfile.read('test2.wav')
frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

d = {}

for i in range(len(spectrogram)):
    for j in range(len(spectrogram.T)):
        if spectrogram[i][j] > 100:
            if d.get(round(times[j],1)) == None:
            #spec.append(round(spectrogram[i][j],1))
                d[round(times[j],1)] = round(frequencies[i],1)

print(d)

'''
plt.pcolormesh(times, frequencies, spectrogram)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
'''
