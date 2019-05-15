"""
analysis.py uses the aubio library package to identify notes,
start times and note velocity for each note. Note velocity is a measure
of how rapidly and forcefully a key was pressed.
Based on the data, it displays the performance tracking of the two audio files

IMPORTANT:
first file input must be student's
second file input must be prof's

"""
import os
from aubio import source, notes, onset, digital_filter, sink, pitch
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm

win_s = 512  # fft size
hop_s = 512 // 2  # hop size

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

    tolerance = 0.8
    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("Hz")
    pitch_o.set_tolerance(tolerance)

    o = onset("default", win_s, hop_s, samplerate)
    notes_o = notes("default", win_s, hop_s, samplerate)

    # list of onsets, in seconds
    onsets = []
    vel = []
    pitches = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        p = pitch_o(samples)[0]
        new_note = notes_o(samples)
        t = total_frames/float(samplerate)

        if o(samples) and p > 0:
            onsets.append(o.get_last_s())
            pitches.append(p)

        if new_note[0] != 0:
            vel.append(new_note[1])
        total_frames += read
        if read < hop_s:
            break
    return onsets, vel, pitches


"""
mapVel maps note velocity to an RGBA value on the viridis colormap.
v1 and v2 are the note velocities for student and professional, respectively
"""


def mapVel(v1, v2):
    minima = min(v2)
    maxima = max(v2)
    norm = mpl.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.viridis)
    c1 = [mapper.to_rgba(i) for i in v1]
    c2 = [mapper.to_rgba(i) for i in v2]
    return c1, c2


"""
getTimes returns the adjusted start times and end times for each note in [t]
"""


def getTimes(t):
    time_np = np.array(t)
    time_diff = np.diff(time_np)
    return time_np.tolist(), time_diff.tolist()


"""
getInfo gathers all the information needed for the audio files, stu and prof.
Returns:
-[t1_end] and [t2_end]: array of start and end times in sec of each note
- [c1] and [c2]: array of note velocity
"""


def getInfo(stu, prof):
    t1, v1, p1 = getOnset(stu)
    t1_s, t1_e = getTimes(t1)
    t2, v2, p2 = getOnset(prof)
    t2_s, t2_e = getTimes(t2)
    c1, c2 = mapVel(v1, v2)
    return zip(t1_s, t1_e, c1, p1), zip(t2_s, t2_e, c2, p2)


def analyze(stu, prof):
    # FIRST FILE MUST BE STUDENT's, SECOND FILE MUST BE PROF's
    stud_filt = createFilterFile(stu)
    prof_filt = createFilterFile(prof)
    applyFilter(stu, stud_filt)
    applyFilter(prof, prof_filt)
    result = getInfo(stud_filt, prof_filt)
    for file in os.listdir(os.getcwd()):
        if file.startswith("filtered"):
            os.remove(file)
    return result


if __name__ == '__main__':
    analyze('twinkstud.wav', 'twinkprof.wav')
