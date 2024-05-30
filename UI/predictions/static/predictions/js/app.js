document.addEventListener('DOMContentLoaded', function() {
    const startBtn = document.getElementById('start-prediction');

    if (startBtn) {
        console.log('Botón encontrado en el DOM');
        startBtn.addEventListener('click', function(event) {
            event.preventDefault(); // Previene la navegación inmediata.
            console.log('Clic en el botón detectado');
            document.body.style.backgroundColor = 'rgba(255, 0, 0, 0.5)'; // Cambia el color de fondo a rojo semitransparente

            setTimeout(() => {
                document.body.style.backgroundColor = ''; // Restablece el color de fondo original
                // Redirige al usuario después de la pausa
                window.location.href = startBtn.getAttribute('data-url');
            }, 1000); // Da 1 segundo para que el cambio sea visible
        });
    } else {
        console.error('El botón no se encontró en el DOM');
    }
});
