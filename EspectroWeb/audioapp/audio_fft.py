import pyaudio
import numpy as np
import struct
import csv

# Parámetros de audio
FRAMES = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
Fs = 44100

def captura_y_procesa_audio():
    """ Captura una muestra de audio y la retorna en formato de datos enteros """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=Fs, input=True, frames_per_buffer=FRAMES)
    
    data = stream.read(FRAMES)
    data_int = struct.unpack(str(FRAMES) + 'h', data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return np.array(data_int)

def calcula_fft(data):
    """ Calcula la FFT y devuelve frecuencias y magnitudes """
    fft_data = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(fft_data), 1/Fs)
    magnitudes = np.abs(fft_data)
    
    # Solo devuelve las frecuencias positivas y sus magnitudes correspondientes
    return freqs[:len(freqs) // 2], magnitudes[:len(magnitudes) // 2]

def save_fft_to_csv(freqs, magnitudes, filename='fft_data.csv'):
    """ Guarda las frecuencias y magnitudes en un archivo CSV """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Frecuencia (Hz)', 'Magnitud'])
        for freq, mag in zip(freqs, magnitudes):
            writer.writerow([freq, mag])
