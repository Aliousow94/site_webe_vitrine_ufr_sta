// --- Script pour faire fonctionner le menu mobile ---
document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("sidebarOverlay");
    const openBtn = document.getElementById("sidebarToggle");
    const closeBtn = document.getElementById("sidebarClose");

    // Quand on clique sur les 3 barres
    if (openBtn) {
        openBtn.addEventListener("click", function() {
            sidebar.classList.add("open");
            overlay.classList.add("active");
        });
    }

    // Quand on clique sur la croix (X)
    if (closeBtn) {
        closeBtn.addEventListener("click", function() {
            sidebar.classList.remove("open");
            overlay.classList.remove("active");
        });
    }

    // Quand on clique sur le fond sombre
    if (overlay) {
        overlay.addEventListener("click", function() {
            sidebar.classList.remove("open");
            overlay.classList.remove("active");
        });
    }
});