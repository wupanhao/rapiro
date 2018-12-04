import snowboydecoder
import sys
import signal
import os
import yaml

from record import Mic
from baidu_api import Baidu
import Hass


interrupted = False
stt = None
mic = Mic()
mic.fetchThreshold()
detector = None
config = None

def detected_callback():
    global detector
    global mic
    global config
    detector.terminate()
    print "hotword detected"
    os.system("aplay resources/ding.wav")
    # os.system("arecord -d 4 -r 16000 -c 1 -t wav -f S16_LE record.wav")
    mic.activeListenToAllOptions()
    res = stt.recognize()
    if(res['err_no']):
      print(res)
    else:
      text = res['result'][0]
      print(text)
      if(Hass.isValid(text)):
        print('handled by hass')
        Hass.handle(text,config)
      else:
        print('no handler matched , use default tuling')
    detector.start(detected_callback=detected_callback,
           interrupt_check=interrupt_callback,
           sleep_time=0.03)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def main():
  global detector
  global stt
  global config
  if len(sys.argv) == 1:
      print("Error: need to specify model name")
      print("Usage: python demo.py your.model")
      sys.exit(-1)

  with open("./config.yaml") as f:
      config = yaml.load(f)
  
  stt = Baidu(config)

  print(len(sys.argv))
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


if __name__ == '__main__':
  main()
