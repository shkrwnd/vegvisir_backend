"""Add hours column (if missing) and upsert vendor data; ensure Barnes & Noble accepts Raider card

Revision ID: update_vendors_add_hours_20251115
Revises: add_vendors_table_20251115
Create Date: 2025-11-15 17:10:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'update_vendors_add_hours_20251115'
down_revision: Union[str, Sequence[str], None] = 'add_vendors_table_20251115'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add hours column if it doesn't already exist (Postgres supports IF NOT EXISTS)
    op.execute("""
    ALTER TABLE vendors
    ADD COLUMN IF NOT EXISTS hours VARCHAR;
    ALTER TABLE vendors
    ADD COLUMN IF NOT EXISTS accepts_meal_plan BOOLEAN DEFAULT true;
    """)

    # Upsert canonical vendor data (hours + accepts_raider_card). Use ON CONFLICT to update existing rows.
    op.execute("""
    INSERT INTO vendors (name, category, description, location, hours, accepts_raider_card, accepts_meal_plan, is_active)
    VALUES
        ('Stonsby Commons', 'dining', 'Attached to Woodward Hall, Stonsby Commons is the main residential dining hall on campus, and is open to any student with a meal plan. Accepts meal plan flex dollars only.', '91 Bleeker Street', 'Sunday: 11:00 AM - 8:00 PM\nMonday-Wednesday: 7:30 AM - 10:30 PM\nThursday-Friday: 7:30 AM - 8:00 PM\nSaturday: 11:00 AM - 8:00 PM', true, true),
        ('JBJ Soul Kitchen', 'dining', 'Located on the second floor of the Paul Robeson Campus Center. JBJ Soul Kitchen is a non-profit Community Restaurant established by the Jon Bon Jovi Soul Foundation. Accepts both meal plan and real money.', '350 Dr Martin Luther King Jr Blvd (PRCC)', 'Saturday: 5:00 PM - 7:00 PM\nSunday: 11:30 AM - 1:30 PM\nMonday: Closed\nTuesday: Closed\nWednesday: 5:00 PM - 7:00 PM\nThursday: 5:00 PM - 7:00 PM\nFriday: 11:30 AM - 1:30 PM, 5:00 PM - 7:00 PM', true, true),
        ('On the RU-N', 'retail', 'Convenience store located in the lower level of the Paul Robeson Campus Center. Accepts flex dollars.', '350 Dr Martin Luther King Jr Blvd (PRCC)', 'Monday-Thursday: 10:00 AM - 6:00 PM\nFriday: 10:00 AM - 4:00 PM', true, true),
        ('Robeson Food Court', 'dining', 'Food court located in the lower level of the Paul Robeson Campus Center. Accepts flex dollars.', '350 Dr Martin Luther King Jr Blvd (PRCC)', 'Monday-Friday: 11:00 AM - 5:00 PM', true, true),
        ('Starbucks (PRCC)', 'dining', 'Starbucks located in the lower level of the Paul Robeson Campus Center. Accepts flex dollars.', '350 Dr Martin Luther King Jr Blvd (PRCC)', 'Monday-Thursday: 8:00 AM - 8:00 PM\nFriday: 8:00 AM - 4:00 PM\nSaturday: 8:00 AM - 1:00 PM', true, true),
        ('Starbucks (RBS)', 'dining', 'Starbucks located in the Rutgers Business School. Accepts flex dollars.', '1 Washington Place (RBS)', 'Monday-Thursday: 8:00 AM - 8:00 PM\nFriday: 8:00 AM - 4:00 PM', true, true),
        ('Barnes & Noble University Bookstore Newark', 'retail', 'Rutgers University''s official campus bookstore.', '42 Halsey Street', 'Monday: 10:00 AM - 5:00 PM\nTuesday: 10:00 AM - 5:00 PM\nWednesday: 10:00 AM - 5:00 PM\nThursday: 10:00 AM - 5:00 PM\nFriday: 10:00 AM - 5:00 PM\nSaturday: Closed\nSunday: Closed', true, false, true)
    ON CONFLICT (name) DO UPDATE
    SET
        category = EXCLUDED.category,
        description = EXCLUDED.description,
        location = EXCLUDED.location,
        hours = EXCLUDED.hours,
        accepts_raider_card = EXCLUDED.accepts_raider_card,
        accepts_meal_plan = EXCLUDED.accepts_meal_plan,
        is_active = EXCLUDED.is_active;
    """)


def downgrade() -> None:
    # Revert Barnes & Noble accepts_raider_card back to false (best-effort) and remove hours column.
    op.execute("""
    UPDATE vendors
    SET accepts_raider_card = false,
        accepts_meal_plan = true
    WHERE name ILIKE 'barnes%noble%';
    """)

    op.execute("""
    ALTER TABLE vendors
    DROP COLUMN IF EXISTS hours;
    ALTER TABLE vendors
    DROP COLUMN IF EXISTS accepts_meal_plan;
    """)
