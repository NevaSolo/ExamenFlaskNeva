// Récupération des données de voitures depuis Flask
const voitures = {{ voitures|tojson }};
    
// Sélection de l'élément conteneur pour les voitures
const voituresContainer = document.getElementById('voitures-container');
    
// Parcours des données de voitures et création des éléments HTML pour les afficher
voitures.forEach(voiture => {
    const voitureElement = document.createElement('div');
    voitureElement.classList.add('row');
    voitureElement.innerHTML = `
        <hr>
        <div class="col-md-6">
            <picture><img src="${voiture[1]}" alt="Image de la voiture"></picture>
        </div>
        <div class="col-md-6">
            <p>Nom: ${voiture[0]}</p>
            <p>Modèle: ${voiture[2]}</p>
            <p>Matriculation: ${voiture[3]}</p>
            <p>Couleur: ${voiture[4]}</p>
            <p>Prix: ${voiture[5]}</p>
        </div>
    `;
    voituresContainer.appendChild(voitureElement);
});
