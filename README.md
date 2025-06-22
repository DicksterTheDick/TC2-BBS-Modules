TC2-BBS-Modules: Extended Meshtastic BBS

This repository presents extended modules and features built upon the robust TC2-BBS-mesh project. It serves as a template and development hub for new functionalities, designed to enhance the capabilities and user experience of the Meshtastic-based Bulletin Board System.
Docker

The original TC²-BBS Meshtastic is available on Docker Hub! (This extended version would require a new Docker build and image, if desired).
Setup
Requirements

    Python 3.x

    Meshtastic

    pypubsub

Update and Install Git

sudo apt update
sudo apt upgrade
sudo apt install git

Installation

    Clone this repository:

cd ~
git clone https://github.com/DicksterTheDick/TC2-BBS-Modules.git
cd TC2-BBS-Modules

    Set up a Python virtual environment: ```sh
    python -m venv venv


3.  **Activate the virtual environment:** - On Windows:  

```sh
venv\Scripts\activate  

    On macOS and Linux:

source venv/bin/activate

    Install the required packages: ```sh
    pip install -r requirements.txt


5.  **Rename `example_config.ini`:**

```sh
mv example_config.ini config.ini

    Set up the configuration in config.ini: You'll need to open up the config.ini file in a text editor and make your changes following the instructions below. This project's config.ini includes new menu items for Games.

    [interface] If using type = serial and you have multiple devices connected, you will need to uncomment the port = line and enter the port of your device.

    Linux Example:

    port = /dev/ttyUSB0

    Windows Example:

    port = COM3

    If using type = tcp you will need to uncomment the hostname = 192.168.x.x line and put in the IP address of your Meshtastic device.

    [sync] Enter a list of other BBS nodes you would like to sync messages and bulletins with. Separate each by comma and no spaces as shown in the example below.

    You can find the nodeID in the menu under Radio Configuration > User for each node, or use this script for getting nodedb data from a device:

    Meshtastic-Python-Examples/print-nodedb.py at main · pdxlocations/Meshtastic-Python-Examples (github.com)

    Example Config:

    [interface]  
    type = serial  
    # port = /dev/ttyUSB0  
    # hostname = 192.168.x.x  

    [sync]  
    bbs_nodes = !f53f4abc,!f3abc123  

Running the Server

Run the server with:

python server.py

Be sure you've followed the Python virtual environment steps above and activated it before running. This server also features a configurable logging system in server.py for in-depth debugging and monitoring.
Command line arguments

$ python server.py --help

████████╗ ██████╗██████╗       ██████╗ ██████╗ ███████╗
╚══██╔══╝██╔════╝╚════██╗      ██╔══██╗██╔══██╗██╔════╝
   ██║   ██║      █████╔╝█████╗██████╔╝██████╔╝███████╗
   ██║   ██║     ██╔═══╝ ╚════╝██╔══██╗██╔══██╗╚════██║
   ██║   ╚██████╗███████╗      ██████╔╝██████╔╝███████║
   ╚═╝    ╚═════╝╚══════╝      ╚═════╝ ╚═════╝ ╚══════╝
Meshtastic Version

usage: server.py [-h] [--config CONFIG] [--interface-type {serial,tcp}] [--port PORT] [--host HOST] [--mqtt-topic MQTT_TOPIC]

Meshtastic BBS system

options:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        System configuration file
  --interface-type {serial,tcp}, -i {serial,tcp}
                        Node interface type
  --port PORT, -p PORT  Serial port
  --host HOST           TCP host address
  --mqtt-topic MQTT_TOPIC, -t MQTT_TOPIC
                        MQTT topic to subscribe

Automatically run at boot

If you would like to have the script automatically run at boot, follow the steps below:

    Edit the service file

    First, edit the mesh-bbs.service file using your preferred text editor. The 3 following lines in that file are what we need to edit:

    User=pi
    WorkingDirectory=/home/pi/TC2-BBS-Modules # MODIFIED: Reflects new folder name
    ExecStart=/home/pi/TC2-BBS-Modules/venv/bin/python3 /home/pi/TC2-BBS-Modules/server.py # MODIFIED: Reflects new folder name

    The file is currently setup for a user named 'pi' and assumes that the TC2-BBS-Modules directory is located in the home directory (which it should be if the earlier directions were followed).

    We just need to replace the 4 parts that have "pi" in those 3 lines with your username.

    Configuring systemd

    From the TC2-BBS-Modules directory, run the following commands:

    sudo cp mesh-bbs.service /etc/systemd/system/
    ```sh
    sudo systemctl enable mesh-bbs.service
    ```sh
    sudo systemctl start mesh-bbs.service

    The service should be started now and should start anytime your device is powered on or rebooted. You can check the status of the service by running the following command:

    sudo systemctl status mesh-bbs.service

    If you need to stop the service, you can run the following:

    sudo systemctl stop mesh-bbs.service

    If you need to restart the service, you can do so with the following command:

    sudo systemctl restart mesh-bbs.service

    Viewing Logs

    Viewing past logs:

    journalctl -u mesh-bbs.service

    Viewing live logs:

    journalctl -u mesh-bbs.service -f

Radio Configuration

Note: There have been reports of issues with some device roles that may allow the BBS to communicate for a short time, but then the BBS will stop responding to requests.

The following device roles have been working:

    Client

    Router_Client

Features (Extended)

This project extends the original TC2-BBS-mesh features with:

    Games Menu: A new menu offering interactive games.

        Blackjack Game: A text-based Blackjack game playable directly through Meshtastic.

    Mail System: Send and receive mail messages.

    Bulletin Boards: Post and view bulletins on various boards.

    Channel Directory: Add and view channels in the directory.

    Statistics: View statistics about nodes, hardware, and roles.

    Wall of Shame: View devices with low battery levels.

    Fortune Teller: Get a random fortune. Pulls from the fortunes.txt file. Feel free to edit this file remove or add more if you like.

Usage

You interact with the BBS by sending direct messages to the node that's connected to the system running the Python script. Sending any message to it will get a response with the main menu.

Make selections by sending messages based on the letter or number in brackets - Send M for [M]ail Menu for example.

A video of the original TC2-BBS-mesh in use is available on The Comms Channel's YouTube:
MAXIMUM CREDIT & Gratitude to The Comms Channel!

This project would not be possible without the foundational work of The Comms Channel and their fantastic TC2-BBS-mesh repository. Their innovative approach to creating a BBS over Meshtastic has been the invaluable starting point and core framework for these extensions. We extend immense gratitude for their vision, development, and ongoing contributions to the Meshtastic community.
Thanks (Original Project Credits)

Meshtastic:

Big thanks to Meshtastic and pdxlocations for the great Python examples:

python/examples at master · meshtastic/python (github.com)

pdxlocations/Meshtastic-Python-Examples (github.com)

JS8Call:

For the JS8Call side of things, big thanks to Jordan Sherer for JS8Call and the example API Python script
License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0), in direct compliance with the licensing of the original TC2-BBS-mesh project. See the LICENSE file for full details.
