================================================================================
TC2-BBS-Modules: Extended Meshtastic BBS
================================================================================

This repository presents extended modules and features built upon the robust 
TC2-BBS-mesh project. It serves as a template and development hub for new 
functionalities, designed to enhance the capabilities and user experience of the 
Meshtastic-based Bulletin Board System.

================================================================================
Docker
================================================================================

The original TC²-BBS Meshtastic is available on Docker Hub! (This extended 
version would require a new Docker build and image, if desired).

================================================================================
Setup
================================================================================

Requirements:
- Python 3.x
- Meshtastic
- pypubsub

Update and Install Git:
sudo apt update
sudo apt upgrade
sudo apt install git

Installation:
1. Clone this repository:
   
   cd ~
   git clone https://github.com/DicksterTheDick/TC2-BBS-Modules.git
   cd TC2-BBS-Modules

2. Set up a Python virtual environment:
   python -m venv venv

3. Activate the virtual environment:
   - On Windows: venv\Scripts\activate
   - On macOS and Linux: source venv/bin/activate

4. Install the required packages:
   pip install -r requirements.txt

5. Rename example_config.ini:
   mv example_config.ini config.ini

6. Set up the configuration in config.ini:
   Open config.ini in a text editor and make your changes following the 
   instructions below. This project's config.ini includes new menu items for Games.

================================================================================
Configuration Details
================================================================================

[interface]
If using type = serial and you have multiple devices connected, you will need to 
uncomment the port = line and enter the port of your device.

Linux Example:
port = /dev/ttyUSB0

Windows Example:
port = COM3

If using type = tcp you will need to uncomment the hostname = 192.168.x.x line 
and put in the IP address of your Meshtastic device.

[sync]
Enter a list of other BBS nodes you would like to sync messages and bulletins 
with. Separate each by comma and no spaces as shown in the example below.

You can find the nodeID in the menu under Radio Configuration > User for each 
node, or use this script for getting nodedb data from a device:
Meshtastic-Python-Examples/print-nodedb.py at main · pdxlocations/Meshtastic-Python-Examples

Example Config:
[interface]
type = serial
# port = /dev/ttyUSB0
# hostname = 192.168.x.x

[sync]
bbs_nodes = !f53f4abc,!f3abc123

================================================================================
Running the Server
================================================================================

Run the server with:
python server.py

Be sure you've followed the Python virtual environment steps above and activated 
it before running. This server also features a configurable logging system in 
server.py for in-depth debugging and monitoring.

Command line arguments:
$ python server.py --help

████████╗ ██████╗██████╗       ██████╗ ██████╗ ███████╗
╚══██╔══╝██╔════╝╚════██╗      ██╔══██╗██╔══██╗██╔════╝
   ██║   ██║      █████╔╝█████╗██████╔╝██████╔╝███████╗
   ██║   ██║     ██╔═══╝ ╚════╝██╔══██╗██╔══██╗╚════██║
   ██║   ╚██████╗███████╗      ██████╔╝██████╔╝███████║
   ╚═╝    ╚═════╝╚══════╝      ╚═════╝ ╚═════╝ ╚══════╝
Meshtastic Version

usage: server.py [-h] [--config CONFIG] [--interface-type {serial,tcp}] [--port PORT] [--host HOST] [--mqtt-topic MQTT_TOPIC]

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

================================================================================
Automatically run at boot
================================================================================

1. Edit the service file:
   Edit the mesh-bbs.service file using your preferred text editor. The 3 
   following lines in that file are what we need to edit:

   User=pi
   WorkingDirectory=/home/pi/TC2-BBS-Modules
   ExecStart=/home/pi/TC2-BBS-Modules/venv/bin/python3 /home/pi/TC2-BBS-Modules/server.py

   Replace "pi" with your username in all 4 locations.

2. Configuring systemd:
   From the TC2-BBS-Modules directory, run:
   sudo cp mesh-bbs.service /etc/systemd/system/
   sudo systemctl enable mesh-bbs.service
   sudo systemctl start mesh-bbs.service

3. Service management:
   - Check status: sudo systemctl status mesh-bbs.service
   - Stop service: sudo systemctl stop mesh-bbs.service
   - Restart service: sudo systemctl restart mesh-bbs.service

4. Viewing Logs:
   - Past logs: journalctl -u mesh-bbs.service
   - Live logs: journalctl -u mesh-bbs.service -f

================================================================================
Radio Configuration
================================================================================

Note: There have been reports of issues with some device roles. The following 
device roles have been working:
- Client
- Router_Client

================================================================================
Features (Extended)
================================================================================

This project extends the original TC2-BBS-mesh features with:
- Games Menu: A new menu offering interactive games
  - Blackjack Game: A text-based Blackjack game
- Mail System: Send and receive mail messages
- Bulletin Boards: Post and view bulletins
- Channel Directory: Add and view channels
- Statistics: View statistics about nodes
- Wall of Shame: View devices with low battery
- Fortune Teller: Get a random fortune (editable via fortunes.txt)

================================================================================
Usage
================================================================================

Interact with the BBS by sending direct messages to the node running the script.
Send any message to get the main menu. Make selections by sending messages based 
on the letter/number in brackets (e.g., send "M" for [M]ail Menu).

================================================================================
Credits
================================================================================

MAXIMUM CREDIT & Gratitude to The Comms Channel!
This project builds upon their TC2-BBS-mesh repository.

Meshtastic:
Thanks to Meshtastic and pdxlocations for Python examples:
python/examples at master · meshtastic/python
pdxlocations/Meshtastic-Python-Examples

JS8Call:
Thanks to Jordan Sherer for JS8Call and example API Python script

================================================================================
License
================================================================================

GNU General Public License v3.0 (GPL-3.0)
