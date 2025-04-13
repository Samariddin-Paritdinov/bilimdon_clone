from fastapi import APIRouter, HTTPException, Response


from app.schemas.auth import *
from app.models import User
from app.utils import hash_password, verify_password, create_access_token, REFRESH_TOKEN_EXPIRE_MINUTES
from app.dependencies import db_dep


router = APIRouter(
    prefix="/authentication", 
    tags=["authentication"],
)


@router.post('/registration', response_model=AuthRegistrationResponse)
async def registration(
    db: db_dep, 
    user: AuthRegistration
):
    is_first_user = db.query(User).count() == 0

    is_user_exists = db.query(User).filter(User.email == user.email).first()
    if is_user_exists:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists."
        )
    
    db_user = User(
        email = user.email,
        hashed_password = hash_password(user.password),
        username = user.email.split("@")[0],
        is_active = True,
        is_staff = is_first_user,
        is_superuser = is_first_user
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user



@router.post('/login')
async def login(
        db: db_dep, 
        user: AuthLogin
    ):
    db_user = db.query(User).filter(User.email == user.email).first()
    is_correct = verify_password(user.password, db_user.hashed_password) if db_user else False

    if not db_user or not is_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid password or username."
        )


    user_dict = user.model_dump()
    
    access_token = create_access_token(user_dict)
    refresh_token = create_access_token(user_dict, REFRESH_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }