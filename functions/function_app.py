import os

from azure.functions import AsgiFunctionApp, AuthLevel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi_versioning import VersionedFastAPI
from routers import authentication, beers, users
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

# Create all the middleware for the app
session_middleware = Middleware(
    SessionMiddleware,
    secret_key=os.environ.get("SECRET_KEY", "secret"),
)
cors_middleware = Middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3400", "http://localhost:7071"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
middleware: list[Middleware] = [session_middleware, cors_middleware]

# Create the app
fastapi_app = FastAPI(
    title="FastAPI Azure Functions",
    description="This is a sample FastAPI app for Azure Functions.",
    version="0.1.0",
    middleware=middleware,
)


@fastapi_app.get("/", include_in_schema=False)
async def docs_redirect() -> RedirectResponse:
    """Redirect root to FastAPI docs page."""
    return RedirectResponse(url="/docs")


# Add the routers
fastapi_app.include_router(authentication.router, prefix="/api")
fastapi_app.include_router(users.router, prefix="/api")
fastapi_app.include_router(beers.router, prefix="/api")

# Define the app
app = AsgiFunctionApp(
    app=VersionedFastAPI(
        fastapi_app,
        enable_latest=True,
        version_format="v{major}",
        prefix_format="/v{major}",
        middleware=middleware,  # NOTE: Redefine the middleware here
    ),
    http_auth_level=AuthLevel.ANONYMOUS,
)
