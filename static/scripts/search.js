
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');

    // Clear "None" placeholder from server-side template
    if (searchInput.value.trim() === 'None') {
        searchInput.value = '';
    }

    function getCurrentCategory() {
        const params = new URLSearchParams(window.location.search);
        return params.get('cat') || 'discover';
    }

    function performSearch() {
        const searchInput = document.getElementById('searchInput');
        const searchTerm = searchInput.value.trim();
        if (searchTerm) {
            const category = getCurrentCategory();
            window.location.href = `/search?q=${encodeURIComponent(searchTerm)}&cat=${category}`;
        }
    }

    // Handle form submission
    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        performSearch();
    });


});
