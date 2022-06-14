# Overview #
 
[Discord](https://discord.com/invite/B7E5eXBz) | [Eye Tracker on iOS](https://apps.apple.com/us/app/eyeware-beam/id1538790472)
[Developers](https://beam.eyeware.tech/developers/) | [API Docs](https://docs.beam.eyeware.tech/) | [Eye Tracker SDK](https://eyewarecistorage.blob.core.windows.net/beam-sdk/BeamSDK-Windows64-1.1.0.zip)

The simple Python / QT web application reminds esports gamers to check the minimap in their favorite MOBA and MMOPRG PC games, including League of Legends, Dota 2,  Starcraft 2, and even games without a minimap like Overwatch, and Smite, helping you train checking gears, ammo, etc.

The app tracks a gamer’s visual attention with eye tracking to check whether the gamer has looked at the minimap within a specified amount of time. A visual or audio alarm alerts the gamer If he or she forgets to look at the minimap within the specified time.

![sample](https://user-images.githubusercontent.com/35032606/172874981-72aeff77-5bc7-4b42-9511-ea27b3c4cd90.gif)

## How does this tool help me become a better gamer? ##

Improving map awareness helps gamers and their teams coordinate or prevent enemy attacks, planning successful strategies, among other uses.

## Eye tracker ##

The current implementation uses the [Eyeware Beam](https://beam.eyeware.tech/developers/) iOS app.
The Eyeware Beam app  turns your Face ID-supported iPhone or iPad, with a built-in TrueDepth camera, into a reliable, precise, multi-purpose head and eye tracking device for a Windows PC . The eye tracker uses proprietary computer vision algorithms and machine perception AI technology that generates a robust eye tracking signal comparable to premium TrackIR or Tobii tracking devices. 

(_**Note**: access to the Eyeware Beam API is a paid feature_)

# I'm a gamer, not a developer, how do I use it? #

Assuming you are using Eyeware Beam as an eye tracker (see previous section), then follow these instructions:

1.  Download the latest Release here: https://github.com/kenneth-ew/MOBA-Minimap-Awareness-Trainer/releases
2.  Unzip and run _minimap_trainer.exe_
3.  If the eye tracker is running and API accessible (see previous section), then the user interface should display "Connected to eye tracker..."
4.  Click on _Set minimap location_ allowing you to indicate where the minimap is in your game by a click-move-and-release action. Press Esc when ready.
![image](https://user-images.githubusercontent.com/35032606/173069164-1acd2d4a-e1d2-4a6f-9091-3b2f764cc3fd.png)
5.  Configure your alarm/trainer settings:
    1. Set the "Alarm timeout (seconds)", which is the time you will be allowed not to look at the minimap, before an alarm is triggered. Everytime you look at the minimap, the time count is reset and no alarm is triggered. So keep looking at the minimap once in a while!
    2. The volume is the volume of the alarm. You can also check/uncheck if you want a visual indicator (a flashing red square on the minimap location)

![image](https://user-images.githubusercontent.com/35032606/173070003-d13b0154-f393-4d19-9d38-bb264fbe481e.png)

6.  Click on Start

# How to develop and set it up? ###

## Development environment configuration

You can use [conda](https://docs.conda.io/en/latest/miniconda.html) to create a minimum python environment by
running the following in your command line.

     conda create --name minimap_env
     conda activate minimap_env
     conda install python=3.6 pyinstaller -y
     pip install PySide6

## Requirements

You need to download the Eyeware Beam SDK from the same [website](https://beam.eyeware.tech/developers/)
and further configure your PYTHONPATH as explained in the [documentation](https://docs.beam.eyeware.tech/getting_started.html).
Alternative, you can unzip the folder and copy the contents of API/python on the root of this repo.

(_**Note**: access to the Eyeware Beam API is a paid feature_)

## Running

To run from the source, in a command line run:

     conda activate minimap_env
     python minimap_trainer.py

## Create an executable

To create an executable, simply run:

     pyinstaller minimap_trainer.py --noconfirm --noconsole --add-data="alarm.mp3;."

### Credits

- Sound effects obtained from https://www.zapsplat.com
- Inspiration from https://www.youtube.com/watch?v=XR11BkzZ8NU but, I definitely do not recommend tazing people ;)
