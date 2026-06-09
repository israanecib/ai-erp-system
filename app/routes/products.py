"""
Product API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse, ProductStockUpdate
from app.services.product_service import ProductService
from app.auth.dependencies import get_current_user, get_current_admin
from app.models.user import User

router = APIRouter(
    prefix="/api/products",
    tags=["Products"],
)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_create: ProductCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new product (Admin only)"""
    try:
        product = ProductService.create_product(db, product_create)
        return ProductResponse.from_attributes(product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=ProductListResponse)
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category_id: int = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all products with pagination"""
    products, total = ProductService.get_all_products(db, skip=skip, limit=limit, category_id=category_id)
    
    return ProductListResponse(
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        items=[ProductResponse.from_attributes(p) for p in products]
    )


@router.get("/search", response_model=ProductListResponse)
async def search_products(
    q: str = Query(..., min_length=1, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search products by name or barcode"""
    products, total = ProductService.search_products(db, q, skip=skip, limit=limit)
    
    return ProductListResponse(
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        items=[ProductResponse.from_attributes(p) for p in products]
    )


@router.get("/low-stock", response_model=list)
async def get_low_stock_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get products below reorder level"""
    products = ProductService.get_low_stock_products(db)
    return [ProductResponse.from_attributes(p) for p in products]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific product by ID"""
    product = ProductService.get_product(db, product_id)
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    return ProductResponse.from_attributes(product)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update a product (Admin only)"""
    try:
        product = ProductService.update_product(db, product_id, product_update)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return ProductResponse.from_attributes(product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{product_id}/stock", response_model=ProductResponse)
async def update_product_stock(
    product_id: int,
    stock_update: ProductStockUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update product stock level"""
    try:
        current_product = ProductService.get_product(db, product_id)
        if not current_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        quantity_change = stock_update.quantity - current_product.quantity
        product = ProductService.update_stock(db, product_id, quantity_change, stock_update.reason)
        return ProductResponse.from_attributes(product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_product(
    product_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Deactivate a product (Admin only)"""
    try:
        ProductService.deactivate_product(db, product_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/stats/inventory", response_model=dict)
async def get_inventory_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get inventory statistics"""
    stats = ProductService.get_inventory_stats(db)
    return stats
