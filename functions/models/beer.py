from pydantic import BaseModel, Field

uuid_field = Field(title="Beer UUID", description="The UUID of the beer.")
name_field = Field(title="Beer Name", description="The name of the beer.")
brewery_uuid_field = Field(title="Brewery UUID", description="The UUID of the brewery.")
abv_field = Field(title="ABV", description="The ABV of the beer.")


class Beer(BaseModel):
    uuid: str = uuid_field
    name: str = name_field
    brewery_uuid: str = brewery_uuid_field
    abv: float = abv_field


class NewBeer(BaseModel):
    name: str = name_field
    brewery_uuid: str = brewery_uuid_field
    abv: float = abv_field
