document.addEventListener('DOMContentLoaded', function() {
    // Fermer la modal si on clique sur le fond sombre
    document.getElementById('albumModal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeAlbumModal();
        }
    });
});

// Fonction pour ouvrir la modal d'un album
function openAlbumModal(albumId, albumTitre) {
    const modal = document.getElementById('albumModal');
    const titre = document.getElementById('modalAlbumTitle');
    const grid = document.getElementById('modalPhotosGrid');
    
    titre.textContent = albumTitre;
    grid.innerHTML = '<div style="text-align:center;padding:40px;color:#94a3b8;">Chargement des photos...</div>';
    
    // Récupérer les photos via la route JSON
    fetch(`/admin/galerie/${albumId}/json`)
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                grid.innerHTML = '<div style="text-align:center;padding:40px;color:#94a3b8;">Aucune photo dans cet album.</div>';
                return;
            }
            
            let html = '';
            data.forEach(photo => {
                html += `<img src="/static/uploads/galerie/${photo.photo}" alt="Photo" onclick="openLightbox(this.src)">`;
            });
            grid.innerHTML = html;
        })
        .catch(error => {
            grid.innerHTML = '<div style="text-align:center;padding:40px;color:#e11d48;">Erreur de chargement.</div>';
        });
    
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeAlbumModal() {
    document.getElementById('albumModal').classList.remove('active');
    document.body.style.overflow = '';
}

// Fonction Lightbox (agrandir une photo)
function openLightbox(src) {
    const lightbox = document.getElementById('lightbox');
    const img = document.getElementById('lightboxImg');
    img.src = src;
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    document.getElementById('lightbox').classList.remove('active');
    document.body.style.overflow = '';
}

// Fermer avec la touche Echap
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeLightbox();
        closeAlbumModal();
    }
});