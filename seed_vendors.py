"""
Seed script to populate the database with Rutgers-Newark vendors that accept Raider card.
Run this script once to create the initial vendor list.

Usage: python seed_vendors.py
"""
from app.database import SessionLocal
from app.models.vendor import Vendor


def seed_vendors():
    """Create vendors for Rutgers-Newark campus."""
    db = SessionLocal()

    # Check if vendors already exist
    existing_vendors = db.query(Vendor).count()
    if existing_vendors > 0:
        print(f"Vendors already exist ({existing_vendors} found). Skipping seed.")
        db.close()
        return

    vendors = [
        {
            "name": "Stonsby Commons",
            "category": "dining",
            "description": "Attached to Woodward Hall, Stonsby Commons is the main residential dining hall on campus, and is open to any student with a meal plan. Accepts meal plan flex dollars only.",
            "location": "91 Bleeker Street",
            "hours": "Sunday: 11:00 AM - 8:00 PM\nMonday-Wednesday: 7:30 AM - 10:30 PM\nThursday-Friday: 7:30 AM - 8:00 PM\nSaturday: 11:00 AM - 8:00 PM",
            "accepts_raider_card": True,
            "accepts_meal_plan": True,
            "is_active": True
        },
        {
            "name": "JBJ Soul Kitchen",
            "category": "dining",
            "description": "Located on the second floor of the Paul Robeson Campus Center. JBJ Soul Kitchen is a non-profit Community Restaurant established by the Jon Bon Jovi Soul Foundation. Accepts both meal plan and real money.",
            "location": "350 Dr Martin Luther King Jr Blvd (PRCC)",
            "hours": "Saturday: 5:00 PM - 7:00 PM\nSunday: 11:30 AM - 1:30 PM\nMonday: Closed\nTuesday: Closed\nWednesday: 5:00 PM - 7:00 PM\nThursday: 5:00 PM - 7:00 PM\nFriday: 11:30 AM - 1:30 PM, 5:00 PM - 7:00 PM",
            "accepts_raider_card": True,
            "accepts_meal_plan": True,
            "is_active": True
        },
        {
            "name": "On the RU-N",
            "category": "retail",
            "description": "Convenience store located in the lower level of the Paul Robeson Campus Center. Accepts flex dollars.",
            "location": "350 Dr Martin Luther King Jr Blvd (PRCC)",
            "hours": "Monday-Thursday: 10:00 AM - 6:00 PM\nFriday: 10:00 AM - 4:00 PM",
            "accepts_raider_card": True,
            "accepts_meal_plan": True,
            "is_active": True
        },
        {
            "name": "Robeson Food Court",
            "category": "dining",
            "description": "Food court located in the lower level of the Paul Robeson Campus Center. Accepts flex dollars.",
            "location": "350 Dr Martin Luther King Jr Blvd (PRCC)",
            "hours": "Monday-Friday: 11:00 AM - 5:00 PM",
            "accepts_raider_card": True,
            "accepts_meal_plan": True,
            "is_active": True
        },
        {
            "name": "Starbucks (PRCC)",
            "category": "dining",
            "description": "Starbucks located in the lower level of the Paul Robeson Campus Center. Accepts flex dollars.",
            "location": "350 Dr Martin Luther King Jr Blvd (PRCC)",
            "hours": "Monday-Thursday: 8:00 AM - 8:00 PM\nFriday: 8:00 AM - 4:00 PM\nSaturday: 8:00 AM - 1:00 PM",
            "accepts_raider_card": True,
            "accepts_meal_plan": True,
            "is_active": True
        },
        {
            "name": "Starbucks (RBS)",
            "category": "dining",
            "description": "Starbucks located in the Rutgers Business School. Accepts flex dollars.",
            "location": "1 Washington Place (RBS)",
            "hours": "Monday-Thursday: 8:00 AM - 8:00 PM\nFriday: 8:00 AM - 4:00 PM",
            "accepts_raider_card": True,
            "accepts_meal_plan": True,
            "is_active": True
        },
        {
            "name": "Barnes & Noble University Bookstore Newark",
            "category": "retail",
            "description": "Rutgers University's official campus bookstore.",
            "location": "42 Halsey Street",
            "hours": "Monday: 10:00 AM - 5:00 PM\nTuesday: 10:00 AM - 5:00 PM\nWednesday: 10:00 AM - 5:00 PM\nThursday: 10:00 AM - 5:00 PM\nFriday: 10:00 AM - 5:00 PM\nSaturday: Closed\nSunday: Closed",
            "accepts_raider_card": True,  # Accepts Raider card (real money)
            "accepts_meal_plan": False,  # Does NOT accept meal plan flex dollars
            "is_active": True
        }
    ]

    try:
        for vendor_data in vendors:
            vendor = Vendor(**vendor_data)
            db.add(vendor)

        db.commit()
        print(f"[SUCCESS] Successfully seeded {len(vendors)} vendors!")

        # Display the created vendors
        print("\nCreated vendors:")
        all_vendors = db.query(Vendor).all()
        for vendor in all_vendors:
            raider = "YES" if vendor.accepts_raider_card else "NO"
            meal = "YES" if getattr(vendor, 'accepts_meal_plan', None) else "NO"
            print(f"  {vendor.id}. {vendor.name}")
            print(f"     Category: {vendor.category} | Location: {vendor.location}")
            print(f"     Raider Card: {raider} | Meal Plan: {meal}")
            print()

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error seeding vendors: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Seeding Rutgers-Newark Vendors")
    print("=" * 60)
    seed_vendors()
    print("=" * 60)
