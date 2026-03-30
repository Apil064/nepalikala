"""
Seed data script for Nepaliकला.
This script creates sample data for testing the application.
"""
import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nepalikala_admin.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'django_admin'))
django.setup()

from apps.users.models import User
from apps.artworks.models import Category, Artist, Artwork, ArtistApplication
from apps.orders.models import Order, OrderItem
from apps.blog.models import BlogCategory, BlogPost


def create_categories():
    """Create art categories."""
    categories = [
        {"name": "Thangka", "slug": "thangka", "description": "Traditional Tibetan Buddhist paintings", "display_order": 1},
        {"name": "Modern & Contemporary", "slug": "modern", "description": "Contemporary Nepali art", "display_order": 2},
        {"name": "Madhubani", "slug": "madhubani", "description": "Traditional Mithila art from Janakpur", "display_order": 3},
        {"name": "Sculpture & Craft", "slug": "sculpture", "description": "Traditional and modern sculptures", "display_order": 4},
        {"name": "Digital Art", "slug": "digital", "description": "Digital and new media art", "display_order": 5},
        {"name": "Photography", "slug": "photography", "description": "Photographic art", "display_order": 6},
    ]

    print("Creating categories...")
    for cat_data in categories:
        Category.objects.get_or_create(slug=cat_data["slug"], defaults=cat_data)
    print(f"Created {len(categories)} categories")


def create_users():
    """Create sample users."""
    users_data = [
        {
            "email": "admin@nepalikala.art",
            "username": "admin",
            "first_name": "Super",
            "last_name": "Admin",
            "role": User.Role.SUPER_ADMIN,
            "is_staff": True,
            "is_superuser": True,
        },
        {
            "email": "editor@nepalikala.art",
            "username": "editor",
            "first_name": "Content",
            "last_name": "Editor",
            "role": User.Role.EDITOR,
        },
        {
            "email": "karma.lama@example.com",
            "username": "karmalama",
            "first_name": "Karma",
            "last_name": "Lama",
            "role": User.Role.ARTIST,
            "location": "Boudhanath, Kathmandu",
            "style": "Thangka",
            "bio": "Master Thangka painter with 20 years of experience",
        },
        {
            "email": "sita.maharjan@example.com",
            "username": "sitamaharjan",
            "first_name": "Sita",
            "last_name": "Maharjan",
            "role": User.Role.ARTIST,
            "location": "Lalitpur, Patan",
            "style": "Oil & Acrylic",
            "bio": "Contemporary artist specializing in modern Nepali themes",
        },
        {
            "email": "geeta.devi@example.com",
            "username": "geetadevi",
            "first_name": "Geeta",
            "last_name": "Devi",
            "role": User.Role.ARTIST,
            "location": "Janakpur",
            "style": "Madhubani",
            "bio": "Traditional Madhubani artist preserving ancient techniques",
        },
        {
            "email": "anil.tamang@example.com",
            "username": "aniltamang",
            "first_name": "Anil",
            "last_name": "Tamang",
            "role": User.Role.ARTIST,
            "location": "Thamel, Kathmandu",
            "style": "Digital",
            "bio": "Digital artist blending tradition with technology",
        },
        {
            "email": "customer@example.com",
            "username": "customer",
            "first_name": "Ram",
            "last_name": "Sharma",
            "role": User.Role.CUSTOMER,
        },
    ]

    print("Creating users...")
    created_users = {}
    for user_data in users_data:
        email = user_data.pop("email")
        username = user_data.pop("username")
        password = "demo123456"

        user, created = User.objects.get_or_create(
            email=email,
            defaults={**user_data, "username": username}
        )
        if created:
            user.set_password(password)
            user.save()
            print(f"  Created user: {email} (password: {password})")
        else:
            print(f"  User exists: {email}")

        created_users[username] = user

    return created_users


