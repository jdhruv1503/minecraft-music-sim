import os
import random
import time
from playsound import playsound


MINECRAFT_MUSIC_PATH = "C:\\Users\\Dhruv\\Music\\MinecraftOST"

os.chdir(MINECRAFT_MUSIC_PATH)
tracks = os.listdir()
playlist = {}

for track in tracks:
    trackfull = "C:\\Users\\Dhruv\\Music\\MinecraftOST\\" + track
    playlist[random.randrange(1,10000)] = trackfull

order = list(playlist.keys())
order.sort()

while True:
    for index in order:
        trackname = playlist[index][trackfull.index(r"-")+1:-4]
        print("Now playing:",trackname)
        playsound(playlist[index])
        
        waittime = random.randint(20,100)
        print("Now waiting:",waittime,"seconds")
        time.sleep(waittime)

        
