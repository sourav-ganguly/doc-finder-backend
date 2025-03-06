from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db

from . import schemas, service

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register", response_model=schemas.User, status_code=201)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    - **email**: Valid email address (must be unique)
    - **username**: Unique username
    - **password**: Password for authentication
    """
    return service.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    
    - **username**: Email address used for authentication
    - **password**: Password for authentication
    """
    user = service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/test-linter-errors")
def test_linter_errors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    An API endpoint with intentional linter errors for testing purposes.
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    # Unused import (linter error)
    
    # Undefined variable (linter error)
    result = undefined_variable + 10
    
    # Unused variable (linter error)
    unused_var = "This variable is never used"
    
    # Missing whitespace around operator (linter error)
    x=10+20
    
    # Line too long (linter error)
    very_long_string = "This is an extremely long string that will definitely exceed the recommended line length limit for Python code according to PEP 8 style guidelines and should trigger a linter warning"
    
    # Multiple statements on one line (linter error)
    a = 1; b = 2; c = 3
    
    # Comparison to None with == (linter error)
    if x == None:
        pass
        
    # Mutable default argument (linter error)
    def function_with_mutable_default(arg=[]):
        return arg
    
    # Inconsistent indentation (linter error - but fixing the syntax error)
    if True:
        y = 1
        z = 2  # Fixed indentation to avoid syntax error
    
    # Trailing whitespace (linter error)
    trailing_space = "This line has trailing spaces"    
    
    # Return statement with unnecessary parentheses (linter error)
    return ({"message": "Test endpoint with linter errors", "data": []}) 