# Frontend Integration Guide

This guide shows how to integrate your existing HTML/CSS/JS frontend with the Nepaliकला backend.

## API Configuration

Create an `api-config.js` file in your frontend:

```javascript
// api-config.js
const API_CONFIG = {
    // Base URL for FastAPI backend
    BASE_URL: 'http://localhost:8001/api/v1',

    // Base URL for Django admin (if needed for direct access)
    ADMIN_URL: 'http://localhost:8000',

    // Request timeout in milliseconds
    TIMEOUT: 30000,

    // Default headers
    HEADERS: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API_CONFIG;
}
```

## API Client

Replace your existing `script.js` cart functions with this API-enabled version:

```javascript
// api-client.js - Add this new file

class NepaliKalaAPI {
    constructor() {
        this.baseURL = 'http://localhost:8001/api/v1';
        this.token = localStorage.getItem('accessToken');
    }

    // Set auth token after login
    setToken(token) {
        this.token = token;
        localStorage.setItem('accessToken', token);
    }

    // Clear token on logout
    clearToken() {
        this.token = null;
        localStorage.removeItem('accessToken');
        localStorage.removeItem('user');
    }

    // Make API request
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                ...API_CONFIG.HEADERS,
                ...(this.token && { 'Authorization': `Bearer ${this.token}` }),
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                if (response.status === 401) {
                    // Token expired, clear it
                    this.clearToken();
                    window.location.href = '/login.html';
                }
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // ========== AUTH ==========
    async login(email, password) {
        const data = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });

        if (data.access_token) {
            this.setToken(data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
        }

        return data;
    }

    async register(userData) {
        const data = await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });

        if (data.access_token) {
            this.setToken(data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
        }

        return data;
    }

    async logout() {
        await this.request('/auth/logout', { method: 'POST' });
        this.clearToken();
    }

    async getMe() {
        return await this.request('/auth/me');
    }

    // ========== ARTWORKS ==========
    async getArtworks(filters = {}) {
        const params = new URLSearchParams();
        Object.entries(filters).forEach(([key, value]) => {
            if (value !== undefined && value !== null) {
                params.append(key, value);
            }
        });
        return await this.request(`/artworks/?${params}`);
    }

    async getArtwork(id) {
        return await this.request(`/artworks/${id}`);
    }

    async getCategories() {
        return await this.request('/artworks/categories');
    }

    async getRelatedArtworks(id, limit = 4) {
        return await this.request(`/artworks/${id}/related?limit=${limit}`);
    }

    // ========== ARTISTS ==========
    async getArtists(filters = {}) {
        const params = new URLSearchParams(filters);
        return await this.request(`/artists/?${params}`);
    }

    async getFeaturedArtists(limit = 4) {
        return await this.request(`/artists/featured?limit=${limit}`);
    }

    async getArtist(id) {
        return await this.request(`/artists/${id}`);
    }

    async getArtistArtworks(id, filters = {}) {
        const params = new URLSearchParams(filters);
        return await this.request(`/artists/${id}/artworks?${params}`);
    }

    // ========== CART ==========
    async getCart() {
        return await this.request('/orders/cart');
    }

    async addToCart(artworkId, quantity = 1) {
        return await this.request('/orders/cart/items', {
            method: 'POST',
            body: JSON.stringify({ artwork_id: artworkId, quantity })
        });
    }

    async updateCartItem(itemId, quantity) {
        return await this.request(`/orders/cart/items/${itemId}?quantity=${quantity}`, {
            method: 'PATCH'
        });
    }

    async removeFromCart(itemId) {
        return await this.request(`/orders/cart/items/${itemId}`, {
            method: 'DELETE'
        });
    }

    async clearCart() {
        return await this.request('/orders/cart', { method: 'DELETE' });
    }

    // ========== ORDERS ==========
    async getOrders(filters = {}) {
        const params = new URLSearchParams(filters);
        return await this.request(`/orders/?${params}`);
    }

    async getOrder(id) {
        return await this.request(`/orders/${id}`);
    }

    async createCheckoutSession(shippingAddress, customerNotes = '') {
        return await this.request('/orders/checkout/session', {
            method: 'POST',
            body: JSON.stringify({
                shipping_address: shippingAddress,
                customer_notes: customerNotes
            })
        });
    }

    // ========== BLOG ==========
    async getPosts(filters = {}) {
        const params = new URLSearchParams(filters);
        return await this.request(`/blog/posts?${params}`);
    }

    async getPost(slug) {
        return await this.request(`/blog/posts/${slug}`);
    }

    async getFeaturedPosts(limit = 3) {
        return await this.request(`/blog/posts/featured?limit=${limit}`);
    }
}

// Create global instance
const api = new NepaliKalaAPI();

// Make available globally
window.NepaliKalaAPI = NepaliKalaAPI;
window.api = api;
```

