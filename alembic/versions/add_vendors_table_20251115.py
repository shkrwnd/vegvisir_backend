"""Add vendors table and vendor_id to payments

Revision ID: add_vendors_table_20251115
Revises: f2990ed00faa
Create Date: 2025-11-15 16:23:25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_vendors_table_20251115'
down_revision: Union[str, None] = 'f2990ed00faa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create vendors table (if it doesn't exist)
    bind = op.get_bind()
    
    # Check if vendors table exists
    result = bind.execute(sa.text("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'vendors'
        )
    """))
    table_exists = result.scalar()
    
    if not table_exists:
        bind.execute(sa.text("""
            CREATE TABLE vendors (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL UNIQUE,
                category VARCHAR NOT NULL,
                description VARCHAR,
                location VARCHAR,
                hours VARCHAR,
                logo_url VARCHAR,
                accepts_raider_card BOOLEAN NOT NULL DEFAULT true,
                accepts_meal_plan BOOLEAN NOT NULL DEFAULT true,
                is_active BOOLEAN NOT NULL DEFAULT true,
                created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
                updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
            )
        """))
        
        # Create index
        bind.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_vendors_id ON vendors(id)"))
        bind.commit()

    # Seed static vendor data for Rutgers-Newark
    op.execute("""
        INSERT INTO vendors (name, category, description, location, hours, accepts_raider_card, accepts_meal_plan, is_active)
        VALUES
            ('Stonsby Commons', 'dining', 'Attached to Woodward Hall, Stonsby Commons is the main residential dining hall on campus, and is open to any student with a meal plan. Accepts meal plan flex dollars only.', '91 Bleeker Street', 'Sunday: 11:00 AM - 8:00 PM\nMonday-Wednesday: 7:30 AM - 10:30 PM\nThursday-Friday: 7:30 AM - 8:00 PM\nSaturday: 11:00 AM - 8:00 PM', true, true, true),
            ('JBJ Soul Kitchen', 'dining', 'Located on the second floor of the Paul Robeson Campus Center. JBJ Soul Kitchen is a non-profit Community Restaurant established by the Jon Bon Jovi Soul Foundation. Accepts both meal plan and real money.', '350 Dr Martin Luther King Jr Blvd (PRCC)', 'Saturday: 5:00 PM - 7:00 PM\nSunday: 11:30 AM - 1:30 PM\nMonday: Closed\nTuesday: Closed\nWednesday: 5:00 PM - 7:00 PM\nThursday: 5:00 PM - 7:00 PM\nFriday: 11:30 AM - 1:30 PM, 5:00 PM - 7:00 PM', true, true, true),
            ('On the RU-N', 'retail', 'Convenience store located in the lower level of the Paul Robeson Campus Center. Accepts flex dollars.', '350 Dr Martin Luther King Jr Blvd (PRCC)', 'Monday-Thursday: 10:00 AM - 6:00 PM\nFriday: 10:00 AM - 4:00 PM', true, true, true),
            ('Robeson Food Court', 'dining', 'Food court located in the lower level of the Paul Robeson Campus Center. Accepts flex dollars.', '350 Dr Martin Luther King Jr Blvd (PRCC)', 'Monday-Friday: 11:00 AM - 5:00 PM', true, true, true),
            ('Starbucks (PRCC)', 'dining', 'Starbucks located in the lower level of the Paul Robeson Campus Center. Accepts flex dollars.', '350 Dr Martin Luther King Jr Blvd (PRCC)', 'Monday-Thursday: 8:00 AM - 8:00 PM\nFriday: 8:00 AM - 4:00 PM\nSaturday: 8:00 AM - 1:00 PM', true, true, true),
            ('Starbucks (RBS)', 'dining', 'Starbucks located in the Rutgers Business School. Accepts flex dollars.', '1 Washington Place (RBS)', 'Monday-Thursday: 8:00 AM - 8:00 PM\nFriday: 8:00 AM - 4:00 PM', true, true, true),
            ('Barnes & Noble University Bookstore', 'retail', 'Rutgers University''s official campus bookstore.', '42 Halsey Street', 'Monday: 10:00 AM - 5:00 PM\nTuesday: 10:00 AM - 5:00 PM\nWednesday: 10:00 AM - 5:00 PM\nThursday: 10:00 AM - 5:00 PM\nFriday: 10:00 AM - 5:00 PM\nSaturday: Closed\nSunday: Closed', true, false, true)
        ON CONFLICT (name) DO NOTHING;
    """)

    # Add vendor_id column to payments table (if it doesn't exist)
    result = bind.execute(sa.text("""
        SELECT EXISTS (
            SELECT FROM information_schema.columns 
            WHERE table_schema = 'public' 
            AND table_name = 'payments' 
            AND column_name = 'vendor_id'
        )
    """))
    column_exists = result.scalar()
    
    if not column_exists:
        bind.execute(sa.text("ALTER TABLE payments ADD COLUMN vendor_id INTEGER"))
        bind.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_payments_vendor_id ON payments(vendor_id)"))
        
        # Check if foreign key exists before creating
        fk_result = bind.execute(sa.text("""
            SELECT EXISTS (
                SELECT FROM information_schema.table_constraints 
                WHERE constraint_schema = 'public' 
                AND constraint_name = 'fk_payments_vendor_id'
            )
        """))
        fk_exists = fk_result.scalar()
        
        if not fk_exists:
            bind.execute(sa.text("""
                ALTER TABLE payments 
                ADD CONSTRAINT fk_payments_vendor_id 
                FOREIGN KEY (vendor_id) REFERENCES vendors(id)
            """))
        bind.commit()


def downgrade() -> None:
    # Remove vendor_id from payments table
    op.drop_constraint('fk_payments_vendor_id', 'payments', type_='foreignkey')
    op.drop_index(op.f('ix_payments_vendor_id'), table_name='payments')
    op.drop_column('payments', 'vendor_id')

    # Drop vendors table
    op.drop_index(op.f('ix_vendors_id'), table_name='vendors')
    op.drop_table('vendors')
