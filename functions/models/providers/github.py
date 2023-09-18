from pydantic import BaseModel, HttpUrl


class GithubEmailData(BaseModel):
    email: str
    primary: bool
    verified: bool
    visibility: str


class GithubUserData(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: HttpUrl | None
    gravatar_id: str
    url: str
    name: str
    email_addresses: list[GithubEmailData]

    @property
    def primary_email(self) -> GithubEmailData:
        return next(
            email for email in self.email_addresses if email.primary and email.verified
        )
