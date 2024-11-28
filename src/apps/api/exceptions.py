from fastapi import HTTPException, status

username_already_exists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Username already exists"
)

verification_code_incorrect = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Verification code is incorrect"
)

authentication_incorrect = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Username or password is incorrect"
)

permission_denied = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied"
)

user_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)