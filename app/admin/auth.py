# from fastapi import Request, Response, HTTPException
# from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
# from starlette_admin.exceptions import FormValidationError, LoginFailed
# from sqlalchemy.orm import Session
#
# from app.dependencies import get_db
# from app.models import User
# from app.utils import verify_password
#
#
# class JSONAuthProvider(AuthProvider):
#     async def login(
#             self,
#             email: str,
#             password: str,
#             remember_me: bool,
#             request: Request,
#             response: Response,
#     ):
#         db: Session = next(get_db())
#         current_requested_user = db.query(User).filter(User.email == email).first()
#
#         if not current_requested_user:
#             raise LoginFailed("User not found.")
#
#         if current_requested_user and current_requested_user.is_superuser != True:
#             raise LoginFailed("User is not admin.")
#
#         if not verify_password(password, current_requested_user.hashed_password):
#             raise LoginFailed("Invalid password.")
#
#         return