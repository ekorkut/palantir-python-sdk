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

from typing import Generator, List, Dict

from palantir.core.types import ResourceIdentifier, PalantirContext
from palantir.objects import OrderTerm, PropertyFilter


class Ontology:

    def __init__(self, rid: ResourceIdentifier, description: str, display_name: str, client: "ObjectClient"):
        self._rid = rid
        self._description = description
        self._display_name = display_name
        self.client = client

    @property
    def rid(self) -> str:
        return str(self._rid)

    @property
    def description(self) -> str:
        return self._description

    @property
    def display_name(self) -> str:
        return self._display_name

    def list_object_types(self) -> Generator["ObjectType", None, None]:
        """
        Lists the object types in the ontology

        Args:
            path: An optional path prefix to use to filter when listing files.

        Returns: A generator over pages of :class:`ObjectType` objects in the current ontology
        """
        return self.client.list_object_types(str(self.rid))

    def object_type(self, api_name: str) -> "ObjectType":
        """
        Get the object type specified by api_name argument in the current ontology

        Args:
            api_name: The API name of the object type

        Returns: An :class:`ObjectType` object representing the object type
        """
        return self.client

    def __eq__(self, other) -> bool:
        return other is self or (
                isinstance(other, Ontology)
                and other.rid == self.rid
                and other.description == self.description
                and other.display_name == self.display_name
        )

    def __str__(self):
        return f'Ontology(rid="{self.rid}", description="{self.description}", display_name="{self.display_name}")'

    def __repr__(self):
        return str(self)


class ObjectType:

    def __init__(
            self, api_name: str, description: str, primary_key: List[str], properties: Dict, rid: ResourceIdentifier
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
    def properties(self) -> Dict:
        return self._properties

    @property
    def rid(self) -> str:
        return str(self._rid)

    def list_objects(
            self,
            properties: List[str] = None,
            order_by: List[tuple[str, OrderTerm]] = None,
            filters: List[PropertyFilter] = None
    ):
        pass

    def query(self, query_string: str):
        pass

    def search(self, json_string: str):
        pass

    def object(self, primary_key: str):
        pass

    def __str__(self):
        return f'ObjectType(api_name="{self.api_name}", primary_key="{self.primary_key}", rid="{self.rid}")'

    def __repr__(self):
        return str(self)

    def __eq__(self, other) -> bool:
        return other is self or (
                isinstance(other, ObjectType)
                and other.rid == self.rid
                and other.api_name == self.api_name
                and other.primary_key == self.primary_key
                and other.description == self.description
                and other.properties == self.properties
        )


class Object:

    def __init__(self, rid: ResourceIdentifier, properties: Dict):
        self._rid = rid
        self._properties = properties

    @property
    def rid(self) -> str:
        return str(self._rid)

    @property
    def properties(self) -> Dict:
        return self._properties

    def list_linked_objects(
        self,
        link_type: str,
        properties: List[str] = None,
        order_by: List[tuple[str, OrderTerm]] = None,
        filters: List[PropertyFilter] = None
    ):
        pass

    def linked_object(self, link_type: str, primary_key: str):
        pass