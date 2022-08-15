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
    ConjureEncoder,
    ConjureDecoder,
    ConjureFieldDefinition
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

