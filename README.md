# Auto-Fan-Control
Script to automatically enable Extreme Cooling on the Lenovo Legion Y520 laptop.
Works in unison with hwinfo, an application used for monitoring various system parameters.

## Requirements
Requires Python 3.8.3 to be installed along with pynput.

## To setup
1. Install Python and pynput.
2. Download the package into a suitable directory.
3. Create an alert in hwinfo settings for CPU/GPU.
4. Enable run a command, and provide the link to the pythonw exe with argument as the downloaded script.<br/>
eg. C:/Python38/pythonw.exe C:/autoFanControl/autoFanControl.py %v
