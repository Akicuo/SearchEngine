document.addEventListener('DOMContentLoaded', function() {
    const editUsernameBtn = document.getElementById('editUsernameBtn');
    const usernameDisplay = document.getElementById('usernameDisplay');
    const usernameEditContainer = document.getElementById('usernameEditContainer');
    const usernameEditInput = document.getElementById('usernameEditInput');
    const usernameEditDoneBtn = document.getElementById('usernameEditDoneBtn');

    editUsernameBtn.addEventListener('click', function() {
        usernameDisplay.style.display = 'none';
        editUsernameBtn.style.display = 'none';
        usernameEditContainer.style.display = 'block';
        usernameEditInput.focus();
    });

    usernameEditDoneBtn.addEventListener('click', function() {
        const newUsername = usernameEditInput.value.trim();

        if (newUsername) {
            // Send POST request to change username
            fetch('/api/change-user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: "{{ session['id'] }}",
                    username: newUsername
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update username display
                    usernameDisplay.textContent = newUsername;
                    
                    // Revert to original view
                    usernameDisplay.style.display = 'block';
                    editUsernameBtn.style.display = 'block';
                    usernameEditContainer.style.display = 'none';
                } else {
                    // Handle error (show message to user)
                    alert(data.message || 'Failed to update username');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while updating username');
            });
        }
    });

    // Allow pressing Enter to submit
    usernameEditInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            usernameEditDoneBtn.click();
        }
    });
});