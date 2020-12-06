# domo2speak

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

Send notification through domoticz to Google Home

Test with Python 3.8.2

## HOW TO
```shell
$>python domo2speak.py -v
$>usage: domo2speak [-h] [-v] -d DEVICE [-s SOUND] -t TEXT -f FOLDER

optional arguments:
  -h, --help            show this help message and exit

Basics Arguments:
  -v, --verbose         Affichage d'une log
  -d DEVICE, --device DEVICE
                        Nom du Chromecast
  -s SOUND, --sound SOUND
                        Volume

gTTS Arguments:
  Value for gTTS generation

  -t TEXT, --text TEXT  Texte à communiquer
  -f FOLDER, --folder FOLDER
                        Dossier de sauvegarde
```

Please also update Python code with the folder where the configuration is `__FULL_PATH__`
And finally configure the configuration file `conf.json` by renamming the file `conf.json.model`

```json
{
    "file_name":"media.mp3",
    "root_url":"url_to_access_to_media_file"
}
```

