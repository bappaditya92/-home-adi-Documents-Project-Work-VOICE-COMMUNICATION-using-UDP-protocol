import socket
import pyaudio
import wave
import time

HOST = '127.0.0.1'
PORT = 5501
SERVER = ('127.0.0.1', 5500)
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 512
RECORD_SECONDS = 10

def start_udp_client():
    start = time.time()
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    print('Sending Stream...START!')
    while True:
        data = stream.read(CHUNK)
        if time.time() > start + RECORD_SECONDS:
            break
        s.sendto(data, SERVER)

    s.sendto('stop'.encode(), SERVER)
    stream.stop_stream()
    stream.close()
    audio.terminate()
    s.close()



if __name__ == '__main__':
    start_udp_client()