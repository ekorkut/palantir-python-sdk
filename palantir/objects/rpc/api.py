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

from typing import Optional, Dict, Any, List

from conjure_python_client import (
    Service,
    ConjureBeanType,
    ConjureDecoder,
    ConjureFieldDefinition,
    DictType,
    OptionalTypeWrapper
)


class Ontology(ConjureBeanType):
    @classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'description': ConjureFieldDefinition('description', str),
            'display_name': ConjureFieldDefinition('displayName', str),
            'rid': ConjureFieldDefinition('rid', str)
        }

    __slots__: List[str] = ["_description", "_displayName", "_rid"]

    def __init__(self, description: str, display_name: str, rid: str):
        self._description = description
        self._displayName = display_name
        self._rid = rid

    @property
    def description(self) -> str:
        return self._description

    @property
    def display_name(self) -> str:
        return self._displayName

    @property
    def rid(self) -> str:
        return self._rid


class ListOntologiesResponse(ConjureBeanType):
    @classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'data': ConjureFieldDefinition('data', List[Ontology])
        }

    __slots__: List[str] = ["_data"]

    def __init__(self, data: List[Ontology]):
        self._data = data

    @property
    def data(self) -> List[Ontology]:
        return self._data


class Property(ConjureBeanType):
    @classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'description': ConjureFieldDefinition('description', OptionalTypeWrapper[str]),
            'base_type': ConjureFieldDefinition('baseType', str)
        }

    __slots__: List[str] = ["_description", "_base_type"]

    def __init__(self, description: str, base_type: str):
        self._description = description
        self._base_type = base_type

    @property
    def description(self) -> str:
        return self._description

    @property
    def base_type(self) -> str:
        return self._base_type


class ObjectType(ConjureBeanType):
    @classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'api_name': ConjureFieldDefinition('apiName', str),
            'description': ConjureFieldDefinition('description', OptionalTypeWrapper[str]),
            'primary_key': ConjureFieldDefinition('primaryKey', OptionalTypeWrapper[List[str]]),
            'properties': ConjureFieldDefinition('properties', DictType(str, Property)),
            'rid': ConjureFieldDefinition('rid', str)
        }

    __slots__: List[str] = ["_api_name", "_description", "_primary_key", "_properties", "_rid"]

    def __init__(
            self, api_name: str, description: str, primary_key: List[str], properties: Dict[str, Property], rid: str
    ):
        self._api_name = api_name
        self._description = description
        self._primary_key = primary_key
        self._properties = properties
        self._rid = rid

    @property
    def api_name(self) -> str:
        return self._api_name

    @property
    def description(self) -> str:
        return self._description

    @property
    def primary_key(self) -> List[str]:
        return self._primary_key

    @property
    def properties(self) -> Dict[str, Property]:
        return self._properties

    @property
    def rid(self) -> str:
        return self._rid


class ListObjectTypesResponse(ConjureBeanType):
    @classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'data': ConjureFieldDefinition('data', List[ObjectType]),
            'next_page_token': ConjureFieldDefinition('nextPageToken', OptionalTypeWrapper[str])
        }

    __slots__: List[str] = ["_next_page_token", "_data"]

    def __init__(self, data: List[ObjectType], next_page_token: OptionalTypeWrapper[str]):
        self._data = data
        self._next_page_token = next_page_token

    @property
    def data(self) -> List[ObjectType]:
        return self._data

    @property
    def next_page_token(self) -> str:
        return self._next_page_token


class APIService(Service):
    def list_ontologies(
            self, auth_header: str,
    ) -> "Optional[ListOntologiesResponse]":
        _headers: Dict[str, Any] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": auth_header,
        }

        _params: Dict[str, Any] = {}

        _json: Any = None

        _path = "/ontologies"

        _response = self._request(
            "GET", self._uri + _path, params=_params, headers=_headers, json=_json
        )

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), ListOntologiesResponse)

    def list_object_types(
        self, auth_header: str, ontology_rid: str, page_token: str = None
    ) -> "Optional[ListObjectTypesResponse]":
        _headers: Dict[str, Any] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": auth_header,
        }

        _params: Dict[str, Any] = {
            "pageToken": page_token
        }
        _path_params: Dict[str, Any] = {
            "ontology_rid": ontology_rid
        }

        _json: Any = None

        _path = "/ontologies/{ontology_rid}/objectTypes"
        _path = _path.format(**_path_params)

        _response = self._request(
            "GET", self._uri + _path, params=_params, headers=_headers, json=_json
        )

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), ListObjectTypesResponse)

    def get_object_type(self, auth_header: str, ontology_rid: str, object_type: str):
        _headers: Dict[str, Any] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": auth_header,
        }

        _params: Dict[str, Any] = {}
        _path_params: Dict[str, Any] = {
            "ontology_rid": ontology_rid,
            "object_type": object_type
        }

        _json: Any = None

        _path = "/ontologies/{ontology_rid}/objectTypes/{object_type}"
        _path = _path.format(**_path_params)

        _response = self._request(
            "GET", self._uri + _path, params=_params, headers=_headers, json=_json
        )

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), ObjectType)

