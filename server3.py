#!coding:utf-8
import snowboydecoder
import sys
import signal
import os
import yaml

from keras.models import load_model
from record import Mic
from data_utils import load_label_name,get_mfcc,get_pcm
import numpy as np
interrupted = False
mic = Mic()
mic.fetchThreshold()
detector = None
config = None

# model = load_model('asr_model.h5') # 加载训练模型
# model = load_model('asr_mfcc_conv1d_model.h5') # 加载训练模型
model = load_model('MiniVGGNet(64,40,1)37.h5') # 加载训练模型
# model = load_model('asr_mfcc_dense_model.h5') # 加载训练模型
label_names = load_label_name()

def detected_callback():
    global detector
    global mic
    global config
    detector.terminate()
    print("hotword detected")
    os.system("aplay resources/ding.wav")
    os.system("arecord -d 2 -r 16000 -c 1 -t wav -f S16_LE record.wav")
    os.system("aplay record.wav")
    # mic.activeListenToAllOptions(LISTEN_TIME=1)
    predict(model)
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
  global config
  if len(sys.argv) == 1:
      print("Error: need to specify model name")
      print("Usage: python demo.py your.model")
      sys.exit(-1)

  with open("./config.yaml") as f:
      config = yaml.load(f)
  
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

def predict(model):
    X=get_mfcc('record.wav',samples=32500)
    # X=get_pcm('record.wav',samples=32000)
    print(X.shape)
    #test dense model
    # X = np.reshape(np.array(X),(-1,32000))

    # test conv1d model
    X = np.reshape(np.array(X),(-1,64,40,1))
    # test conv2d model
    # X = np.reshape(np.array(X),(-1,64,40))    
    pred_probab = model.predict(X)
    pred_class = list(pred_probab[0]).index(max(pred_probab[0]))
    print("may be " , label_names[pred_class] , " probab: " ,  pred_probab[0][pred_class])
    formated = list( map(lambda x,i : (x.item(),label_names[i]) , pred_probab[0],[i for i in range(len(label_names))]) )
    lists = sorted(formated,reverse=True)
    top5 = lists[:5]
    print("top5 :",top5)
    return lists

if __name__ == '__main__':
    main()
