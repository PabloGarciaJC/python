// JS para limpiar historial y manejar ayuda
document.addEventListener('DOMContentLoaded', function() {
    // Flag para evitar duplicidad de envíos
    let isSending = false;

    // ======================
    // CSRF helper
    // ======================
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // ======================
    // Variables globales
    // ======================
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const typingIndicator = document.getElementById('typing-indicator');
    const clearBtn = document.getElementById('clear-history-btn');
    let autoScroll = true;

    // ======================
    // Enviar mensaje
    // ======================
    async function sendMessage() {
            if (isSending) return;
            const message = messageInput.value.trim();
            if (!message) return;

            // Validar comandos básicos
            const comandosBasicos = [
                /^ayuda$/i,
                /^buscar producto\s.+$/i,
                /^resumen de ventas$/i,
                /^resumen de compras$/i,
                /^productos con stock bajo$/i
            ];
            const esComando = comandosBasicos.some(reg => reg.test(message));
            if (!esComando) {
                Swal.fire({
                    title: 'Comando no reconocido',
                    text: 'Ese mensaje no es un comando aceptado. Usa los comandos básicos mostrados en la bienvenida.',
                    icon: 'warning',
                    confirmButtonColor: '#667eea'
                });
                return;
            }

            isSending = true;
            messageInput.disabled = true;
            sendBtn.disabled = true;
            messageInput.value = '';
            messageInput.style.height = 'auto';
            typingIndicator.style.display = 'flex';
            scrollToBottom();
        try {
            const csrftoken = getCookie('csrftoken');
            const response = await fetch('/chatbot/send/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            if (data.success) {
                location.reload();
            } else {
                addBotMessage('Lo siento, hubo un error al procesar tu mensaje.');
                console.error('Error:', data.error);
            }
        } catch (error) {
            console.error('Error al enviar mensaje:', error);
            addBotMessage('Error de conexión. Verifica tu internet e intenta de nuevo.');
        } finally {
            typingIndicator.style.display = 'none';
            messageInput.disabled = false;
            sendBtn.disabled = false;
            messageInput.focus();
            scrollToBottom();
            isSending = false;
        }
    }

    // ======================
    // Agregar mensaje usuario
    // ======================
    function addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.innerHTML = `
            <div class="message-content">
                <i class="fas fa-user message-icon"></i>
                <div class="message-text">${escapeHtml(message)}</div>
            </div>
            <div class="message-time">${getCurrentTime()}</div>
        `;
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    // ======================
    // Agregar mensaje bot
    // ======================
    function addBotMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.innerHTML = `
            <div class="message-content">
                <i class="fas fa-robot message-icon"></i>
                <div class="message-text">${formatBotMessage(message)}</div>
            </div>
            <div class="message-time">${getCurrentTime()}</div>
        `;
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    // ======================
    // Formatear mensaje bot
    // ======================
    function formatBotMessage(message) {
        let formatted = escapeHtml(message);
        formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        formatted = formatted.replace(/^•(.+)$/gm, '<li>$1</li>');
        formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
        formatted = formatted.replace(/\n\n/g, '<br><br>');
        formatted = formatted.replace(/\n/g, '<br>');
        return formatted;
    }

    // ======================
    // Escapar HTML
    // ======================
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ======================
    // Hora actual
    // ======================
    function getCurrentTime() {
        const now = new Date();
        return `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    }

    // ======================
    // Scroll automático
    // ======================
    function scrollToBottom() {
        if (autoScroll) {
            setTimeout(() => {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 100);
        }
    }

    // Detectar scroll del usuario
    chatMessages.addEventListener('scroll', function () {
        const isScrolledToBottom =
            chatMessages.scrollHeight - chatMessages.scrollTop <= chatMessages.clientHeight + 50;
        autoScroll = isScrolledToBottom;
    });

    // Enviar mensaje con click
    sendBtn.addEventListener('click', sendMessage);

    // Enviar con Enter
    messageInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });


    // ======================
    // Limpiar historial
    // ======================
    if (clearBtn) {
        clearBtn.addEventListener('click', async function () {
            try {
                const csrftoken = getCookie('csrftoken');
                const response = await fetch('/chatbot/clear-history/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    }
                });

                const data = await response.json();

                if (data.success) {
                    Swal.fire({
                        title: '¡Listo!',
                        text: 'Historial eliminado correctamente',
                        icon: 'success',
                        confirmButtonColor: '#667eea',
                        timer: 2000
                    });
                    location.reload();
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                console.error('Error al limpiar historial:', error);
                Swal.fire({
                    title: 'Error',
                    text: 'No se pudo eliminar el historial',
                    icon: 'error',
                    confirmButtonColor: '#667eea'
                });
            }
        });
    }

});
