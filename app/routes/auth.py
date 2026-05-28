"""
Authentication API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import (
    UserCreate, 
    UserLogin, 
    TokenResponse, 
    UserResponse,
    TokenRefresh,
    ChangePassword
)
from app.services.auth_service import AuthService
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.auth.jwt_handler import create_access_token, verify_token, create_refresh_token

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    db: Session = Depends(get_db)
) -> dict:
    """
    Register a new user account
    
    **Request Body:**
    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **full_name**: User's full name
    - **password**: Strong password (minimum 8 characters)
    
    **Returns:**
    - **access_token**: JWT token for accessing protected endpoints
    - **refresh_token**: Token for refreshing access token
    - **user**: User information
    """
    try:
        result = AuthService.register_user(db, user_create)
        
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            user=UserResponse.from_attributes(result["user"])
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user account"
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    user_login: UserLogin,
    db: Session = Depends(get_db)
) -> dict:
    """
    User login endpoint
    
    **Request Body:**
    - **username**: User's username
    - **password**: User's password
    
    **Returns:**
    - **access_token**: JWT token for accessing protected endpoints
    - **refresh_token**: Token for refreshing access token
    - **user**: User information
    """
    try:
        result = AuthService.login_user(db, user_login)
        
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            user=UserResponse.from_attributes(result["user"])
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during login"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current authenticated user information
    
    **Returns:**
    - **id**: User ID
    - **username**: Username
    - **email**: Email address
    - **full_name**: User's full name
    - **role**: User's role (admin, accountant, employee)
    - **is_active**: Account status
    - **created_at**: Account creation date
    - **last_login**: Last login timestamp
    
    **Security:** Requires valid JWT token in Authorization header
    """
    return current_user


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    token_refresh: TokenRefresh,
    db: Session = Depends(get_db)
) -> dict:
    """
    Refresh access token using refresh token
    
    **Request Body:**
    - **refresh_token**: Valid refresh token
    
    **Returns:**
    - **access_token**: New JWT access token
    - **refresh_token**: New refresh token
    - **user**: User information
    """
    # Verify refresh token
    payload = verify_token(token_refresh.refresh_token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Get user ID from token
    try:
        user_id = int(payload.get("sub"))
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )
    
    # Get user from database
    user = AuthService.get_user_by_id(db, user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token_new = create_refresh_token(data={"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_new,
        user=UserResponse.from_attributes(user)
    )


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Change user password
    
    **Request Body:**
    - **old_password**: Current password
    - **new_password**: New password (minimum 8 characters)
    - **confirm_password**: Confirm new password (must match new_password)
    
    **Returns:**
    - **message**: Success message
    
    **Security:** Requires valid JWT token in Authorization header
    """
    # Validate passwords match
    if not password_data.validate_passwords_match():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirmation do not match"
        )
    
    try:
        AuthService.change_password(
            db,
            current_user.id,
            password_data.old_password,
            password_data.new_password
        )
        
        return {"message": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error changing password"
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Logout user (client-side token removal)
    
    **Note:** JWT tokens cannot be revoked server-side. This endpoint
    is for logging the logout action. Clients should delete the token
    from local storage/cookies.
    
    **Returns:**
    - **message**: Logout success message
    
    **Security:** Requires valid JWT token in Authorization header
    """
    return {"message": f"User {current_user.username} logged out successfully"}
