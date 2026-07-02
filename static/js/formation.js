document.addEventListener('DOMContentLoaded', function() {
    const blocks = document.querySelectorAll('.programme-content');
    
    blocks.forEach(block => {
        const rawText = block.querySelector('.programme-raw-text').textContent.trim();
        if (!rawText) return;

        // Regex magique pour trouver "Semestre 1 :", "semestre 2 :", etc.
        const regex = /(semestre\s*\d+)\s*:/gi;
        const matches = [...rawText.matchAll(regex)];
        
        let html = '';

        if (matches.length > 0) {
            // Si on a trouvé des semestres, on les sépare proprement
            matches.forEach((m, index) => {
                // Mettre une majuscule au début du titre (ex: "Semestre 1 :")
                const titre = m[1].charAt(0).toUpperCase() + m[1].slice(1); 
                const start = m.index + m[0].length;
                
                // Trouver où finit ce semestre (là où commence le suivant)
                const end = index < matches.length - 1 ? matches[index + 1].index : rawText.length;
                
                // Extraire le texte du semestre
                let texteSemestre = rawText.substring(start, end).trim();
                
                // Nettoyer les tirets/puces existants et séparer en lignes (modules)
                const modules = texteSemestre.split('\n')
                    .map(m => m.replace(/^[-•*]\s*/, '').trim()) 
                    .filter(m => m.length > 0); 

                html += `
                    <div class="semestre-block">
                        <div class="semestre-title">📘 ${titre}</div>
                        <ul class="module-list">
                            ${modules.map(mod => `<li>${mod}</li>`).join('')}
                        </ul>
                    </div>
                    `;
            });
        } else {
            // Si l'admin n'a pas écrit "Semestre X :", on affiche le texte brut en liste simple
            const lignes = rawText.split('\n').filter(l => l.trim().length > 0);
            html = `<div class="semestre-block"><ul class="module-list">${lignes.map(l => `<li>${l}</li>`).join('')}</ul></div>`;
        }

        // Injecter le HTML généré dans la div visible
        block.querySelector('.programme-formatted').innerHTML = html;
    });
});

// Fonction pour ouvrir/fermer le programme
function toggleProgramme(button) {
    const content = button.nextElementSibling;
    const icon = button.querySelector('.toggle-icon');
    
    if (content.style.display === 'none' || getComputedStyle(content).display === 'none') {
        content.style.display = 'block';
        icon.classList.add('rotated');
    } else {
        content.style.display = 'none';
        icon.classList.remove('rotated');
    }
}