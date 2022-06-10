# Overview #

The minimap trainer is a simple python/Qt application that reminds you about checking your minimap
while playing games like League of Legends, Starcraft, or other MOBA games. 

It uses eye tracking to check whether you have checked your minimap with certain frequency and, if you
haven't, it emits a visual or audio alarm.

![sample](https://user-images.githubusercontent.com/35032606/172874981-72aeff77-5bc7-4b42-9511-ea27b3c4cd90.gif)

# Eye tracker #

The current implementation uses the [Eyeware Beam](https://beam.eyeware.tech/developers/) iOS application
that transforms iPhones or iPads, supporting faceid, into an eye tracker device for a Windows PC (_**Note**: access to the API is a paid feature_). 

# I'm a gamer, not a developer, how do I use it? #

Assuming you are using Eyeware Beam as an eye tracker (see previous section), then follow these instructions:

1.  Download the latest Release here: https://github.com/kenneth-ew/minimap_trainer/releases
2.  Unzip and run _minimap_trainer.exe_
3.  If the eye tracker is running and API accessible (see previous section), then the user interface should display "Connected to eye tracker..."
4.  Click on _Set minimap location_ allowing you to indicate where the minimap is in your game by a click-move-and-release action. Press Esc when ready.
![image](https://user-images.githubusercontent.com/35032606/173069164-1acd2d4a-e1d2-4a6f-9091-3b2f764cc3fd.png)
5.  Configure your alarm/trainer settings:
    1. Set the "Alarm timeout (seconds)", which is the time you will be allowed not to look at the minimap, before an alarm is triggered. Everytime you look at the minimap, the time count is reset and no alarm is triggered. So keep looking at the minimap once in a while!
    2. The volume is the volume of the alarm. You can also check/uncheck if you want a visual indicator (a flashing red square on the minimap location)
![image](https://user-images.githubusercontent.com/35032606/173070003-d13b0154-f393-4d19-9d38-bb264fbe481e.png)
6.  Click on Start

# How do I get set up? ###

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

_**Note**: an active subscription is needed to access Eyeware Beam's API._

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
