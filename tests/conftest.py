from typing import Any
import pytest


@pytest.fixture
def gw_event() -> dict[str, Any]:
    return {
        "version": "1.0",
        "resource": "/my/path",
        "path": "/my/path",
        "httpMethod": "GET",
        "headers": {
            "Header1": "value1",
            "Header2": "value2",
            "Origin": "https://aws.amazon.com",
        },
        "multiValueHeaders": {
            "Header1": ["value1"],
            "Origin": ["https://aws.amazon.com"],
            "Header2": ["value1", "value2"],
        },
        "queryStringParameters": {"parameter1": "value1", "parameter2": "value"},
        "multiValueQueryStringParameters": {
            "parameter1": ["value1", "value2"],
            "parameter2": ["value"],
        },
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "id",
            "authorizer": {"claims": None, "scopes": None},
            "domainName": "id.execute-api.us-east-1.amazonaws.com",
            "domainPrefix": "id",
            "extendedRequestId": "request-id",
            "httpMethod": "GET",
            "identity": {
                "accessKey": None,
                "accountId": None,
                "caller": None,
                "cognitoAuthenticationProvider": None,
                "cognitoAuthenticationType": None,
                "cognitoIdentityId": None,
                "cognitoIdentityPoolId": None,
                "principalOrgId": None,
                "sourceIp": "192.168.0.1/32",
                "user": None,
                "userAgent": "user-agent",
                "userArn": None,
                "clientCert": {
                    "clientCertPem": "CERT_CONTENT",
                    "subjectDN": "www.example.com",
                    "issuerDN": "Example issuer",
                    "serialNumber": "a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1",
                    "validity": {
                        "notBefore": "May 28 12:30:02 2019 GMT",
                        "notAfter": "Aug  5 09:36:04 2021 GMT",
                    },
                },
            },
            "path": "/my/path",
            "protocol": "HTTP/1.1",
            "requestId": "id=",
            "requestTime": "04/Mar/2020:19:15:17 +0000",
            "requestTimeEpoch": 1583349317135,
            "resourceId": None,
            "resourcePath": "/my/path",
            "stage": "$default",
        },
        "pathParameters": None,
        "stageVariables": None,
        "body": "Hello from Lambda!",
        "isBase64Encoded": False,
    }
