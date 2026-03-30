# Nepaliकला Backend

A complete backend and admin panel for the Nepaliकला art marketplace, featuring Django for admin/user management and FastAPI for REST APIs.

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │────│  FastAPI        │    │   PostgreSQL    │
│   (HTML/CSS/JS) │    │  (REST API)     │────│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              │
                       ┌──────▼──────────┐
                       │   Django        │
                       │   (Admin Panel) │
                       └─────────────────┘
```

## Project Structure

```
backend/
├── django_admin/          # Django admin panel
│   ├── apps/
│   │   ├── users/         # User management, authentication
│   │   ├── artworks/      # Categories, Artists, Artworks
│   │   ├── orders/        # Orders, Cart, Partnerships
│   │   ├── blog/          # Blog posts, Categories
│   │   └── media/         # Media library
│   ├── nepalikala_admin/  # Django project config
│   └── requirements.txt
│
├── fastapi_api/           # FastAPI REST API
│   ├── app/
│   │   ├── api/v1/        # API endpoints
│   │   ├── core/          # Config, security, database
│   │   └── schemas/       # Pydantic models
│   ├── main.py
│   └── requirements.txt
│
├── scripts/               # Utility scripts
│   └── seed_data.py       # Database seeding
│
├── docker-compose.yml     # Docker orchestration
├── Dockerfile.django
├── Dockerfile.fastapi
└── .env.example
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- OR Python 3.11+ with pip

### Using Docker (Recommended)

1. **Clone and navigate to the backend directory:**

```bash
cd backend
```

2. **Create environment file:**

```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start all services:**

```bash
docker-compose up --build
```

This will start:
- PostgreSQL database on port 5432
- Django admin panel on http://localhost:8000
- FastAPI on http://localhost:8001

4. **Access the services:**

| Service | URL | Credentials |
|---------|-----|-------------|
| Django Admin | http://localhost:8000/admin | admin@nepalikala.art / admin123 |
| FastAPI Docs | http://localhost:8001/docs | - |
| FastAPI ReDoc | http://localhost:8001/redoc | - |

5. **Seed sample data (optional):**

```bash
docker-compose exec django python scripts/seed_data.py
```

### Manual Setup (Development)

#### Django Admin

```bash
cd django_admin
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create database
createdb nepalikala

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

#### FastAPI

```bash
cd fastapi_api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login and get token |
| POST | `/api/v1/auth/logout` | Logout |
| GET | `/api/v1/auth/me` | Get current user |
| POST | `/api/v1/auth/refresh` | Refresh access token |

### Artworks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/artworks/` | List artworks (with filters) |
| GET | `/api/v1/artworks/{id}` | Get artwork details |
| GET | `/api/v1/artworks/categories` | List categories |
| POST | `/api/v1/artworks/{id}/view` | Record artwork view |

### Artists

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/artists/` | List artists |
| GET | `/api/v1/artists/featured` | Featured artists |
| GET | `/api/v1/artists/{id}` | Get artist details |
| GET | `/api/v1/artists/{id}/artworks` | Artist's artworks |
| GET | `/api/v1/artists/{id}/stats` | Artist statistics |

### Orders & Cart

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/orders/cart` | Get cart |
| POST | `/api/v1/orders/cart/items` | Add to cart |
| PATCH | `/api/v1/orders/cart/items/{id}` | Update quantity |
| DELETE | `/api/v1/orders/cart/items/{id}` | Remove from cart |
| POST | `/api/v1/orders/checkout/session` | Create checkout |
| POST | `/api/v1/orders/checkout/verify` | Verify payment |
| GET | `/api/v1/orders/` | List orders |
| GET | `/api/v1/orders/{id}` | Get order |

### Blog

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/blog/posts` | List posts |
| GET | `/api/v1/blog/posts/{slug}` | Get post |
| GET | `/api/v1/blog/categories` | List categories |
| POST | `/api/v1/blog/posts/{id}/like` | Like post |

### Admin (Requires admin role)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/admin/dashboard` | Dashboard stats |
| GET | `/api/v1/admin/analytics` | Analytics data |
| GET | `/api/v1/admin/revenue` | Revenue report |
| GET | `/api/v1/admin/inventory` | Inventory status |

## Frontend Integration Examples

### JavaScript/Fetch Example

