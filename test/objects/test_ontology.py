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
from mockito import mock, when, verify
from expects import expect, equal

from palantir.core.types import ResourceIdentifier
from palantir.objects.core import Ontology, ObjectType
from palantir.objects.client import ObjectsClient


class TestOntology:

    @pytest.fixture(autouse=True)
    def before(self):
        self.client = mock(ObjectsClient)
        self.ontology_rid = "ri.ontology.main.ontology.1"
        self.ontology = Ontology(
            rid=ResourceIdentifier.try_parse(self.ontology_rid),
            description="Ontology 1 description",
            display_name="Ontology 1 display",
            client=self.client
        )

    def test_list_object_types(self):
        object_type1 = ObjectType(
            api_name="ObjectType1",
            description="Object Type 1 description",
            primary_key=["type_one_primary_key"],
            properties={
                "type1_prop1": {
                    "description": None,
                    "base_type": "String"
                },
                "type1_prop2": {
                    "description": '',
                    "base_type": 'Array<String>'
                }
            },
            rid=ResourceIdentifier.try_parse("ri.ontology.main.object-type.1")
        )
        object_type2 = ObjectType(
            api_name="ObjectType2",
            description="Object Type 2 description",
            primary_key=["type_two_primary_key"],
            properties={
                "type2_prop1": {
                    "description": 'some description',
                    "base_type": "String"
                },
                "type2_prop2": {
                    "description": 'some other description',
                    "base_type": 'Array<String>'
                }
            },
            rid=ResourceIdentifier.try_parse("ri.ontology.main.object-type.2")
        )

        def gen():
            yield object_type1
            yield object_type2

        when(self.client).list_object_types(self.ontology_rid).thenReturn(gen())

        expect(list(self.ontology.list_object_types())).to(equal([object_type1, object_type2]))

    def test_object_type(self):
        pass