def create_artists(users):
    """Create artist profiles."""
    artists_data = [
        {
            "user": users["karmalama"],
            "bio": "Karma Lama is a master Thangka painter who learned the ancient art from his grandfather in the monasteries of Tibet. His works are characterized by meticulous attention to detail and traditional iconography.",
            "location": "Boudhanath, Kathmandu",
            "style": "Thangka",
            "years_experience": 20,
            "education": "Traditional apprenticeship under master Thangka painter",
            "awards": "National Art Award 2020, Himalayan Art Excellence Award 2018",
            "exhibitions": "Solo exhibitions in Kathmandu, Delhi, New York, and London",
            "is_verified": True,
            "is_featured": True,
        },
        {
            "user": users["sitamaharjan"],
            "bio": "Sita Maharjan is a contemporary artist whose work explores the intersection of traditional Nepali culture and modern urban life. Her oil paintings capture the essence of Kathmandu Valley.",
            "location": "Lalitpur, Patan",
            "style": "Oil & Acrylic",
            "years_experience": 15,
            "education": "BFA from Kathmandu University, MFA from Delhi College of Art",
            "awards": "Young Artist Award 2019",
            "is_verified": True,
            "is_featured": True,
        },
        {
            "user": users["geetadevi"],
            "bio": "Geeta Devi is a renowned Madhubani artist from Janakpur, continuing the ancient Mithila tradition passed down through generations of women in her family.",
            "location": "Janakpur",
            "style": "Madhubani",
            "years_experience": 25,
            "education": "Learned traditional techniques from family",
            "awards": "President's Award for Folk Art 2021",
            "is_verified": True,
            "is_featured": True,
        },
        {
            "user": users["aniltamang"],
            "bio": "Anil Tamang creates stunning digital artworks that reimagine Nepali mythology and landscapes through a contemporary lens. His work bridges tradition and technology.",
            "location": "Thamel, Kathmandu",
            "style": "Digital",
            "years_experience": 8,
            "education": "Self-taught, with courses in digital design",
            "is_verified": True,
            "is_featured": True,
        },
    ]

    print("Creating artist profiles...")
    artists = {}
    for artist_data in artists_data:
        user = artist_data["user"]
        artist, created = Artist.objects.get_or_create(
            user=user,
            defaults=artist_data
        )
        if created:
            print(f"  Created artist profile: {user.get_full_name()}")
            artists[user.username] = artist
        else:
            print(f"  Artist exists: {user.get_full_name()}")
            artists[user.username] = artist

    return artists


