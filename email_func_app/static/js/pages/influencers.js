document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle favorite button clicks
    document.querySelectorAll('.favorite-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const heartIcon = this.querySelector('.bi');
            heartIcon.classList.toggle('bi-heart');
            heartIcon.classList.toggle('bi-heart-fill');
            
            // TODO: Add API call to save favorite status
            // const influencerId = this.closest('.influencer-card').dataset.influencerId;
            // saveFavoriteStatus(influencerId);
        });
    });

    // Handle platform filter clicks
    document.querySelectorAll('.platform-filter').forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('active');
            filterInfluencers();
        });
    });

    // Handle category filter clicks
    document.querySelectorAll('.category-filter').forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('active');
            filterInfluencers();
        });
    });

    // Handle search input with debounce
    const searchInput = document.getElementById('search-input');
    let searchTimeout = null;
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            
            searchTimeout = setTimeout(() => {
                const query = this.value.trim();
                if (query.length >= 2 || query.length === 0) {
                    filterInfluencers();
                }
            }, 300);
        });
    }

    // Function to get current filters
    function getCurrentFilters() {
        const platforms = Array.from(document.querySelectorAll('.platform-filter.active'))
            .map(btn => btn.dataset.platform);
        
        const categories = Array.from(document.querySelectorAll('.category-filter.active'))
            .map(btn => btn.dataset.category);
        
        const searchQuery = document.getElementById('search-input')?.value.trim() || '';
        
        return {
            platforms,
            categories,
            searchQuery
        };
    }

    // Function to filter influencers
    function filterInfluencers() {
        const filters = getCurrentFilters();
        
        // Show loading state
        document.querySelectorAll('.influencer-card').forEach(card => {
            card.style.opacity = '0.5';
        });

        // TODO: Replace with actual API call
        setTimeout(() => {
            // Simulate API response
            document.querySelectorAll('.influencer-card').forEach(card => {
                card.style.opacity = '1';
                
                // Example filtering logic (to be replaced with backend filtering)
                let visible = true;
                
                if (filters.platforms.length > 0) {
                    // Check if card has any of the selected platforms
                    const cardPlatforms = Array.from(card.querySelectorAll('.platform-link'))
                        .map(link => link.title.toLowerCase());
                    visible = filters.platforms.some(p => cardPlatforms.includes(p));
                }
                
                if (visible && filters.categories.length > 0) {
                    // Check if card has any of the selected categories
                    const cardCategories = Array.from(card.querySelectorAll('.category-tag'))
                        .map(tag => tag.textContent.trim().toLowerCase());
                    visible = filters.categories.some(c => cardCategories.includes(c));
                }
                
                if (visible && filters.searchQuery) {
                    // Check if card matches search query
                    const cardText = card.textContent.toLowerCase();
                    visible = cardText.includes(filters.searchQuery.toLowerCase());
                }
                
                card.style.display = visible ? '' : 'none';
            });
        }, 300);
    }
});
