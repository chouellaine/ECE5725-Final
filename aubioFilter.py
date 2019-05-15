"""
aubioFilter.py uses the aubio library package to identify notes,
start times and note velocity for each note. Note velocity is a measure
of how rapidly and forcefully a key was pressed.
Based on the data, it displays the performance tracking of the two audio files

IMPORTANT:
first file input must be student's
second file input must be prof's

"""
import os
from aubio import source, notes, onset, digital_filter, sink
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm

win_s = 512                 # fft size
hop_s = win_s // 2          # hop size

"""createFilterfile creates a new file name for the filtered audio file"""


def createFilterFile(f):
    return "filtered_" + f


"""applyFilter applies an A-weighting filter to the audio file"""


def applyFilter(path, target):
        # open input file, get its samplerate
    s = source(path)
    samplerate = s.samplerate

    # create an A-weighting filter
    f = digital_filter(7)
    f.set_a_weighting(samplerate)

    # create output file
    o = sink(target, samplerate)

    total_frames = 0
    while True:
        # read from source
        samples, read = s()
        # filter samples
        filtered_samples = f(samples)
        # write to sink
        o(filtered_samples, read)
        # count frames read
        total_frames += read
        # end of file reached
        if read < s.hop_size:
            break


"""
getOnset gives the start time for each identified note in seconds.
f is the filename of the audio file. 
"""


def getOnset(f):
    s = source(f, 0, hop_s)
    samplerate = s.samplerate

    o = onset("default", win_s, hop_s, samplerate)
    notes_o = notes("default", win_s, hop_s, samplerate)

    # list of onsets, in seconds
    onsets = []
    vel = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        if o(samples):
            # print("%f" % o.get_last_s())
            # print("%f" % o.get_threshold())
            onsets.append(o.get_last_s())

        new_note = notes_o(samples)
        if (new_note[0] != 0):
            vel.append(new_note[1])
        total_frames += read
        if read < hop_s:
            break
    # print len(onsets)

    return onsets, vel


"""
mapVel maps note velocity to an RGBA value on the viridis colormap.
v1 and v2 are the note velocities for student and professional, respectively
"""


def mapVel(v1, v2):
    minima = min(v2)
    maxima = max(v2)
    norm = mpl.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.viridis)
    c1 = []
    c2 = []
    for x in v1:
        c1.append(mapper.to_rgba(x))

    for x in v2:
        c2.append(mapper.to_rgba(x))

    """def mapVel_helper(v, c, i):
        if i >= len(v):
            print(repr(c))
            return tuple(c)
        else:
            x = mapper.to_rgba(v[i])
            c.append(x)
            i += 1
            mapVel_helper(v, c, i)

    c1 = mapVel_helper(v1, [], 0)
    c2 = mapVel_helper(v2, [], 0)"""
    print(repr(c1))
    print(repr(c2))
    return c1, c2


"""
getTimes returns the adjusted start times and end times for each note in [t]
"""


def getTimes(t):
    # print(timePoints)
    time_np = np.array(t)
    time_np = time_np - time_np[0]
    time_diff = np.diff(time_np)
    times = zip(time_np.tolist(), time_diff.tolist())
    return times


"""
getInfo gathers all the information needed for the audio files, f1 and f2
"""


def getInfo(f1, f2):
    t1, v1 = getOnset(f1)
    t1_end = getTimes(t1)
    t2, v2 = getOnset(f2)
    t2_end = getTimes(t2)
    c1, c2 = mapVel(v1, v2)
    return t1_end, t2_end, c1, c2


def createPlot(f1, f2):
    i1, i2, c1, c2 = getInfo(f1, f2)
    c1_tup = tuple(c1)
    c2_tup = tuple(c2)
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.broken_barh(list(i1), (10, 3), facecolors=c1_tup)
    ax2.broken_barh(list(i2),  (10, 3), facecolors=c2_tup)
    # ax.set_ylim(0,1)
    # ax.set_xlim(0, 200)
    ax1.title.set_text('Student')
    ax2.title.set_text('Professional')
    ax1.set_yticklabels([])
    ax2.set_yticklabels([])
    ax2.set_xlabel('seconds since start')
    plt.xticks([], " ")
    plt.show()
    cur_axes = plt.gca()
    cur_axes.axes.get_yaxis().set_visible(False)
    cur_axes.axes.get_yaxis().set_ticks([])
    cur_axes.axes.get_yaxis().set_ticklabels([])
    return


def main(f1, f2):
    # FIRST FILE MUST BE STUDENT's, SECOND FILE MUST BE PROF's
    filter_1 = createFilterFile(f1)
    filter_2 = createFilterFile(f2)
    applyFilter(f1, filter_1)
    applyFilter(f2, filter_2)
    createPlot(filter_1, filter_2)
    os.remove(filter_1)
    os.remove(filter_2)


if __name__ == "__main__":
    # fecute only if run as a script
    # FIRST FILE MUST BE STUDENT's, SECOND FILE MUST BE PROF's
    main('twinkle_student.wav', 'twinkle_prof.wav')
