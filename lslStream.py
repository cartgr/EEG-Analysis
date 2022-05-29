"""
Set-up: 
    1. connect Muse using Petal Metrics and start stream
    2. Run this script

This script is the beginning of a training data generator
"""

import pylsl
import time
import pyautogui
import numpy as np
import pandas as pd
from datetime import datetime
from pygame import mixer

cols = ["cursor x", "cursor y", "ch1", "ch2", "ch3", "ch4", "ch5"]
data = []

time.sleep(2) # time to reposition cursor

start = time.time()
run_time = 100

streams = pylsl.resolve_stream('name', 'PetalStream_eeg')
inlet = pylsl.StreamInlet(streams[0])
while True:
    cur_time = time.time()
    if cur_time < start + run_time:
        sample, _ = inlet.pull_sample()
        ch1, ch2, ch3, ch4, ch5 = sample
        x, y = pyautogui.position().x, pyautogui.position().y
        data.append([x, y, ch1, ch2, ch3, ch4, ch5])
    else:
        break

df = pd.DataFrame(data, columns = cols)

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H.%M.%S")

file_name = "train_files/"+dt_string+".csv"
df.to_csv(file_name, index=False)

mixer.init() 
beep=mixer.Sound("bell.wav")
beep.play()