#  (c) Copyright 2022 Palantir Technologies Inc. All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pytest
from mockito import mock, when
from expects import expect, equal
from unittest.mock import patch, MagicMock

from palantir.objects.rpc.api import (
    APIService, ListOntologiesResponse, Ontology, ListObjectTypesResponse, ObjectType, Property
)
from palantir.objects.client import ObjectServices

from palantir.core.rpc import ConjureClient
from palantir.core.types import PalantirContext, ResourceIdentifier
from palantir.core.config import StaticTokenProvider, StaticHostnameProvider, AuthToken, StaticOntologyRidProvider


class TestRPC:
    AUTH_HEADER: str = "auth-header"

    @pytest.fixture(autouse=True)
    def before(self):
        self.api_root = f"https://somehost/api/v1"
        self.ontology_rid = "ri.ontology.main.ontology.1"
        self.ontology_display_name = "My ontology"
        self.ontology_desc = "My ontology desc"

    def test_list_ontologies(self):
        with patch('conjure_python_client.Service._request') as mocked_request:
            service = ConjureClient().service(
                APIService,
                self.api_root,
            )
            mocked_response = MagicMock()
            mocked_request.return_value = mocked_response
            mocked_response.json.return_value = {
                'data': [
                    {
                        'displayName': self.ontology_display_name,
                        "description": self.ontology_desc,
                        "rid": self.ontology_rid
                    }
                ]
            }

            output = service.list_ontologies(auth_header=self.AUTH_HEADER)
            # Verify the request
            mocked_request.assert_called()
            assert len(mocked_request.call_args.args) == 2
            assert mocked_request.call_args.args[0] == "GET"
            assert mocked_request.call_args.args[1] == self.api_root + "/ontologies"
            assert len(mocked_request.call_args.kwargs) == 3
            assert mocked_request.call_args.kwargs["params"] == {}
            assert mocked_request.call_args.kwargs["headers"]["Authorization"] == self.AUTH_HEADER
            assert mocked_request.call_args.kwargs["json"] is None

            # Verify the output
            assert len(output.data) == 1
            assert output.data[0].description == self.ontology_desc
            assert output.data[0].display_name == self.ontology_display_name
            assert output.data[0].rid == self.ontology_rid

    def test_list_object_types(self):
        with patch('conjure_python_client.Service._request') as mocked_request:
            service = ConjureClient().service(
                APIService,
                self.api_root,
            )
            mocked_response = MagicMock()
            mocked_request.return_value = mocked_response
            mocked_response.json.return_value = {
                'data': [
                    {
                        'apiName': "ObjectType1",
                        "description": "ObjectType1Desc",
                        "rid": "ri.ontology.main.object-type.1",
                        "primaryKey": ["o1pk1", "o1pk2"],
                        "properties": {
                            'o1prop1': {'description': "", "baseType": 'Timestamp'},
                            'o1prop2': {'description': "", "baseType": 'String'},
                        }
                    },
                    {
                        'apiName': "ObjectType2",
                        "description": "ObjectType2Desc",
                        "rid": "ri.ontology.main.object-type.2",
                        "primaryKey": ["o2pk1"],
                        "properties": {
                            'o2prop1': {'description': "", "baseType": 'Timestamp'},
                            'o2prop2': {'description': "", "baseType": 'String'},
                        }
                    },
                ]
            }

            output = service.list_object_types(auth_header=self.AUTH_HEADER, ontology_rid=self.ontology_rid)

            # Verify the request
            mocked_request.assert_called()
            assert len(mocked_request.call_args.args) == 2
            assert mocked_request.call_args.args[0] == "GET"
            assert mocked_request.call_args.args[1] == self.api_root + f"/ontologies/{self.ontology_rid}/objectTypes"
            assert len(mocked_request.call_args.kwargs) == 3
            assert mocked_request.call_args.kwargs["params"]["pageToken"] is None
            assert mocked_request.call_args.kwargs["headers"]["Authorization"] == self.AUTH_HEADER
            assert mocked_request.call_args.kwargs["json"] is None

            # Verify the output
            assert len(output.data) == 2
            assert output.data[0].api_name == "ObjectType1"
            assert output.data[0].description == "ObjectType1Desc"
            assert output.data[0].primary_key == ["o1pk1", "o1pk2"]
            assert output.data[0].rid == "ri.ontology.main.object-type.1"
            assert len(output.data[0].properties) == 2
            assert output.data[0].properties["o1prop1"].description == ""
            assert output.data[0].properties["o1prop1"].base_type == "Timestamp"
            assert output.data[0].properties["o1prop2"].description == ""
            assert output.data[0].properties["o1prop2"].base_type == "String"

            assert output.data[1].api_name == "ObjectType2"
            assert output.data[1].description == "ObjectType2Desc"
            assert output.data[1].primary_key == ["o2pk1"]
            assert output.data[1].rid == "ri.ontology.main.object-type.2"
            assert len(output.data[1].properties) == 2
            assert output.data[1].properties["o2prop1"].description == ""
            assert output.data[1].properties["o2prop1"].base_type == "Timestamp"
            assert output.data[1].properties["o2prop2"].description == ""
            assert output.data[1].properties["o2prop2"].base_type == "String"


