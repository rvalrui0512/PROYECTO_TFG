// notification_popup.js

document.addEventListener('DOMContentLoaded', function() {
    const bell = document.getElementById('notificationBell');
    const popup = document.getElementById('notificationPopup');
    if (!bell || !popup) return;

    bell.addEventListener('click', function(e) {
        e.preventDefault();
        popup.classList.toggle('show');
        if (popup.classList.contains('show')) {
            fetch('/notificaciones/?ajax=1')
                .then(response => response.text())
                .then(html => {
                    popup.innerHTML = html;
                });
        }
    });

    document.addEventListener('click', function(e) {
        if (!popup.contains(e.target) && !bell.contains(e.target)) {
            popup.classList.remove('show');
        }
    });
});