def create_artworks(artists, categories):
    """Create sample artworks."""
    thangka_cat = next((c for c in categories if c.slug == "thangka"), None)
    modern_cat = next((c for c in categories if c.slug == "modern"), None)
    madhubani_cat = next((c for c in categories if c.slug == "madhubani"), None)
    digital_cat = next((c for c in categories if c.slug == "digital"), None)

    artworks_data = [
        # Karma Lama - Thangka
        {
            "artist": artists["karmalama"],
            "title": "Himalayan Dawn Thangka",
            "slug": "himalayan-dawn-thangka",
            "description": "A stunning depiction of the Himalayan sunrise in traditional Thangka style. Natural pigments on cotton create a luminous effect that captures the spiritual essence of the mountains.",
            "artwork_type": Artwork.ArtworkType.ORIGINAL,
            "medium": "Natural pigments on cotton",
            "dimensions": "60×80 cm",
            "year_created": 2024,
            "price_npr": Decimal("85000"),
            "categories": [thangka_cat],
            "is_featured": True,
        },
        {
            "artist": artists["karmalama"],
            "title": "Sacred Mandala",
            "slug": "sacred-mandala",
            "description": "An intricate mandala representing the universe in Buddhist cosmology. Gold leaf accents add divine radiance to this meditation piece.",
            "artwork_type": Artwork.ArtworkType.ORIGINAL,
            "medium": "Gold leaf on cotton",
            "dimensions": "90×90 cm",
            "year_created": 2024,
            "price_npr": Decimal("120000"),
            "categories": [thangka_cat],
            "is_featured": True,
        },
        # Sita Maharjan - Modern
        {
            "artist": artists["sitamaharjan"],
            "title": "Pokhara Lakeside",
            "slug": "pokhara-lakeside",
            "description": "A serene view of Phewa Lake at dawn, capturing the reflection of the Annapurna range in still waters.",
            "artwork_type": Artwork.ArtworkType.PRINT,
            "medium": "Giclée print",
            "dimensions": "A2 (42×59.4 cm)",
            "year_created": 2024,
            "price_npr": Decimal("4500"),
            "edition_size": 30,
            "prints_available": 18,
            "categories": [modern_cat],
            "is_featured": True,
        },
        {
            "artist": artists["sitamaharjan"],
            "title": "Kathmandu Sunrise",
            "slug": "kathmandu-sunrise",
            "description": "The ancient city awakens as golden light bathes the temples and pagodas of Patan Durbar Square.",
            "artwork_type": Artwork.ArtworkType.ORIGINAL,
            "medium": "Oil on linen",
            "dimensions": "70×100 cm",
            "year_created": 2024,
            "price_npr": Decimal("45000"),
            "categories": [modern_cat],
        },
        # Geeta Devi - Madhubani
        {
            "artist": artists["geetadevi"],
            "title": "Janakpur Festivity",
            "slug": "janakpur-festivity",
            "description": "Vibrant celebration of the Vivah Panchami festival with traditional Madhubani motifs depicting scenes from the Ramayana.",
            "artwork_type": Artwork.ArtworkType.ORIGINAL,
            "medium": "Madhubani on handmade paper",
            "dimensions": "50×70 cm",
            "year_created": 2024,
            "price_npr": Decimal("28000"),
            "categories": [madhubani_cat],
            "is_featured": True,
        },
        # Anil Tamang - Digital
        {
            "artist": artists["aniltamang"],
            "title": "Everest Spirit",
            "slug": "everest-spirit",
            "description": "A digital interpretation of the world's highest peak, blending photography with digital painting techniques.",
            "artwork_type": Artwork.ArtworkType.PRINT,
            "medium": "Giclée print",
            "dimensions": "30×40 cm",
            "year_created": 2024,
            "price_npr": Decimal("2800"),
            "edition_size": 50,
            "prints_available": 3,
            "categories": [digital_cat],
        },
    ]

    print("Creating artworks...")
    for art_data in artworks_data:
        categories = art_data.pop("categories", [])
        artwork, created = Artwork.objects.get_or_create(
            slug=art_data["slug"],
            defaults=art_data
        )
        if created:
            artwork.categories.set(categories)
            print(f"  Created artwork: {artwork.title}")
        else:
            print(f"  Artwork exists: {artwork.title}")


def create_blog_categories():
    """Create blog categories."""
    categories = [
        {"name": "Tradition", "slug": "tradition"},
        {"name": "Folk Art", "slug": "folk-art"},
        {"name": "Contemporary", "slug": "contemporary"},
        {"name": "Craft", "slug": "craft"},
        {"name": "Artist Stories", "slug": "artist-stories"},
    ]

    print("Creating blog categories...")
    for cat_data in categories:
        BlogCategory.objects.get_or_create(slug=cat_data["slug"], defaults=cat_data)
    print(f"Created {len(categories)} blog categories")


