document.addEventListener('DOMContentLoaded', function() {
    const searchResults = document.querySelector('.searchResults');
    const searchInput = document.getElementById('searchInput');

    function fetchSearchResults(category = '') {

        const query = searchInput.value.trim();
        
        // Don't perform empty searches
        if (!query) {
            searchResults.innerHTML = '<p>Please enter a search term</p>';
            return;
        }

        // Construct the URL with query and category parameters
        const url = `/api/serper?q=${encodeURIComponent(query)}${category ? `&cat=${encodeURIComponent(category)}` : ''}`;


        const resultsContainer = document.getElementById('searchResults');
        if (resultsContainer) {
            resultsContainer.classList.add('blurred-text');
        }

        fetch(url, { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Search results:', data);
            searchResults.innerHTML = '';
            
            if (!data.organic || data.organic.length === 0) {
                searchResults.innerHTML = '<p>No results found</p>';
                return;
            }

            data.organic.forEach(item => {
                const result = document.createElement('a');
                result.className = "searchResult";
                result.href = item.link;
                result.target = "_blank";
                result.rel = "noopener noreferrer"; // Security best practice for _blank links

                const title = document.createElement('h2');
                title.className = "searchResultTitle";
                title.textContent = item.title;

                const link = document.createElement('h5');
                link.className = "searchResultLink";
                link.textContent = item.link;

                const snippet = document.createElement('p');
                snippet.className = "searchResultContent";
                snippet.textContent = item.snippet;

                result.appendChild(title);
                result.appendChild(link);
                result.appendChild(snippet);
                searchResults.appendChild(result);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            searchResults.innerHTML = '<p>An error occurred while fetching results</p>';
        })
        .finally(() => {
            // Removing blur after loaded results
            if (resultsContainer) {
                resultsContainer.classList.remove('blurred-text');
            }
        });
    }
    fetchSearchResults(category = 'discover');

    // CATegory selection
    document.querySelectorAll('.WebSearchCatag').forEach(function(element) {
        element.addEventListener('click', function(event) {
            event.preventDefault();
            
            // Update active state for clicked category
            document.querySelectorAll('.WebSearchCatag').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Fetch results with selected category
            const selectedCategory = event.target.textContent.trim();
            fetchSearchResults(selectedCategory);
        });
    });


    searchInput.addEventListener('input', debounce(function() {
        const activeCategory = document.querySelector('.WebSearchCatag.active');
        fetchSearchResults(activeCategory ? activeCategory.textContent.trim() : '');
    }, 500));
});

// Debounce helper function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}