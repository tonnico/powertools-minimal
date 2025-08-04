from http import HTTPStatus
from minimal_powertools import app as sut

import pytest
class TestApp:
    def test_query_model_simple(self, gw_event):
        gw_event["path"] = "/query-model-simple"
        gw_event["multiValueQueryStringParameters"] = {
            "full_name": ["Nico123"],
            "next_token": ["bmV4dF90b2tlbg=="],
            "search_id": ["search_id_value"],
        }
        response = sut.app(gw_event, {})
        assert response == {
            "statusCode": HTTPStatus.OK,
            "body": '{"fullName":"Nico123","nextToken":"next_token"}',
            "isBase64Encoded": False,
            "multiValueHeaders": {"Content-Type": ["application/json"]},
        }

    @pytest.mark.xfail(reason="This should work when valiadate_by_alias=True, but will only pass with validate_by_name=True")
    def test_query_model_advanced__success_expected(self, gw_event):
        gw_event["path"] = "/query-model-advanced"
        gw_event["multiValueQueryStringParameters"] = {
            "fullName": ["Nico123"],
            "nextToken": ["bmV4dF90b2tlbg=="],
            "id": ["550e8400-e29b-41d4-a716-446655440000"],
        }
        response = sut.app(gw_event, {})
        assert response == {
            "statusCode": HTTPStatus.OK,
            "body": '{"fullName":"Nico123","nextToken":"bmV4dF90b2tlbg==","id":"550e8400-e29b-41d4-a716-446655440000"}',
            "isBase64Encoded": False,
            "multiValueHeaders": {"Content-Type": ["application/json"]},
        }

    @pytest.mark.xfail(reason="This should work when valiadate_by_name=True")
    def test_query_model_advanced__fail_expected(self, gw_event):
        gw_event["path"] = "/query-model-advanced"
        gw_event["multiValueQueryStringParameters"] = {
            "full_name": ["Nico123"],
            "next_token": ["bmV4dF90b2tlbg=="],
            "search_id": ["550e8400-e29b-41d4-a716-446655440000"],
        }
        response = sut.app(gw_event, {})
        assert response == {
            "statusCode": HTTPStatus.OK,
            "body": '{"fullName":"Nico123","nextToken":"bmV4dF90b2tlbg==","id":"550e8400-e29b-41d4-a716-446655440000"}',
            "isBase64Encoded": False,
            "multiValueHeaders": {"Content-Type": ["application/json"]},
        }


class TestModel:
    def test_query_model_simple(self):
        input = {
            "full_name": "Nico123",
            "next_token": "bmV4dF90b2tlbg==",
            "search_id": "search_id_value",
        }

        model = sut.QuerySimple.model_validate(input)

        assert model.model_dump() == {
            "full_name": "Nico123",
            "next_token": "bmV4dF90b2tlbg==",
            "search_id": "search_id_value",
        }

    def test_query_model_advanced_alias(self):
        input = {
            "fullName": "Nico123",
            "nextToken": "bmV4dF90b2tlbg==",
            "id": "550e8400-e29b-41d4-a716-446655440000",
        }

        model = sut.QueryAdvanced.model_validate(input)

        assert model.model_dump(mode="json") == {
            "fullName": "Nico123",
            "nextToken": "bmV4dF90b2tlbg==",
            "id": "550e8400-e29b-41d4-a716-446655440000",
        }

    def test_query_model_advanced_name(self):
        input = {
            "full_name": "Nico123",
            "next_token": "bmV4dF90b2tlbg==",
            "search_id": "550e8400-e29b-41d4-a716-446655440000",
        }

        model = sut.QueryAdvanced.model_validate(input, by_name=True)

        assert model.model_dump(mode="json") == {
            "fullName": "Nico123",
            "nextToken": "bmV4dF90b2tlbg==",
            "id": "550e8400-e29b-41d4-a716-446655440000",
        }
