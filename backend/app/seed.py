# backend/app/seed.py

from app import create_app, db
from app.models import User, ProviderProfile, Work
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# ------------------------
# 1) Admin User
# ------------------------
if not User.query.filter_by(email="elior@gmail.com").first():
    admin = User(
        email="elior@gmail.com",
        password_hash=generate_password_hash("123"),
        role="admin",
        full_name="Admin User"
    )
    db.session.add(admin)
    db.session.commit()
    print("Seeded Admin User")

# ------------------------
# 2) Existing “Alice 3D Prints” provider
# ------------------------
if not User.query.filter_by(email="provider1@example.com").first():
    u = User(
        email="provider1@example.com",
        password_hash=generate_password_hash("secret"),
        role="provider",
        full_name="Alice 3D Prints"
    )
    db.session.add(u)
    db.session.commit()
    prof = ProviderProfile(
        user_id=u.id,
        bio="High-quality SLA and FDM prints.",
        equipment_specs="Formlabs Form 3; Prusa i3 MK3S",
        pricing_info={"per_hour": 50, "per_gram": 0.10},
        location="New York, NY"
    )
    db.session.add(prof)
    db.session.commit()
    print("Seeded Alice 3D Prints")

# ------------------------
# 3) Existing “Bob Designer” customer
# ------------------------
if not User.query.filter_by(email="customer1@example.com").first():
    c = User(
        email="customer1@example.com",
        password_hash=generate_password_hash("secret"),
        role="customer",
        full_name="Bob Designer"
    )
    db.session.add(c)
    db.session.commit()
    print("Seeded Bob Designer")

# ------------------------
# 4) Tal Cohen (provider) and his works
# ------------------------
if not User.query.filter_by(email="tal.cohen@example.com").first():
    t = User(
        email="tal.cohen@example.com",
        password_hash=generate_password_hash("tal_secret"),
        role="provider",
        full_name="Tal Cohen"
    )
    db.session.add(t)
    db.session.commit()
    prof_tal = ProviderProfile(
        user_id=t.id,
        bio="Expert in decorative 3D prints and custom art pieces.",
        equipment_specs="Creality Ender 3; Prusa Mini",
        pricing_info={"per_hour": 40, "per_gram": 0.08},
        location="Tel Aviv, Israel"
    )
    db.session.add(prof_tal)
    db.session.commit()
    print("Seeded Tal Cohen")

    # Add Tal Cohen’s works
    works = [
        {"image_url": "/images/tal1.jpg", "title": "Decorative Vase"},
        {"image_url": "/images/tal2.jpg", "title": "Custom Phone Stand"},
        {"image_url": "/images/tal3.jpg", "title": "Artistic Capybara Sculpture"}
    ]
    for w in works:
        work = Work(provider_id=t.id, image_url=w["image_url"], title=w["title"])
        db.session.add(work)
    db.session.commit()
    print("Seeded Tal Cohen’s works")