## Updated Cart Functions

Update your `script.js` to use the API:

```javascript
// Updated cart functions for script.js

// Initialize cart from API
async function initCart() {
    try {
        if (api.token) {
            const cartData = await api.getCart();
            updateCartBadge(cartData.item_count);
        } else {
            // Fall back to localStorage for guest users
            updateCartBadge(getCart().length);
        }
    } catch (error) {
        console.error('Failed to load cart:', error);
    }
}

// Add to cart - Updated version
async function addToCart(item) {
    if (api.token) {
        // Logged in - use API cart
        try {
            await api.addToCart(item.id, item.qty || 1);
            const cart = await api.getCart();
            updateCartBadge(cart.item_count);
            showToast('Added to Cart', '✔', `<strong>${item.title}</strong> added successfully.`);
        } catch (error) {
            showToast('Error', '✕', 'Failed to add to cart. Please try again.');
        }
    } else {
        // Guest user - use localStorage
        const cart = getCart();
        const existing = cart.find(c => c.id === item.id && c.type === item.type);

        if (existing) {
            existing.qty = (existing.qty || 1) + 1;
        } else {
            cart.push({ ...item, qty: 1 });
        }

        saveCart(cart);
        updateCartBadge();
        showToast('Added to Cart', '✔', `<strong>${item.title}</strong> added successfully.`);
    }
}

// Get cart - Updated version
async function getCart() {
    if (api.token) {
        try {
            const cartData = await api.getCart();
            return cartData.items.map(item => ({
                id: item.artwork.id,
                title: item.artwork.title,
                price: item.artwork.price_npr,
                qty: item.quantity,
                artist: item.artwork.artist.display_name,
                type: item.artwork.artwork_type,
                img: item.artwork.main_image_url
            }));
        } catch (error) {
            return [];
        }
    }
    // Guest fallback
    try {
        return JSON.parse(localStorage.getItem(CART_KEY)) || [];
    } catch {
        return [];
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initCart();
    // ... rest of your initialization
});
```

## Dynamic Content Loading

### Load Featured Artists on Homepage

Add this to your `index.html`:

```javascript
// Load featured artists dynamically
async function loadFeaturedArtists() {
    try {
        const artists = await api.getFeaturedArtists(4);
        const container = document.querySelector('.artists-grid');

        container.innerHTML = artists.map((artist, index) => `
            <a href="artist-detail.html?id=${artist.id}" class="artist-card reveal reveal-delay-${index + 1}">
                <div class="artist-portrait">
                    <div class="ap ap${(index % 8) + 1}"></div>
                    <div class="artist-portrait-overlay"></div>
                    <span class="artist-style-tag">${artist.style}</span>
                </div>
                <div class="artist-card-body">
                    <div class="artist-card-name">${artist.display_name}</div>
                    <div class="artist-card-loc">📍 ${artist.location}</div>
                    <div class="artist-card-works">${artist.total_works} works available</div>
                </div>
            </a>
        `).join('');
    } catch (error) {
        console.error('Failed to load artists:', error);
    }
}

// Load on page ready
document.addEventListener('DOMContentLoaded', loadFeaturedArtists);
```

### Load Artworks on Shop Page

