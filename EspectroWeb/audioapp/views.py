from django.shortcuts import render
from django.http import JsonResponse
import json
import io
import base64
from .audio_fft import captura_y_procesa_audio, calcula_fft, save_fft_to_csv
import matplotlib.pyplot as plt
import numpy as np

def index(request):
    return render(request, 'index.html')

def procesar_audio_view(request):
    if request.method == 'POST':
        # Captura de audio y procesamiento FFT
        data = captura_y_procesa_audio()
        freqs, magnitudes = calcula_fft(data)
        
        # Determinación de la frecuencia máxima y su magnitud
        idx_max = np.argmax(magnitudes)
        frecuencia_max = freqs[idx_max]
        magnitud_max = magnitudes[idx_max]
        
        # Guardado en CSV
        save_fft_to_csv(freqs, magnitudes)

        # Crear figura de gráficos
        fig, (ax, ax1) = plt.subplots(2, figsize=(8, 6))
        ax.plot(data)  # Gráfica de onda temporal
        ax.set_title('Onda Temporal')
        ax.set_xlabel('Muestras')
        ax.set_ylabel('Amplitud')

        ax1.plot(freqs, magnitudes)  # Gráfica de espectro de frecuencia
        ax1.set_title('Espectro de Frecuencia')
        ax1.set_xlabel('Frecuencia (Hz)')
        ax1.set_ylabel('Magnitud')

        # Ajustar el espacio entre los gráficos
        plt.subplots_adjust(hspace=0.6)

        # Guardar gráfico en un buffer de memoria
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        image_png = buf.getvalue()
        buf.close()

        # Codificar imagen a base64
        graphic_base64 = base64.b64encode(image_png).decode('utf-8')

        return JsonResponse({
            'frecuencia_max': frecuencia_max,
            'magnitud_max': magnitud_max,
            'graphic': graphic_base64
        })

    return JsonResponse({'error': 'Método no permitido'}, status=405)
