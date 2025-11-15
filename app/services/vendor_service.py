from sqlalchemy.orm import Session
from typing import List
from app.repositories.vendor_repository import VendorRepository
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorResponse
from app.exceptions import NotFoundError, ValidationError


class VendorService:
    def __init__(self, db: Session):
        self.db = db
        self.vendor_repo = VendorRepository(db)

    def get_vendors(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True,
        category: str = None
    ) -> List[dict]:
        """Get all vendors with optional filtering."""
        if category:
            vendors = self.vendor_repo.get_by_category(category, skip, limit)
        else:
            vendors = self.vendor_repo.get_all(skip, limit, active_only)

        return [VendorResponse.model_validate(vendor).model_dump() for vendor in vendors]

    def get_vendor(self, vendor_id: int) -> dict:
        """Get a specific vendor by ID."""
        vendor = self.vendor_repo.get_by_id(vendor_id)
        if not vendor:
            raise NotFoundError(f"Vendor with ID {vendor_id} not found")

        return VendorResponse.model_validate(vendor).model_dump()

    def create_vendor(self, vendor_data: VendorCreate) -> dict:
        """Create a new vendor."""
        # Check if vendor with same name already exists
        existing_vendor = self.vendor_repo.get_by_name(vendor_data.name)
        if existing_vendor:
            raise ValidationError(f"Vendor with name '{vendor_data.name}' already exists")

        vendor = self.vendor_repo.create(vendor_data)
        return VendorResponse.model_validate(vendor).model_dump()

    def update_vendor(self, vendor_id: int, vendor_data: VendorUpdate) -> dict:
        """Update an existing vendor."""
        vendor = self.vendor_repo.get_by_id(vendor_id)
        if not vendor:
            raise NotFoundError(f"Vendor with ID {vendor_id} not found")

        # If name is being updated, check for duplicates
        if vendor_data.name and vendor_data.name != vendor.name:
            existing_vendor = self.vendor_repo.get_by_name(vendor_data.name)
            if existing_vendor:
                raise ValidationError(f"Vendor with name '{vendor_data.name}' already exists")

        updated_vendor = self.vendor_repo.update(vendor, vendor_data)
        return VendorResponse.model_validate(updated_vendor).model_dump()

    def delete_vendor(self, vendor_id: int) -> None:
        """Delete a vendor."""
        vendor = self.vendor_repo.get_by_id(vendor_id)
        if not vendor:
            raise NotFoundError(f"Vendor with ID {vendor_id} not found")

        self.vendor_repo.delete(vendor)
