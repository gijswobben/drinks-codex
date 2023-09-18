from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(
        title="Access Token",
        description="The access token.",
    )
    token_type: str = Field(
        title="Token Type",
        description="The type of token.",
    )


class TokenData(BaseModel):
    username: str = Field(
        title="Username",
        description="The username.",
    )
