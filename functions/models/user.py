from pydantic import BaseModel, Field, HttpUrl

# Define the fields
email_field = Field(
    title="Email",
    example="test@123.com",
    description="The email of the user.",
    regex="^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$",
)
username_field = Field(
    title="Username",
    max_length=255,
    example="testuser",
    description="The username of the user.",
)
full_name_field = Field(
    default=None,
    title="Full Name",
    example="Test User",
    description="The full name of the user.",
)
profile_picture_url_field = Field(
    default=None,
    title="Profile Picture URL",
    description="The URL of the user's profile picture.",
    example="https://api.multiavatar.com/Binx Bond.svg",
)
password_field = Field(
    title="Password",
    example="SomeStrongPassword123@",
    description="The password of the user.",
    min_length=8,
)
disabled_field = Field(
    default=False,
    title="Disabled",
    description="Whether the user is disabled.",
)
email_verified_field = Field(
    default=False,
    title="Email Verified",
    description="Whether the user's email is verified.",
)
hashed_password_field = Field(
    default=None,
    title="Hashed Password",
    description="The hashed password of the user as stored in the database.",
)
is_admin_field = Field(
    default=False,
    title="Is Admin",
    description="Whether the user is an admin.",
)

# Define the models


class PublicUser(BaseModel):
    username: str = username_field
    full_name: str | None = full_name_field
    profile_picture_url: HttpUrl | None = profile_picture_url_field


class NewUser(BaseModel):
    username: str = username_field
    full_name: str | None = full_name_field
    profile_picture_url: HttpUrl | None = profile_picture_url_field
    email: str = email_field
    password: str = password_field


class User(BaseModel):
    username: str = username_field
    full_name: str | None = full_name_field
    profile_picture_url: HttpUrl | None = profile_picture_url_field
    email: str = email_field
    disabled: bool = disabled_field
    email_verified: bool = email_verified_field
    is_admin: bool = is_admin_field


class UserInDB(BaseModel):
    username: str = username_field
    full_name: str | None = full_name_field
    profile_picture_url: HttpUrl | None = profile_picture_url_field
    email: str = email_field
    disabled: bool = disabled_field
    email_verified: bool = email_verified_field
    hashed_password: str | None = hashed_password_field
    is_admin: bool = is_admin_field