def create_blog_posts(users, artists):
    """Create sample blog posts."""
    posts_data = [
        {
            "title": "The Secrets of Thangka Pigments",
            "slug": "secrets-thangka-pigments",
            "subtitle": "Exploring the natural colors of the Himalayas",
            "excerpt": "Discover the ancient techniques of preparing pigments for Thangka painting.",
            "content": """Thangka painting is one of the most revered art forms in the Himalayan region. The pigments used in these sacred paintings are derived from natural minerals and plants found in the mountains.

## The Colors of the Earth

Traditional Thangka artists use a palette of mineral pigments that have remained unchanged for centuries:

- **Lapis Lazuli**: Provides the deep blues that represent the sky and water
- **Cinnabar**: Creates the brilliant reds for robes and sacred objects
- **Malachite**: Yields the greens of nature and prosperity
- **Gold**: Ground and applied as paint or as leaf for divine radiance

## The Process

The preparation of these pigments is a meditation in itself. Each color must be ground to the perfect fineness and mixed with a binding medium of animal glue and water. This laborious process can take days for a single color.

## Preservation

These natural pigments not only create the distinctive look of Thangka paintings but also ensure their longevity. Properly cared for, a Thangka painted with natural pigments can last for centuries without fading.""",
            "author": users["editor"],
            "categories_slugs": ["tradition"],
            "is_featured": True,
            "status": BlogPost.Status.PUBLISHED,
        },
        {
            "title": "Geeta Devi: Madhubani Lives",
            "slug": "geeta-devi-madhubani-lives",
            "subtitle": "A portrait of a master folk artist",
            "excerpt": "Meet the artist keeping the ancient Mithila tradition alive.",
            "content": """In the heart of Janakpur, Geeta Devi continues a tradition that has been passed down through generations of women in her family...

[Article continues with artist profile]""",
            "author": users["editor"],
            "featured_artist": artists.get("geetadevi"),
            "categories_slugs": ["folk-art", "artist-stories"],
            "is_featured": True,
            "status": BlogPost.Status.PUBLISHED,
        },
    ]

    print("Creating blog posts...")
    categories = {cat.slug: cat for cat in BlogCategory.objects.all()}

    for post_data in posts_data:
        categories_slugs = post_data.pop("categories_slugs", [])
        featured_artist = post_data.pop("featured_artist", None)

        post, created = BlogPost.objects.get_or_create(
            slug=post_data["slug"],
            defaults=post_data
        )
        if created:
            post.categories.set([categories[slug] for slug in categories_slugs])
            print(f"  Created blog post: {post.title}")
        else:
            print(f"  Blog post exists: {post.title}")


def create_artist_applications():
    """Create sample artist applications."""
    applications = [
        {
            "first_name": "Anita",
            "last_name": "Shrestha",
            "email": "anita.shrestha@example.com",
            "location": "Pokhara",
            "art_style": "Watercolour",
            "years_experience": 8,
            "portfolio_description": "I specialize in watercolour landscapes of the Annapurna region.",
        },
        {
            "first_name": "Bikash",
            "last_name": "Gurung",
            "email": "bikash.gurung@example.com",
            "location": "Chitwan",
            "art_style": "Digital",
            "years_experience": 4,
            "portfolio_description": "Digital illustrations inspired by Tharu culture.",
        },
    ]

    print("Creating artist applications...")
    for app_data in applications:
        app, created = ArtistApplication.objects.get_or_create(
            email=app_data["email"],
            defaults=app_data
        )
        if created:
            print(f"  Created application: {app.full_name}")
        else:
            print(f"  Application exists: {app.full_name}")


def main():
    """Run all seed functions."""
    print("=" * 60)
    print("Nepaliकła Seed Data Script")
    print("=" * 60)
    print()

    try:
        # Create data in order of dependencies
        create_categories()
        users = create_users()
        artists = create_artists(users)
        categories = list(Category.objects.all())
        create_artworks(artists, categories)
        create_blog_categories()
        create_blog_posts(users, artists)
        create_artist_applications()

        print()
        print("=" * 60)
        print("Seed data created successfully!")
        print("=" * 60)
        print()
        print("Login credentials:")
        print("  Admin: admin@nepalikala.art / demo123456")
        print("  Editor: editor@nepalikala.art / demo123456")
        print("  Customer: customer@example.com / demo123456")
        print()
        print("All artist users: <email> / demo123456")

    except Exception as e:
        print(f"\nError creating seed data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
