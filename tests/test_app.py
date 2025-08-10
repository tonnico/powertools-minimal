import json
from http import HTTPStatus

import pytest
from inline_snapshot import snapshot

from minimal_powertools import app as sut


class TestQueryModelSimple:
    def test_query_model_simple(self, gw_event):
        gw_event["path"] = "/query-model-simple"
        gw_event["multiValueQueryStringParameters"] = {
            "full_name": ["Nico123"],
            "next_token": ["bmV4dF90b2tlbg=="],
            "search_id": ["search_id_value"],
        }
        response = sut.app(gw_event, {})
        assert response == snapshot(
            {
                "statusCode": HTTPStatus.OK,
                "body": '{"fullName":"Nico123","nextToken":"next_token"}',
                "isBase64Encoded": False,
                "multiValueHeaders": {"Content-Type": ["application/json"]},
            }
        )

class TestQueryModelAdvanced:
    def test_query_model_advanced__success_expected(self, gw_event):
        gw_event["path"] = "/query-model-advanced"
        gw_event["multiValueQueryStringParameters"] = {
            "fullName": ["Nico123"],
            "nextToken": ["bmV4dF90b2tlbg=="],
            "id": ["550e8400-e29b-41d4-a716-446655440000"],
        }
        response = sut.app(gw_event, {})
        assert response == snapshot(
            {
                "statusCode": HTTPStatus.OK,
                "body": '{"fullName":"Nico123","nextToken":"bmV4dF90b2tlbg==","id":"550e8400-e29b-41d4-a716-446655440000","attr":[]}',
                "isBase64Encoded": False,
                "multiValueHeaders": {"Content-Type": ["application/json"]},
            }
        )

    @pytest.mark.xfail(reason="This should work with validate_by_name=True")
    def test_query_model_advanced__fail_expected(self, gw_event):
        gw_event["path"] = "/query-model-advanced"
        gw_event["multiValueQueryStringParameters"] = {
            "full_name": ["Nico123"],
            "next_token": ["bmV4dF90b2tlbg=="],
            "search_id": ["550e8400-e29b-41d4-a716-446655440000"],
        }
        response = sut.app(gw_event, {})
        assert response == snapshot(
            {
                "statusCode": HTTPStatus.OK,
                "body": '{"fullName":"Nico123","nextToken":"bmV4dF90b2tlbg==","id":"550e8400-e29b-41d4-a716-446655440000"}',
                "isBase64Encoded": False,
                "multiValueHeaders": {"Content-Type": ["application/json"]},
            }
        )

    @pytest.mark.xfail(reason="multiValueQueryStringParameters lists should be handled")
    def test_lists_can_be_parsed(self, gw_event):
        gw_event["path"] = "/query-model-advanced"
        gw_event["multiValueQueryStringParameters"] = {
            "fullName": ["Nico123"],
            "nextToken": ["bmV4dF90b2tlbg=="],
            "id": ["550e8400-e29b-41d4-a716-446655440000"],
            "attr": ["a", "b", "c"],
        }
        response = sut.app(gw_event, {})
        assert response == {}
        body = json.loads(response["body"])
        assert "attr" in body
        assert body["attr"] == ["a", "b", "c"]


class TestQuery:
    def test_query_model_simple(self, gw_event):
        gw_event["path"] = "/query"
        gw_event["multiValueQueryStringParameters"] = {
            "fullName": ["Nico123"],
            "nextToken": ["bmV4dF90b2tlbg=="],
            "id": ["550e8400-e29b-41d4-a716-446655440000"],
            "attr": ["a", "b", "c"],
        }
        response = sut.app(gw_event, {})
        assert response == snapshot(
            {
                "statusCode": HTTPStatus.OK,
                "body": '{"fullName":"Nico123","nextToken":"next_token","id":"550e8400-e29b-41d4-a716-446655440000","attr":["a","b","c"]}',
                "isBase64Encoded": False,
                "multiValueHeaders": {"Content-Type": ["application/json"]},
            }
        )


class TestModel:
    def test_query_model_simple(self):
        input = {
            "full_name": "Nico123",
            "next_token": "bmV4dF90b2tlbg==",
            "search_id": "search_id_value",
        }

        model = sut.QuerySimple.model_validate(input)

        assert model.model_dump() == snapshot(
            {
                "full_name": "Nico123",
                "next_token": "bmV4dF90b2tlbg==",
                "search_id": "search_id_value",
                "attr": [],
            }
        )

    def test_query_model_advanced_alias(self):
        input = {
            "fullName": "Nico123",
            "nextToken": "bmV4dF90b2tlbg==",
            "id": "550e8400-e29b-41d4-a716-446655440000",
        }

        model = sut.QueryAdvanced.model_validate(input)

        assert model.model_dump(mode="json") == snapshot(
            {
                "fullName": "Nico123",
                "nextToken": "bmV4dF90b2tlbg==",
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "attr": [],
            }
        )

    def test_query_model_advanced_name(self):
        input = {
            "full_name": "Nico123",
            "next_token": "bmV4dF90b2tlbg==",
            "search_id": "550e8400-e29b-41d4-a716-446655440000",
        }

        model = sut.QueryAdvanced.model_validate(input, by_name=True)

        assert model.model_dump(mode="json") == snapshot(
            {
                "fullName": "Nico123",
                "nextToken": "bmV4dF90b2tlbg==",
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "attr": [],
            }
        )
