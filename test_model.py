from keras.models import load_model
from record import Mic
from data_utils import load_label_name,get_mfcc
import time
import numpy as np

model = load_model('asr_mfcc_conv_model.h5') # 加载训练模型
label_names = load_label_name()

def predict(model):
    X=get_mfcc('record.wav')
    print(X.shape)
    X = np.reshape(np.array(X),(-1,20,32,1))
    pred_probab = model.predict(X)
    pred_class = list(pred_probab[0]).index(max(pred_probab[0]))
    print("may be " , label_names[pred_class] , " probab: " ,  pred_probab[0])
    formated = list( map(lambda x,i : (x.item(),label_names[i]) , pred_probab[0],[i for i in range(len(label_names))]) )
    return sorted(formated,reverse=True)

if __name__ == '__main__':
    mic = Mic()
    threshold = mic.fetchThreshold()
    while True:
        print('start listening')
        mic.activeListenToAllOptions(threshold)
        predict(model)
        time.sleep(1)