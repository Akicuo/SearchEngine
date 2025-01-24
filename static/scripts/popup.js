document.addEventListener('DOMContentLoaded', function() {
    const popup = document.getElementById('popupMessage');
    const closeBtn = document.querySelector('.popup-close');

    if (popup) {
        closeBtn.addEventListener('click', function() {
            popup.style.display = 'none';
            fetch("/remove-session-message", { method: "POST" })
        });

        // Optional: Close popup when clicking outside
        popup.addEventListener('click', function(event) {
            if (event.target === popup) {
                popup.style.display = 'none';
                
            }
        });
    }
});