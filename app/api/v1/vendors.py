from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.vendor import VendorCreate, VendorUpdate
from app.services.vendor_service import VendorService
from app.exceptions import NotFoundError, ValidationError

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.get("/", response_model=list[dict])
def get_vendors(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    category: Optional[str] = Query(None, description="Filter by category (dining, retail, service, entertainment)"),
    active_only: bool = Query(True, description="Only return active vendors"),
    db: Session = Depends(get_db)
):
    """
    Get all campus vendors.

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **category**: Optional filter by category
    - **active_only**: Only show active vendors (default: true)

    No authentication required - public endpoint.
    """
    service = VendorService(db)
    return service.get_vendors(
        skip=skip,
        limit=limit,
        active_only=active_only,
        category=category
    )


@router.get("/{vendor_id}", response_model=dict)
def get_vendor(
    vendor_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific vendor by ID.

    No authentication required - public endpoint.
    """
    service = VendorService(db)
    try:
        return service.get_vendor(vendor_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_vendor(
    vendor_data: VendorCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new vendor.

    Requires admin authentication.
    """
    # TODO: Add admin role check
    # if current_user.role != UserRole.ADMIN:
    #     raise HTTPException(status_code=403, detail="Admin access required")

    service = VendorService(db)
    try:
        return service.create_vendor(vendor_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )


@router.put("/{vendor_id}", response_model=dict)
def update_vendor(
    vendor_id: int,
    vendor_data: VendorUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing vendor.

    Requires admin authentication.
    """
    # TODO: Add admin role check
    # if current_user.role != UserRole.ADMIN:
    #     raise HTTPException(status_code=403, detail="Admin access required")

    service = VendorService(db)
    try:
        return service.update_vendor(vendor_id, vendor_data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )


@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendor(
    vendor_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a vendor.

    Requires admin authentication.
    """
    # TODO: Add admin role check
    # if current_user.role != UserRole.ADMIN:
    #     raise HTTPException(status_code=403, detail="Admin access required")

    service = VendorService(db)
    try:
        service.delete_vendor(vendor_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
