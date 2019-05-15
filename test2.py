from aubio import source, onset
import numpy as np
import matplotlib.pyplot as plt

win_s = 512                 # fft size
hop_s = win_s // 2          # hop size
ex1 = "test2.wav"
ex2 = "twinkle_prof.wav"


def main():
    createPlot(ex1, ex2)


def getOnset(ex):
    s = source(ex, 0, hop_s)
    samplerate = s.samplerate

    o = onset("default", win_s, hop_s, samplerate)

    # list of onsets, in seconds
    onsets = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        if o(samples):
            # print("%f" % o.get_last_s())
            onsets.append(o.get_last_s())
        total_frames += read
        if read < hop_s:
            break
    # print len(onsets)
    return onsets


def getTimes(f):
    timePoints = getOnset(f)
    print(timePoints)
    time_np = np.array(timePoints)
    time_np = time_np - time_np[0]
    time_diff = np.diff(time_np)
    times = zip(time_np.tolist(), time_diff.tolist())
    return times


def createPlot(f1, f2):
    t1 = list(getTimes(f1))
    t2 = list(getTimes(f2))
    _, ax = plt.subplots()
    ax.broken_barh(t1, (15, 3), facecolors=('blue', 'red'))
    ax.broken_barh(t2,  (25, 3), facecolors=('red', 'blue'))
    ax.set_ylim(5, 40)
    # ax.set_xlim(0, 200)
    ax.set_xlabel('seconds since start')
    ax.set_yticks([15, 25])
    ax.set_yticklabels(['Professional', 'Student'])
    plt.show()
    return


if __name__ == "__main__":
    # execute only if run as a script
    main()
