# Capture.py
# Captures volume of sound signal to be used for frequency response analysis.

# LIB
import alsaaudio
import time
import audioop
from threading import Thread


class Capturer(Thread):
    def __init__(self, sample_rate=11025, period_size=882):
        Thread.__init__(self)
        self.SAMPLE_RATE = sample_rate
        self.PERIOD_SIZE = period_size
        self.PERIOD_DURATION = self.PERIOD_SIZE / self.SAMPLE_RATE
        self.sound_data_time = []
        self.sound_data_values = []
        self.sound_data = []

    def run(self):
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
        inp.setchannels(1)
        inp.setrate(self.SAMPLE_RATE)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp.setperiodsize(self.PERIOD_SIZE)

        while True:
            length, data = inp.read()
            if length:
                peak = audioop.minmax(data, 2)
                peak_to_peak = peak[1] - peak[0]
                timestamp = round(time.time(), 2)
                self.sound_data_time.append(timestamp)
                self.sound_data_values.append(peak_to_peak)
                self.sound_data.append([timestamp, peak_to_peak])
            time.sleep(self.PERIOD_DURATION / 2)

