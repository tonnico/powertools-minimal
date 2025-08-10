from typing import Annotated, Any

from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.openapi.params import Query
from pydantic import (
    UUID4,
    AfterValidator,
    Base64UrlStr,
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    alias_generators,
)

app = APIGatewayRestResolver(enable_validation=True)

def _validate_nico(value: str) -> str:
    if not value.startswith("Nico"):
        raise ValueError("Full name must start with 'Nico'")
    return value

class QuerySimple(BaseModel):
    full_name: Annotated[str, StringConstraints(min_length=5), AfterValidator(_validate_nico)]
    next_token: Base64UrlStr
    search_id: str
    attr: list[str] = []



@app.get("/query-model-simple")
def query_model(
    params: Annotated[QuerySimple, Query()],
) -> dict[str, Any]:
    return {
        "fullName": params.full_name,
        "nextToken": params.next_token,
    }


class QueryAdvanced(BaseModel):
    full_name: Annotated[str, StringConstraints(min_length=5), AfterValidator(_validate_nico)]
    next_token: Base64UrlStr
    search_id: Annotated[UUID4, Field(alias="id")]
    attr: Annotated[list[str], Field(max_length=3)] = []

    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel,
        validate_by_alias=True,  # by_alias is not working
        serialize_by_alias= True,
        validate_by_name=True,
    )

@app.get("/query-model-advanced")
def query_model_advanced(
    params: Annotated[QueryAdvanced, Query()],
) -> dict[str, Any]:
    return params.model_dump()


@app.get("/query")
def query(
    full_name: Annotated[str, StringConstraints(min_length=5), AfterValidator(_validate_nico), Query(alias="fullName")],
    next_token: Annotated[Base64UrlStr, Query(alias="nextToken")],
    search_id: Annotated[UUID4, Query(alias="id")],
    attr: Annotated[list[str], Query(max_length=3)] = [],
)-> dict[str, Any]:
    return {
        "fullName": full_name,
        "nextToken": next_token,
        "id": search_id,
        "attr": attr,
    }