```javascript
const API_BASE_URL = 'http://localhost:8001/api/v1';

// Helper to make authenticated requests
async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('accessToken');
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
            ...options.headers,
        },
    });
    return response.json();
}

// Fetch artworks with filters
async function fetchArtworks(filters = {}) {
    const params = new URLSearchParams(filters);
    return apiRequest(`/artworks/?${params}`);
}

// Login
async function login(email, password) {
    const response = await apiRequest('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
    });

    if (response.access_token) {
        localStorage.setItem('accessToken', response.access_token);
        localStorage.setItem('user', JSON.stringify(response.user));
    }
    return response;
}

// Add to cart
async function addToCart(artworkId, quantity = 1) {
    return apiRequest('/orders/cart/items', {
        method: 'POST',
        body: JSON.stringify({ artwork_id: artworkId, quantity }),
    });
}

// Usage examples
fetchArtworks({ category: 'thangka', artwork_type: 'original' })
    .then(data => console.log(data.items));

login('customer@example.com', 'demo123456')
    .then(data => console.log('Logged in:', data.user));
```

### Python Example

```python
import requests

BASE_URL = "http://localhost:8001/api/v1"

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "customer@example.com",
    "password": "demo123456"
})
token = response.json()["access_token"]

# Set auth header
headers = {"Authorization": f"Bearer {token}"}

# Get artworks
artworks = requests.get(
    f"{BASE_URL}/artworks/?category=thangka",
    headers=headers
).json()

# Get cart
cart = requests.get(f"{BASE_URL}/orders/cart", headers=headers).json()
```

## Authentication Flow

1. **Register** → POST `/api/v1/auth/register`
2. **Login** → POST `/api/v1/auth/login` → Returns JWT token
3. **Use token** → Include in `Authorization: Bearer <token>` header
4. **Refresh** → POST `/api/v1/auth/refresh` before token expires

## Role-Based Access

| Role | Permissions |
|------|-------------|
| Super Admin | Full access to everything |
| Admin | Manage content, users, orders |
| Editor | Create/edit content, blog posts |
| Support | View orders, respond to enquiries |
| Artist | Manage own artworks, view sales |
| Customer | Browse, purchase, manage profile |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_DB` | Database name | nepalikala |
| `POSTGRES_USER` | Database user | postgres |
| `POSTGRES_PASSWORD` | Database password | - |
| `DJANGO_SECRET_KEY` | Django secret key | - |
| `SECRET_KEY` | FastAPI secret key | - |
| `DEBUG` | Debug mode | False |
| `CORS_ORIGINS` | Allowed CORS origins | - |

## Database Schema

### Users
- `User` - Extended user model with roles
- `Artist` - Artist profile linked to user
- `UserActivity` - Activity tracking

### Artworks
- `Category` - Art categories
- `Artwork` - Artworks with variants
- `ArtworkView` - View analytics
- `ArtistApplication` - Artist sign-ups

### Commerce
- `Order` - Customer orders
- `OrderItem` - Line items
- `CartItem` - Shopping cart
- `PartnershipEnquiry` - Business enquiries

### Content
- `BlogPost` - Blog articles
- `BlogCategory` - Blog categories
- `BlogComment` - Comments
- `Media` - File uploads

## Security Features

- JWT token-based authentication
- Role-based access control (RBAC)
- CORS protection
- Password hashing with bcrypt
- SQL injection prevention (SQLAlchemy/ORM)
- XSS protection (Django templates)
- CSRF tokens for Django admin

## Deployment

### VPS/Cloud Deployment

1. **Set up environment:**

```bash
export DJANGO_SECRET_KEY="your-production-secret"
export SECRET_KEY="your-fastapi-secret"
export DEBUG="False"
export POSTGRES_PASSWORD="strong-password"
```

2. **Build and run:**

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

3. **Run migrations:**

```bash
docker-compose exec django python manage.py migrate
docker-compose exec django python manage.py collectstatic --noinput
```

4. **Create superuser:**

```bash
docker-compose exec django python manage.py createsuperuser
```

### Environment-Specific Considerations

- Use a reverse proxy (Nginx/Traefik) for SSL
- Configure backup for PostgreSQL
- Set up monitoring (Prometheus/Grafana)
- Configure log aggregation
- Use environment-specific `.env` files

## Development

### Running Tests

```bash
# Django
cd django_admin
python manage.py test

# FastAPI
cd fastapi_api
pytest
```

### Code Style

```bash
# Format Python code
black django_admin/ fastapi_api/

# Lint
flake8 django_admin/ fastapi_api/
```

## Troubleshooting

### Database Connection Issues

```bash
# Reset database
docker-compose down -v
docker-compose up -d db
```

### Migration Issues

```bash
# Reset migrations
docker-compose exec django python manage.py migrate --run-syncdb
```

### Clear Docker Cache

```bash
docker-compose down
docker system prune -a
docker-compose up --build
```

## License

This project is proprietary software for Nepaliकला.

## Support

For support, contact: support@nepalikala.art
