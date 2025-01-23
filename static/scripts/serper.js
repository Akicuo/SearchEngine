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
        console.log(url);

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
        
        if (data.news && Array.isArray(data.news)) {
            searchResults.classList.remove('image-results');

            data.news.forEach(item => {
                const container = document.createElement('div');
                container.classList.add('news-item');

                const image = document.createElement('img');
                image.src = item.imageUrl || 'https://via.placeholder.com/150'; // Fallback image
                image.alt = 'News Image';

                const content = document.createElement('div');
                const title = document.createElement('h2');
                const link = document.createElement('a');
                link.href = item.link;
                link.textContent = item.title;

                const description = document.createElement('p');
                description.textContent = item.snippet;

                const meta = document.createElement('div');
                meta.classList.add('meta');
                meta.innerHTML = `<span>${item.date}</span> • <span>${item.source}</span>`;

                title.appendChild(link);
                content.appendChild(title);
                content.appendChild(description);
                content.appendChild(meta);

                container.appendChild(image);
                container.appendChild(content);

                searchResults.appendChild(container);
            });
        }

        else if (data.organic && Array.isArray(data.organic)) {
            searchResults.classList.toggle('image-results', false);
            searchResults.classList.toggle('fdc', true);
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
        } else if (data.images && Array.isArray(data.images)) {
            searchResults.classList.toggle('fdc', false);
            data.images.forEach(item => {
                searchResults.classList.toggle('image-results', true);
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

    fetchSearchResults('discover');

    // Category selection
    document.querySelectorAll('.WebSearchCatag').forEach(function(element) {
        element.addEventListener('click', function(event) {
            event.preventDefault();

            document.querySelectorAll('.WebSearchCatag').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');

            // Fetch results with selected category from href
            const href = event.target.getAttribute('href');
            const urlParams = new URLSearchParams(href.split('?')[1]);
            const selectedCategory = urlParams.get('cat') || 'discover';
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
