import sys
import os
import yaml
from aip import AipSpeech
#root_dir = "./"
root_dir = os.path.dirname(os.path.abspath(__file__))+'/'
print(root_dir)
#sys.path.append(root_dir)
import snowboydecoder
class XiaoBai:
    def __init__(self,keyword_model,callback):
        self.detector = snowboydecoder.HotwordDetector(keyword_model, sensitivity=0.5)
        self._callback = callback
        with open(root_dir+"config.yaml") as f:
            config = yaml.load(f)
            SLUG = 'baidu_yuyin'
            APP_ID = config[SLUG]['app_id']
            API_KEY = config[SLUG]['api_key']
            SECRET_KEY = config[SLUG]['secret_key']
            self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    def callback(self):
            self.detector.terminate()
            self._callback()
            self.detector.start(detected_callback=self.callback,sleep_time=0.03)
            
    def listen_for_keyword(self):
        try:
            print('Listening...')
            self.detector.start(detected_callback=self.callback,sleep_time=0.03)
        except KeyboardInterrupt:
            print('stop')
        finally:
            self.detector.terminate()            
            
    def listen_and_recognize(self,length = 4):
        os.system("arecord -d %d -r 16000 -c 1 -t wav -f S16_LE record.wav" % (length,) )    
        with open("./record.wav", 'rb') as fp:
            res = self.client.asr(fp.read(), 'wav', 16000, { 'dev_pid': 1536,})
            if res['err_no']==0:
#                 print(res)
                return res["result"][0]
            else:
                print(res)
                return ""
    def speak(self,text = '你好百度',lang = 'zh',type = 1 , vol = 5):
        result  = self.client.synthesis(text, lang, type, {'vol': vol,})
        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(result, dict):
            with open('speak.mp3', 'wb') as f:
                f.write(result)
            os.system('mpg123 speak.mp3')
        else:
            print(result)
if __name__ == '__main__':
    xiaobai = None
    def callback():
        global xiaobai
        notify_sound = root_dir+'resources/ding.wav'
        os.system("aplay "+notify_sound)
        print("key word detected")
        if xiaobai is not None:
            res = xiaobai.listen_and_recognize()
            print(res)
            xiaobai.speak(res)
        # to be add
    keyword_model = root_dir+'resources/小白.pmdl'
    xiaobai = XiaoBai(keyword_model=keyword_model,callback=callback) 
    xiaobai.listen_for_keyword()
