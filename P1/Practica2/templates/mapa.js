const map = L.map('map').setView([52.52, 13.405], 12); 

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

storeCoordinates.forEach(coords => {
    const lat = coords[0];
    const lng = coords[1];

    const marker = L.marker([lat, lng]).addTo(map);

    // Crear contenido de la ventana emergente (popup)
    const popupContent = `
        <div>
            <h3>hola</h3>
        </div>
    `;

    // Vincular la ventana emergente al marcador
    marker.bindPopup(popupContent);
});