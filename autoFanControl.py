from pynput.keyboard import Key, Controller
import os,sys
import time as systime
import json
from subprocess import check_output

currentTemp = int(sys.argv[1])
homeDir = os.getcwd()
dataDir = homeDir + "/data/"
logsDir = homeDir + "/logs/"
configDir = homeDir + "/config/"
scriptConfig = configDir + "configAutoFanControl.json"
outputFile = dataDir + "temperatureList.txt"
indicatorFile = dataDir + "coolingIndicator.txt"
logFile = logsDir + "autoFanControl.log"

# Reading thresholds
with open(scriptConfig, 'r') as config:
	configData = json.load(config)
outputFileSizeLimit = int(configData['fileSizeThreshold'])
upperTemperatureLimit = int(configData['temperatureThreshold'])

def logMessage(message,mode=None):
	time = systime.localtime()
	current_time = systime.strftime("%d-%b-%Y %H:%M:%S", time)
	try:
		with open(logFile,"a+") as f:
			if mode is None:
				f.write(current_time+': '+'INFO: '+str(message)+"\n")
			else:
				f.write("\n")
		f.close()
	except Exception as e:
		logMessage("Unexpected error found in logMessage, exiting")
		logMessage(e)
		sys.exit(1)

def readConfig(scriptSetting):
	try:
		with open(scriptConfig, 'r') as config:
			configData = json.load(config)
		return configData[scriptSetting]
	except IOError:
		logMessage("Configuration is missing, exiting")
		sys.exit(1)
	except Exception as e:
		logMessage("Script failed due to an unexpected error")
		logMessage(e)
		sys.exit(1)

def runExtremeCooling():
	try:
		keyboard = Controller()
		keyboard.press(Key.ctrl.value)
		keyboard.press(Key.shift.value)
		keyboard.press('0')
		systime.sleep(0.1)
		keyboard.release('0')
		keyboard.release(Key.shift.value)
		keyboard.release(Key.ctrl.value)
	except Exception as e:
		logMessage("Script failed due to an unexpected error")
		logMessage(e)
		sys.exit(1)

def checkPreviousTemps():
	try:
		with open(outputFile) as f:
			tempsArray=f.readlines()
		tempsArray = list(map(str.strip, tempsArray))
		for temperatures in tempsArray[-3:]:
			if int(temperatures) > upperTemperatureLimit:
				return False
				break
		return True
	except IOError:
		logMessage("File not found for checking previous temperatures, assuming initial run")
		return True
	except Exception as e:
		logMessage("Script failed due to an unexpected error")
		logMessage(e)
		sys.exit(1)

def readLastKnownTemp():
	try:
		with open(outputFile, "r") as f:
			lines = f.read().splitlines()
			lastKnownTempVal = lines[-1]
		return int(lastKnownTempVal)
	except IOError:
		logMessage("File not found for reading last known temperature, assuming initial run")
		return 0
	except Exception as e:
		logMessage("Unexpected error found in readLastKnownTemp, exiting")
		logMessage(e)
		sys.exit(1)

def clearOutputFile():
	try:
		outputFileSize=os.path.getsize(outputFile)
		if outputFileSize > outputFileSizeLimit:
			logMessage("Output file size exceeds the limit, clearing the file")
			open(outputFile, "w").close()
	except Exception as e:
		if "The system cannot find the file specified" in str(e):
			logMessage("File not found for clearing, assuming initial run")
		else:
			logMessage("Unexpected error found in clearOutputFile, exiting")
			logMessage(e)
			sys.exit(1)

def writeToFile(coolingInd=None):
	try:
		if coolingInd is None:
			with open(outputFile,"a+") as f:
				f.write(str(currentTemp)+"\n")
			f.close()
		else:
			with open(indicatorFile,"w+") as f:
				f.write(str(coolingInd))
			f.close()
	except IOError as e:
		logMessage("Unable to write temperature to output file")
		logMessage(e)
		sys.exit(1)
	except Exception as e:
		logMessage("Unexpected error found in writeToFile, exiting")
		logMessage(e)
		sys.exit(1)

def getCoolingInd():
	try:
		with open(indicatorFile,"r") as f:
			currentCoolingInd = f.readlines()
		return currentCoolingInd[0]
	except IOError as e:
		logMessage("File not found for reading cooling indicator, assuming initial run")
		return "Stop"
	except Exception as e:
		logMessage("Unexpected error found in getCoolingInd, exiting")
		logMessage(e)
		sys.exit(1)

# Main script starts here
lastKnownTemp = readLastKnownTemp()
clearOutputFile()
curCoolingInd = getCoolingInd()

logMessage("Current temperature is " + str(currentTemp))
logMessage("Last known temperature is " + str(lastKnownTemp))

if currentTemp > upperTemperatureLimit and lastKnownTemp > upperTemperatureLimit and curCoolingInd == "Start":
	logMessage("Extreme Cooling is already running")
elif currentTemp > upperTemperatureLimit and lastKnownTemp < upperTemperatureLimit and curCoolingInd == "Stop":
	logMessage("Temperature is above the limit, running Extreme Cooling")
	writeToFile("Start")
	#runExtremeCooling()
elif currentTemp < upperTemperatureLimit and checkPreviousTemps() and curCoolingInd == "Start":
	logMessage("Temperature is below the limit, stopping Extreme Cooling")
	#runExtremeCooling()
	writeToFile("Stop")
elif currentTemp <= upperTemperatureLimit and checkPreviousTemps() == False and curCoolingInd == "Start":
	logMessage("Not cooled enough, skipping till next run")
elif currentTemp < upperTemperatureLimit and curCoolingInd == "Stop":
	logMessage("Temperature is normal")

writeToFile()
logMessage("","Newline")
