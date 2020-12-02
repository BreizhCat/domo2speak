import argparse
import logging
import time
import pychromecast
import sys
import os
from gtts import gTTS, gTTSError

parser = argparse.ArgumentParser(prog="domo2speak")
group = parser.add_argument_group(title="Basics Arguments")
group.add_argument("-v", "--verbose", help = "Affichage d'une log", action="store_true")
group.add_argument("-d", "--device",  help = "Nom du Chromecast", default=None)

group = parser.add_argument_group(title="gTTS Arguments", description="Value for gTTS generation")
group.add_argument("-t", "--text", help = "Texte à communiquer", default=None, required = True)
group.add_argument("-f", "--folder",  help = "Dossier de sauvegarde", default=None, required = True)

args = parser.parse_args()

class domo2speak():
    "Classe de gestion des messages à envoyer depuis Domoticz (ou autre) vers l'un des Google Home"

    FILE_NAME = "media.mp3"
    BASE_ROOT = "http://www.breizhcat/"

    def __init__(self, args):
        self.debug  = args.verbose
        if self.debug:
            logging.basicConfig(format='%(levelname)s:%(message)s', level = logging.INFO)
        
        self.logging = logging.getLogger()        

        self.device = args.device
        self.text   = args.text
        self.folder = args.folder

        self.output_media = ""

        if not os.path.exists(self.folder):
            raise Exception("Error:", "Folder doesn't exist !")

        if self.folder.endswith("\\"):
            self.output_media = self.folder + domo2speak.FILE_NAME
        else:
            self.output_media = self.folder + "\\" + domo2speak.FILE_NAME

        self.is_error = False


    def log(self, message, level = logging.INFO):
        if self.debug:
            if level == logging.INFO:
                self.logging.info(message)

            if level == logging.ERROR:
                self.logging.error(message)
                self.is_error = True



    def create_audio_message(self):
        if self.is_error:
            return

        self.log("__ CREATE_AUDIO_MESSAGE")
        self.log("____ Media name: " + self.output_media)

        if os.path.exists(self.output_media):
            self.log("____ Delete previous media")
            os.remove(self.output_media)
        else:
            self.log("____ No previous media found")

        try:
            tts = gTTS(text=self.text, lang="fr")
            self.log("____ gTTS request works!")
            tts.save(self.output_media)
            self.log("____ Media saved !")
        except AssertionError:
            self.log("____ AssertionError: Text is empty", logging.ERROR)
        except ValueError:
            self.log("____ ValueError: Language doesn't exist", logging.ERROR)
        except RuntimeError:
            self.log("____ RuntimeError: Error during gTTS request", logging.ERROR)
        except gTTSError:
            self.log("____ An issue occured during saving media", logging.ERROR)
    
    def send_to_device(self):
        if self.is_error:
            return 
        self.log("__ SEND_TO_DEVICE")
        
        cast = self._get_cast_device()
        cast.wait()
        old_volume = cast.status.volume_level
        self.log("____ Old Volume Value:" + str(old_volume))
        cast.play_media(self.BASE_ROOT + self.FILE_NAME, "audio/mp3")
        #cast.set_volume(100)
        cast.media_controller.block_until_active()
        cast.media_controller.play()
        cast.set_volume(old_volume)
        cast.media_controller.stop()
        cast.quit_app()
       
    def _get_cast_device(self):
        if self.is_error:
            return 
        self.log("__ _GET_CAST_DEVICE")
        devices_list = []
        self.log("____ Device: " + self.device)
        devices_list.append(self.device)

        devices, browser = pychromecast.get_listed_chromecasts(friendly_names = devices_list)
        pychromecast.stop_discovery(browser)

        return devices[0]
        

run = domo2speak(args)
run.create_audio_message()
run.send_to_device()
sys.exit(0)