from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate


class VendorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, vendor_id: int) -> Optional[Vendor]:
        """Get vendor by ID."""
        return self.db.query(Vendor).filter(Vendor.id == vendor_id).first()

    def get_by_name(self, name: str) -> Optional[Vendor]:
        """Get vendor by name."""
        return self.db.query(Vendor).filter(Vendor.name == name).first()

    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = False) -> List[Vendor]:
        """Get all vendors with pagination."""
        query = self.db.query(Vendor)

        if active_only:
            query = query.filter(Vendor.is_active == True)

        return query.offset(skip).limit(limit).all()

    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Vendor]:
        """Get vendors by category."""
        return self.db.query(Vendor).filter(
            Vendor.category == category,
            Vendor.is_active == True
        ).offset(skip).limit(limit).all()

    def create(self, vendor_data: VendorCreate) -> Vendor:
        """Create a new vendor."""
        db_vendor = Vendor(**vendor_data.model_dump())
        self.db.add(db_vendor)
        self.db.commit()
        self.db.refresh(db_vendor)
        return db_vendor

    def update(self, vendor: Vendor, vendor_data: VendorUpdate) -> Vendor:
        """Update vendor fields."""
        update_data = vendor_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(vendor, key):
                setattr(vendor, key, value)
        self.db.commit()
        self.db.refresh(vendor)
        return vendor

    def delete(self, vendor: Vendor) -> None:
        """Delete a vendor."""
        self.db.delete(vendor)
        self.db.commit()
