import argparse
import logging
import time
import pychromecast
import sys
from gtts import gTTS

parser = argparse.ArgumentParser(prog="domo2speak")
group = parser.add_argument_group(title="Basics Arguments")
group.add_argument("-v", "--verbose", help = "Affichage d'une log", action="store_true")
group.add_argument("-d", "--device",  help = "Nom du Chromecast", default=None)

group = parser.add_argument_group(title="gTTS Arguments", description="Value for gTTS generation")
group.add_argument("-t", "--text", help = "Texte à communiquer", default=None, required = True)
group.add_argument("-f", "--folder",  help = "Dossier de sauvegarde", default=None, required = True)

args = parser.parse_args()

class myLogger():
    def __init__(self, value):
        self.status = value
        self.logger = logging.getLogger()

        if value:
            logging.basicConfig(level = logging.DEBUG)

    def info(self, msg):
        if self.status:
            self.logger.info(msg)

logger = myLogger(args.verbose)


friendly_names = []
if args.device:
    friendly_names.append(args.device)

    devices, browser = pychromecast.get_listed_chromecasts(friendly_names = friendly_names)
    pychromecast.stop_discovery(browser)

    if args.text:
        tts = gTTS(text=args.text, lang="fr")
        tts.save(args.folder + 'media.mp3')

    cast = devices[0]

    cast.wait()

    if not cast.is_idle:
        print("Killing current running app")
    
    old_volume = cast.status.volume_level
    print(old_volume)
    cast.play_media("http://www.breizhcat.fr/media.mp3", "audio/mp3")
    cast.set_volume(100)
    cast.media_controller.block_until_active()
    cast.media_controller.play()
    cast.set_volume(old_volume)
    cast.media_controller.stop()
    cast.quit_app()
else:
    print("Veuillez indiquer un device name")
