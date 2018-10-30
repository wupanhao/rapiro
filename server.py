import snowboydecoder
import sys
import signal
from stt2 import *
import os

interrupted = False
token = get_token()

def detected_callback():
        global detector
        detector.terminate()
        print "hotword detected"
        os.system("aplay resources/ding.wav")
        os.system("arecord -d 4 -r 16000 -c 1 -t wav -f S16_LE record.wav")
        use_cloud(token)
        detector.start(detected_callback=detected_callback,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=detected_callback,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
