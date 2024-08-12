document.addEventListener('DOMContentLoaded', function() {
    const videoStream = document.getElementById('videoStream');
    const startExperiment = document.getElementById('start-experiment');
    const stopExperiment = document.getElementById('stop-experiment');
    const uploadScript = document.getElementById('upload-script');
    const scriptFile = document.getElementById('script-file');
    const currentStatus = document.getElementById('current-status');
    const activeRobots = document.getElementById('active-robots');
    const resultsContent = document.getElementById('results-content');

    // Configurar el stream de video
    videoStream.src = `http://atriz-project.duckdns.org/video/stream?topic=/usb_cam/image_raw`;
    // videoStream.src = `http://181.52.68.38/video/stream?topic=/usb_cam/image_raw`;

    videoStream.onerror = function() {
        setTimeout(() => {
            videoStream.src = videoStream.src;
        }, 1000);
    };

    // Funciones de control de experimentos
    startExperiment.addEventListener('click', function() {
        // Aquí iría la lógica para iniciar el experimento
        currentStatus.textContent = 'Running';
        activeRobots.textContent = '5'; // Ejemplo
        console.log('Experimento iniciado');
    });

    stopExperiment.addEventListener('click', function() {
        // Aquí iría la lógica para detener el experimento
        currentStatus.textContent = 'Stopped';
        activeRobots.textContent = '0';
        console.log('Experimento detenido');
    });

    // Función para subir script
    uploadScript.addEventListener('click', function() {
        if (scriptFile.files.length > 0) {
            const file = scriptFile.files[0];
            const reader = new FileReader();
            reader.onload = function(e) {
                const content = e.target.result;
                console.log('Script cargado:', content);
                // Aquí iría la lógica para enviar el script al servidor
                resultsContent.textContent = 'Script uploaded: ' + file.name;
            };
            reader.readAsText(file);
        } else {
            alert('Por favor seleccione un archivo Python.');
        }
    });

    // Simulación de actualización de resultados (esto se reemplazaría con datos reales del experimento)
    function updateResults() {
        const fakeResults = `Experiment Results:
Robot 1: Position (10, 20), Task Completed
Robot 2: Position (15, 30), In Progress
Robot 3: Position (5, 25), Waiting
Robot 4: Position (20, 10), Task Completed
Robot 5: Position (30, 35), In Progress`;
        
        resultsContent.textContent = fakeResults;
    }

    // Actualizar resultados cada 5 segundos (simulación)
    setInterval(updateResults, 5000);
});
