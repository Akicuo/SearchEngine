
let currentSearchType = 'web';

const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');


    function performSearch() {
        const searchTerm = searchInput.value.trim();
        if (searchTerm) {
            window.location.href = `/search?q=${encodeURIComponent(searchTerm)}`;
        }
    }


    if (searchButton) {
        searchButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default button behavior
            performSearch();
        });
    }

    if (searchInput) {
        searchInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault(); 
                performSearch();
            }
        });
    }
});