#!/usr/bin/python3
#
# Analyzer.py
# Analyzes frequency response of an audio device.

# LIB
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from math import log
# USR
from Generator import Generator
from Capturer import Capturer
from Pitch import pitch

CLIP_TIME = 0.05  # number of seconds to clip from sound sample to analyze
STEP_TIME =1.0  # length of one musical note in seconds
FREQ_START = 13.75  # frequency to start from, 13.75Hz is A-1
STEPS_NUM = 130
# FREQ_START = 880
# STEPS_NUM = 10


def filter_frequency_data(freq, gen_data, rec_data, clip_time=0.05,
        freq_threshold=1.02):
    filt1 = gen_data[:, 1] > (freq / freq_threshold)
    filtered1 = gen_data[filt1, :]
    filt2 = filtered1[:, 1] < (freq * freq_threshold)
    filtered2 = filtered1[filt2, :]

    timestamp_start = min(filtered2[0][0], filtered2[1][0]) + clip_time
    timestamp_end = max(filtered2[0][0], filtered2[1][0]) - clip_time

    filt3 = rec_data[:, 0] > timestamp_start
    filtered3 = rec_data[filt3, :]
    filt4 = filtered3[:, 0] < timestamp_end
    filtered4 = filtered3[filt4, :]
    return filtered4

def main():
    print('Elektroteror sound analyzer.')
    worker_generator = Generator(freq_start=FREQ_START, steps_num=STEPS_NUM,
            step_time=STEP_TIME)
    worker_capturer = Capturer()
    worker_capturer.daemon = True
    print('Starting capturer...')
    worker_capturer.start()
    print('Starting generator...')
    worker_generator.start()
    worker_generator.join()

    plt.plot(worker_generator.sound_data_time, worker_generator.sound_data_values, 'b-',
             worker_capturer.sound_data_time, worker_capturer.sound_data_values, 'r-')
    plt.title('Audio frequency response - raw data')
    plt.xlabel('time')
    plt.show()

    gen_data = np.array(worker_generator.sound_data)
    rec_data = np.array(worker_capturer.sound_data)

    multiplier = 2 ** (1.0/12)
    freqs = []
    levels = []
    freqs_labels = []

    for step in range(int(STEPS_NUM)):
        freq = round(FREQ_START * (multiplier ** step), 2)
        freqs.append(freq)
        level_data = filter_frequency_data(freq, gen_data, rec_data)
        level = np.average(level_data, 0)[1]
        level_log = 10 * log(level/65536, 10)
        levels.append(level_log)
        label = '%.f' % freq
        label += ' | ' + pitch(freq)
        freqs_labels.append(label)

    plt.plot(freqs, levels, 'g-')
    plt.title('Frequency response')
    plt.xlabel('frequency')
    plt.ylabel('gain/normalized response (dB)')
    plt.xscale('log')
    plt.xticks(freqs, rotation=90)
    plt.axes().set_xticklabels(freqs_labels, rotation='vertical')
    # plt.axes().xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()

