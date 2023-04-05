# np_audio_control

[![Python
Versions](https://img.shields.io/pypi/pyversions/np_audio_control.svg)](https://pypi.python.org/pypi/np-audio-control/)

Tools for remote control of Windows system audio on Mindscope Neuropixels and Behavior rigs.

Uses SetVol v3.4 (https://www.rlatour.com/setvol/)


## Install
```shell
python -m pip install np_audio_control
```


## Basic usage
```python
>>> from np_audio_control import mute, unmute, set_volume, get_volume

>>> host = 'W10LTPC2BC51P'

# interact with default audio device 
>>> mute(host)
>>> unmute(host)
>>> set_volume(50, host)
>>> get_volume(host)
50

# interact with specific device (see SetVol `device name` argument)
>>> device = 'Speakers (Realtek USB2.0 Audio)'
>>> mute(host, device)
>>> set_volume(50, host, device)


# send any command to SetVol
>>> from np_audio_control import send_setvol_cmd
>>> send_setvol_cmd(host, 'beep')
```
