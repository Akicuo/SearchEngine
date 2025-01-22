
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');

    // Clean initial input value
    const cleanInitialValue = (value) => {
        const cleaned = value.replace(/^"|"$/g, ''); // Remove surrounding quotes
        return cleaned === 'None' ? '' : cleaned;
    };
    
    searchInput.value = cleanInitialValue(searchInput.value.trim());

    function getCurrentCategory() {
        const params = new URLSearchParams(window.location.search);
        return params.get('cat') || 'discover';
    }

    function performSearch() {
        const searchInput = document.getElementById('searchInput');
        const searchTerm = searchInput.value.trim();
        console.log(searchTerm);
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
