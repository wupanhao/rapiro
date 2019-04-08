#!coding=utf-8
import pygame
import time
import wave
import pyaudio

pygame.mixer.init(16000)
def play(file):
  #file_wav = wave.open(file)
  #frequency = file_wav.getframerate()
  #pygame.mixer.init(frequency)
  track=pygame.mixer.music.load(file) #可以播放.mp3 .wav等多种格式的音频文件
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
    time.sleep(0.5)

def play_wav(file):
    CHUNK = 1024
    wf = wave.open(file, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
  play('./record.wav')
  play('./speak.mp3')
