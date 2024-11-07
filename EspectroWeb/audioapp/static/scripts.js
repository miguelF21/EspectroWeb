fetch('/procesar_audio/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({})
})
.then(response => response.json())
.then(data => {
    if (data.error) {
        document.getElementById('error-message').style.display = 'block';
        document.getElementById('error-message').textContent = data.error;
        document.getElementById('resultados').style.display = 'none';
    } else {
        document.getElementById('error-message').style.display = 'none';
        document.getElementById('resultados').style.display = 'block';
        document.getElementById('frecuencia_max').textContent = data.frecuencia_max.toFixed(2);
        document.getElementById('magnitud_max').textContent = data.magnitud_max.toFixed(2);
        document.getElementById('grafico').src = 'data:image/png;base64,' + data.graphic;
    }
})
.catch(error => {
    console.error('Error al procesar el audio:', error);
    document.getElementById('error-message').style.display = 'block';
    document.getElementById('error-message').textContent = 'Error al procesar el audio. Inténtalo de nuevo.';
    document.getElementById('resultados').style.display = 'none';
});
