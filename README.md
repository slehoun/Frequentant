Frequentant
-----------

A frequency response analyser. Utilizes `alsaaudio` for input and `simpleaudio` for output. Generates sine waves in musical notes frequencies on the fly and plays them back while another thread captures them. Results are then analyzed and frequency response [bode plot](https://en.wikipedia.org/wiki/Bode_plot) is generated.

### External dependencies
`matplotlib`, `numpy`, `alsaaudio`,`simpleaudio`

See `requirements.txt`.

### Usage
Microphone/audio ouput device combination needs to have volumes adjusted.
Script will play sound at maximum level. To avoid clipping, maximum volume
needs to be lowered so it barely touches maximum level when recorded. The exact volume level is different for each
microphone/audio device combination. This might be automated in future
releases.

### Sample output
This is what frequency response of Marshall Major II headphones looks like:

![Marshall Major II frequency response](/images/marshall-major-freq-resp.png)

