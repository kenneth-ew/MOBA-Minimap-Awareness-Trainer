# Overview #

The minimap trainer is a simple python/Qt application that reminds you about checking your minimap
while playing games like League of Legends, Starcraft, or other MOBA games. 

It uses eye tracking to check whether you have checked your minimap with certain frequency and, if you
haven't, it emits a visual or audio alarm.

![sample](https://user-images.githubusercontent.com/35032606/172874981-72aeff77-5bc7-4b42-9511-ea27b3c4cd90.gif)

# Eye tracking #

The current implementation uses the [Eyeware Beam](https://beam.eyeware.tech/developers/) iOS application
that transforms iPhones or iPads having faceid into an eye tracker device for a PC.

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
