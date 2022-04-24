import socket
import pyaudio
import wave

HOST = '127.0.0.1'
PORT = 5500

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 512
WAVE_OUTPUT_FILENAME = "outstream.wav"
frames = []

def start_udp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    print('Waiting for Stream...')
    while True:
        data, addr = s.recvfrom(CHUNK * 4)
        if str(data) == "b'stop'":
            print('Stop Stream...')
            break
        frames.append(data)

    print('Saving file...')

    audio = pyaudio.PyAudio()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print('DONE!')

    s.close()



if __name__ == '__main__':
    start_udp_server()