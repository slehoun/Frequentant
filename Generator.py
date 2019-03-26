# Generator.py
# Generates and plays back sound signals to be used for frequency response
# analysis.
# Signals used are sine waves in frequencies of musical notes.

# LIB
import numpy as np
import simpleaudio as sa
import time
from threading import Thread
# USR
from Pitch import pitch


class Generator(Thread):
    def __init__(self, freq_start=880, steps_num=10, step_time=0.5):
        Thread.__init__(self)
        self.sound_data_time = []
        self.sound_data_values = []
        self.sound_data = []
        self.freq_start = freq_start
        self.steps_num = steps_num
        self.step_time = step_time
        pass

    @staticmethod
    def generate_sinewave(frequency=1000, sample_rate=44100, duration=1.0, amplitude=1.0):
        time_stamps = np.linspace(0, duration, duration * sample_rate, False)
        sine_wave = np.sin(frequency * time_stamps * 2 * np.pi)
        audio_sine_wave = sine_wave * amplitude * 32767 / np.max(np.abs(sine_wave))
        audio_sine_wave = audio_sine_wave.astype(np.int16)
        return audio_sine_wave

    def run(self):
        multiplier = 2 ** (1.0/12)

        for step in range(int(self.steps_num)):
            n = int(20 * step/self.steps_num)
            progress_bar = ' [' + n * '=' + ((20 - n) * ' ') + ']'
            freq = round(self.freq_start * (multiplier ** step), 2)
            note = pitch(freq)
            print(progress_bar + ' Playing tone %s with frequency %.1fHz (%d of %d).    '\
                            % (note, freq, step, int(self.steps_num)), end='\r')
            wave = Generator.generate_sinewave(frequency=freq,
                    duration=self.step_time)

            start = round(time.time(), 2)
            self.sound_data_time.append(start - 0.01)
            self.sound_data_values.append(0)
            self.sound_data.append([start - 0.01, 0])
            self.sound_data_time.append(start)
            self.sound_data_values.append(freq)
            self.sound_data.append([start, freq])

            play_object = sa.play_buffer(wave, 1, 2, 44100)
            play_object.wait_done()

            end = round(time.time(), 2)
            self.sound_data_time.append(end)
            self.sound_data_values.append(freq)
            self.sound_data.append([end, freq])
            self.sound_data_time.append(end + 0.01)
            self.sound_data_values.append(0)
            self.sound_data.append([end + 0.01, 0])
            time.sleep(0.25)

