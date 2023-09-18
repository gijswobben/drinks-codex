from fastapi import HTTPException, status

unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
admin_required_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Admin privileges required",
    headers={"WWW-Authenticate": "Bearer"},
)

inactive_user_exception = HTTPException(status_code=400, detail="Inactive user")

beer_not_found_exception = HTTPException(status_code=404, detail="Beer not found")
beer_already_exists_exception = HTTPException(
    status_code=400, detail="Beer already exists"
)
