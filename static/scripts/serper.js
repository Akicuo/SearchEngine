document.addEventListener('DOMContentLoaded', function() {
    const searchResults = document.querySelector('.searchResults');
    const searchInput = document.getElementById('searchInput');
    const searchCache = {}; // Cache to store search results

    function fetchSearchResults(category = '') {
        const query = searchInput.value.trim();
        const cacheKey = `${query}_${category}`;

        // Check if results are already cached
        if (searchCache[cacheKey]) {
            displayResults(searchCache[cacheKey]);
            return; 
        }


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
            searchCache[cacheKey] = data; // Cache the results
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            searchResults.innerHTML = '<p>An error occurred while fetching results</p>';
        })
        .finally(() => {
            // Removing blur effect after results are displayed
            if (resultsContainer) {
                resultsContainer.classList.remove('blurred-text');
            }
        });
    }

    function displayResults(data) {
        searchResults.innerHTML = '';

        if (data.organic) {
            document.querySelector('.searchResults').classList.toggle('image-results', false);
            document.querySelector('.searchResults').classList.toggle('fdc', true);
            data.organic.forEach(item => {
                const result = document.createElement('a');
                result.className = "searchResult";
                result.href = item.link;
                result.target = "_blank";
                result.rel = "noopener noreferrer"; 

                const title = document.createElement('h2');
                title.className = "searchResultTitle";
                title.textContent = item.title;

                const link = document.createElement('h5');
                link.className = "searchResultLink";
                // Format URL path as breadcrumbs
                const url = new URL(item.link);
                const pathSegments = url.pathname.split('/').filter(segment => segment.length > 0);
                link.textContent = `${url.hostname} ${pathSegments.length > 0 ? '> ' + pathSegments.join(' > ') : ''}`;

                const snippet = document.createElement('p');
                snippet.className = "searchResultContent";
                snippet.textContent = item.snippet;

                result.appendChild(title);
                result.appendChild(link);
                result.appendChild(snippet);
                searchResults.appendChild(result);
            });
        } else if (data.images) {
            document.querySelector('.searchResults').classList.toggle('fdc', false);
            data.images.forEach(item => {
                document.querySelector('.searchResults').classList.toggle('image-results', true);
                const result = document.createElement('img');
                result.src = item.imageUrl;
                result.alt = item.title || 'Image';
                result.className = "ImgResult";
                searchResults.appendChild(result);
            });
        } else if (!data.organic || data.organic.length === 0) {
            searchResults.innerHTML = '<p>No results found for your search.</p>';
            return;
        }
    }

    fetchSearchResults(category = 'discover');

    // Category selection
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
