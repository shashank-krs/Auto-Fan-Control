# Auto Fan Control
Script to automatically enable Extreme Cooling on the Lenovo Legion Y520 laptop.
Works in unison with hwinfo, an application used for monitoring various system hardware parameters.

## Requirements
Requires Python 3.8.3 to be installed along with pynput.

## Configuration
The following paramters can be configured in the json configuration file-
1. Upper temperature threshold - the temperature at which Extreme Cooling has to be enabled.
2. Output file size limit - the size limit of the output file to avoid the file growing too large and causing performance issues.
3. Previous temperatures check - the number of previously recorded temperatures to check before switching off Extreme Cooling.

## Setup
1. Install Python and pynput.
2. Download the package into a suitable directory.
3. Create an alert in hwinfo settings for CPU/GPU.
4. Enable run a command, and provide the link to the pythonw exe with argument as the downloaded script.<br/>
eg. C:/Python38/pythonw.exe C:/autoFanControl/autoFanControl.py %v
