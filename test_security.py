from security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token
)

# Test password hashing
hashed = hash_password("mypassword123")

print("Password verified:",
      verify_password("mypassword123", hashed))

# Generate JWT token
token = create_access_token(user_id=1)

print("JWT Token:", token)

# Verify JWT token
user_id = verify_access_token(token)

print("Authenticated User ID:", user_id)