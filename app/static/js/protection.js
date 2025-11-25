// Protection Layer - Interceptar envíos de formularios
document.addEventListener('DOMContentLoaded', function() {
    // Solo activar protección si el usuario está INACTIVO (activo = 0)
    // window.userActive = true (activo=1) → Puede modificar, no interceptar
    // window.userActive = false (activo=0) → No puede modificar, interceptar
    if (typeof window.userActive === 'undefined' || window.userActive === true) {
        return; // Usuario activo, permitir modificaciones
    }
    
    // Si llegamos aquí, window.userActive === false (usuario inactivo)
    // Interceptar todos los formularios con método POST
    const forms = document.querySelectorAll('form[method="POST"], form[method="post"]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Si el usuario está inactivo, bloquear el envío y mostrar modal
            e.preventDefault();
            e.stopPropagation();
            showRestrictedAccessModal();
            return false;
        });
    });
    
    // Interceptar clicks en botones de eliminar
    const deleteLinks = document.querySelectorAll('a[href*="/eliminar/"]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            showRestrictedAccessModal();
            return false;
        });
    });
});

function showRestrictedAccessModal() {
    const modal = document.createElement('div');
    modal.className = 'swal2-container swal2-center swal2-backdrop-show';
    modal.style.overflowY = 'auto';
    
    modal.innerHTML = `
        <div class="swal2-popup swal2-modal swal2-icon-info swal2-show" tabindex="-1" role="dialog" aria-live="assertive" aria-modal="true" style="display: grid;">
            <button type="button" class="swal2-close" aria-label="Close this dialog" onclick="closeSwalModal()">×</button>
            <div class="swal2-icon swal2-info swal2-icon-show" style="display: flex;">
                <div class="swal2-icon-content">i</div>
            </div>
            <h2 class="swal2-title" id="swal2-title" style="display: block;">Acceso Restringido</h2>
            <div class="swal2-html-container" id="swal2-html-container" style="display: block;">
                <p class="contact-message">El acceso al panel administrativo está restringido. Si necesitas autorización para ingresar o gestionar los módulos del sistema, no dudes en contactarme a través de mis redes sociales.</p>
                <div class="social-links">
                    <a href="https://www.facebook.com/PabloGarciaJC" target="_blank" title="Facebook">
                        <i class="fab fa-facebook-f"></i>
                    </a>
                    <a href="https://www.instagram.com/pablogarciajc" target="_blank" title="Instagram">
                        <i class="fab fa-instagram"></i>
                    </a>
                    <a href="https://www.linkedin.com/in/pablogarciajc" target="_blank" title="LinkedIn">
                        <i class="fab fa-linkedin-in"></i>
                    </a>
                    <a href="https://www.youtube.com/channel/UC5I4oY7BeNwT4gBu1ZKsEhw" target="_blank" title="YouTube">
                        <i class="fab fa-youtube"></i>
                    </a>
                </div>
            </div>
            <div class="swal2-actions" style="display: flex;">
                <button type="button" class="swal2-confirm swal2-styled" aria-label="" onclick="closeSwalModal()" style="display: inline-block;">Cerrar</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    document.body.classList.add('swal2-shown', 'swal2-height-auto');
}

function closeSwalModal() {
    const modal = document.querySelector('.swal2-container');
    if (modal) {
        modal.remove();
        document.body.classList.remove('swal2-shown', 'swal2-height-auto');
    }
}
