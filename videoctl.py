import subprocess
import os
import time
import datetime
prev_statev = 0
prev_statea = 0
prev_statef = 0
while True:
	#date and time
	now = datetime.datetime.now()
	out = now.strftime("%Y-%m-%d_%H:%M:%s")

	#curl to check audio,video and bluetooth start/stop from firebase
	outputv = subprocess.check_output("curl 'https://adhd-69.firebaseio.com/adhd-69/act/video/.json' | awk -F'\"' '{$0=$4}1'",shell=True)
	outputb = subprocess.check_output("curl 'https://adhd-69.firebaseio.com/adhd-69/act/bluetooth/.json' | awk -F'\"' '{$0=$4}1'",shell=True)
	outputa = subprocess.check_output("curl 'https://adhd-69.firebaseio.com/adhd-69/act/audio/.json' | awk -F'\"' '{$0=$4}1'",shell=True)

	#start face detection
	if str (outputv.rstrip()) == "Stop" and str(outputb.rstrip()) == "Start" and prev_statef == 0:
		subprocess.call("sudo python bhuvan.py &", shell=True)
		prev_statef = 1

	#to stop face detection
	elif str (outputv.rstrip()) == "Start" or str(outputb.rstrip()) == "Stop" and prev_statef == 1:
                os.system("sudo pkill -9 -f bhuvan.py")
		prev_statef = 0

	#to start video record
	if str (outputv.rstrip()) == "Start" and str (outputa.rstrip()) == "Stop" and prev_statev == 0:
		nowv = datetime.datetime.now()
		outv = nowv.strftime("%Y-%m-%d_%H:%M:%s")
		os.system("bash parallel.sh \"arecord /home/pi/%s.wav -D sysdefault:CARD=1 -d 0\" \"raspivid -o /home/pi/%s.h264 -t 0\" &" % (outv,outv))
		prev_statev = 1

	#to stop and merge video
	elif str (outputv.rstrip()) == "Stop" and prev_statev == 1:
		os.system("sudo killall raspivid")
		os.system("sudo killall arecord")
		#time.sleep(20)
		os.system("ffmpeg -framerate 24 -i /home/pi/%s.h264 -c copy /home/pi/%s.mp4" % (outv,outv))
		os.system("ffmpeg -i /home/pi/%s.mp4 -i /home/pi/%s.wav -c:v copy -c:a aac -strict experimental /home/pi/%sout.mp4" % (outv,outv,outv))
		time.sleep(10)
		os.system("python learn.py -v /home/pi/%sout.mp4" % outv)
		prev_statev = 0

	#to start audio record
        elif str (outputa.rstrip()) == "Start" and str (outputv.rstrip()) == "Stop" and prev_statea == 0:
		sec = subprocess.check_output("curl 'https://adhd-69.firebaseio.com/adhd-69/act/seconds/.json' | awk -F'\"' '{$0=$4}1'",shell=True)
		print sec
		os.system("arecord /home/pi/Desktop/Untitled\ Folder/%s.wav -D sysdefault:CARD=1 -d %s " % (out,sec))
		#time.sleep(10)
		os.system("python dha.py -a %s.wav" % out)
		#prev_statea = 1
		#name = out;
		os.system("curl -X PUT -d '{ \"action\" : \"Stop\" }' 'https://adhd-69.firebaseio.com/adhd-69/act/audio/.json'")

	#to stop audio record
	#elif str (outputa.rstrip()) == "Stop" and prev_statea == 1:
		#os.system("killall arecord")
		#time.sleep(10)
		#os.system("sudo cp %s.wav test.wav" % name)
		#os.system("python dha.py -a %s" % name)
		#prev_statea = 0