```javascript
// Load artworks with filters
async function loadArtworks(filters = {}) {
    try {
        const data = await api.getArtworks({
            ...filters,
            page: 1,
            per_page: 24
        });

        const container = document.querySelector('.shop-grid');
        const resultsCount = document.querySelector('.results-count');

        resultsCount.innerHTML = `Showing <strong style="color:var(--ivory)">${data.items.length}</strong> of ${data.total} artworks`;

        container.innerHTML = data.items.map((artwork, index) => `
            <div class="product-card reveal ${index % 3 === 1 ? 'reveal-delay-1' : index % 3 === 2 ? 'reveal-delay-2' : ''}"
                 data-category="${artwork.artwork_type}"
                 data-product-id="${artwork.id}"
                 data-title="${artwork.title}"
                 data-price="${artwork.price_npr}"
                 data-artist="${artwork.artist.display_name}"
                 data-type="${artwork.artwork_type}">
                <div class="product-thumb">
                    <div class="ap ap${(index % 8) + 1}"></div>
                    <span class="product-badge badge-${artwork.artwork_type}">
                        ${artwork.artwork_type === 'original' ? 'Original' : 'Print'}
                    </span>
                    <div class="product-thumb-overlay">
                        <a href="product-detail.html?id=${artwork.id}" class="thumb-action">Quick View</a>
                        <button class="thumb-action btn-cart" onclick="addToCartFromAPI('${artwork.id}')">+ Cart</button>
                    </div>
                </div>
                <div class="product-info">
                    <a href="artist-detail.html?id=${artwork.artist.id}" class="product-artist-link">${artwork.artist.display_name}</a>
                    <a href="product-detail.html?id=${artwork.id}" class="product-title">${artwork.title}</a>
                    <div class="product-meta">${artwork.medium} · ${artwork.dimensions}</div>
                    <div class="product-price-row">
                        <span class="product-price">NPR ${artwork.price_npr.toLocaleString()}</span>
                        <button class="btn-cart" onclick="addToCartFromAPI('${artwork.id}')">Cart</button>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load artworks:', error);
    }
}

// Add to cart from API
async function addToCartFromAPI(artworkId) {
    try {
        const artwork = await api.getArtwork(artworkId);
        await addToCart({
            id: artwork.id,
            title: artwork.title,
            price: artwork.price_npr,
            artist: artwork.artist.display_name,
            type: artwork.artwork_type,
            img: artwork.main_image_url
        });
    } catch (error) {
        console.error('Failed to add to cart:', error);
    }
}
```

## Login Page Integration

Create a simple login page:

```html
<!-- login.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Nepaliकला</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="page-hero" style="min-height: 100vh; display: flex; align-items: center; justify-content: center;">
        <div style="max-width: 400px; width: 100%; padding: 2rem; background: var(--navy-card); border: 1px solid var(--border);">
            <h1 class="section-title" style="text-align: center; margin-bottom: 2rem;">Sign In</h1>

            <form id="login-form" class="js-form">
                <div class="form-group" style="margin-bottom: 1.2rem;">
                    <label>Email</label>
                    <input type="email" name="email" required placeholder="you@example.com">
                </div>

                <div class="form-group" style="margin-bottom: 1.5rem;">
                    <label>Password</label>
                    <input type="password" name="password" required placeholder="••••••••">
                </div>

                <button type="submit" class="btn btn-primary" style="width: 100%;">Sign In</button>

                <p style="text-align: center; margin-top: 1rem; font-size: 0.85rem;">
                    Don't have an account? <a href="register.html" style="color: var(--gold);">Register</a>
                </p>
            </form>
        </div>
    </div>

    <script src="api-client.js"></script>
    <script>
        document.getElementById('login-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);

            try {
                const response = await api.login(
                    formData.get('email'),
                    formData.get('password')
                );

                // Redirect to home or intended page
                window.location.href = '/';
            } catch (error) {
                alert('Login failed. Please check your credentials.');
            }
        });
    </script>
</body>
</html>
```

## CSS Updates for API Integration

Add loading states to your CSS:

```css
/* Add to styles.css */

/* Loading state */
.loading {
    opacity: 0.6;
    pointer-events: none;
    position: relative;
}

.loading::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 24px;
    height: 24px;
    margin: -12px 0 0 -12px;
    border: 2px solid var(--gold);
    border-top-color: transparent;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Auth required indicator */
.auth-required {
    position: relative;
}

.auth-required::before {
    content: '🔒';
    position: absolute;
    right: -20px;
    font-size: 0.7rem;
    opacity: 0.7;
}
```

## Summary

To integrate your frontend:

1. **Include `api-client.js`** in all your HTML files before `script.js`
2. **Replace cart functions** with API-enabled versions
3. **Add login/logout** functionality
4. **Load dynamic content** using the API for artists, artworks, etc.
5. **Handle authentication** - show/hide elements based on login state

The API client handles all authentication automatically - it will:
- Store tokens in localStorage
- Include tokens in authenticated requests
- Redirect to login when tokens expire
- Fall back to localStorage cart for guest users
