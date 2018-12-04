#!coding:utf-8

from aip import AipSpeech
import yaml

SLUG = 'baidu_yuyin'

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

class Baidu:
	def __init__(self, config):
		APP_ID = config[SLUG]['app_id']
		API_KEY = config[SLUG]['api_key']
		SECRET_KEY = config[SLUG]['secret_key']
		self._client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
	# 读取文件


	# 识别本地文件
	def recognize(self,audio_file = 'record.wav'):
		file = get_file_content(audio_file)
		res = self._client.asr(file, 'wav', 16000, {
	    'dev_pid': 1536,
	})
		return res


if __name__ == '__main__':
    with open("./config.yaml") as f:
        config = yaml.load(f)
        stt = Baidu(config)
        print(stt.recognize())