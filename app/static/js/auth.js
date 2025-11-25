// Auto-login con usuarios de prueba
(function() {
    console.log('Iniciando script de auto-login');
    
    // Esperar a que el DOM esté completamente cargado
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAutoLogin);
    } else {
        initAutoLogin();
    }
    
    function initAutoLogin() {
        console.log('DOM listo, iniciando...');
        
        var userCards = document.querySelectorAll('.user-card');
        console.log('Tarjetas encontradas:', userCards.length);
        
        userCards.forEach(function(card) {
            card.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                var username = this.getAttribute('data-username');
                var password = this.getAttribute('data-password');
                
                console.log('Click en tarjeta - Usuario:', username, 'Password:', password);
                
                var usernameInput = document.getElementById('username-input');
                var passwordInput = document.getElementById('password-input');
                var form = document.getElementById('login-form');
                var spinner = document.getElementById('spinner');
                
                if (usernameInput && passwordInput && form) {
                    usernameInput.value = username;
                    passwordInput.value = password;
                    
                    // Mostrar spinner
                    if (spinner) {
                        spinner.style.display = 'block';
                    }
                    
                    console.log('Valores asignados, mostrando spinner y enviando formulario...');
                    
                    // Delay de 1.5 segundos para ver el spinner
                    setTimeout(function() {
                        form.submit();
                    }, 1500);
                } else {
                    console.error('No se encontraron los elementos del formulario');
                }
            });
        });
        
        console.log('Event listeners agregados');
    }
})();
