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

from palantir.objects.client import ObjectsClient, ObjectServices
from palantir.objects.rpc.api import (
    APIService, ListOntologiesResponse, Ontology, ListObjectTypesResponse, ObjectType, Property
)
from palantir.objects.core import (
    Ontology as FinalOntology,
    ObjectType as FinalObjectType
)

from palantir.core.types import PalantirContext, ResourceIdentifier
from palantir.core.config import StaticTokenProvider, StaticHostnameProvider, AuthToken


class TestClient:

    AUTH_HEADER: str = "auth-header"

    @pytest.fixture(autouse=True)
    def before(self):
        self.api_service = mock(APIService)
        services = mock(ObjectServices)
        services.api_service = self.api_service
        ctx: PalantirContext = PalantirContext(
            StaticHostnameProvider("unused"),
            StaticTokenProvider(AuthToken(self.AUTH_HEADER)),
        )
        services.ctx = ctx
        self.client = ObjectsClient(services)
        self.rid1, self.desc1, self.disp1 = "ri.ontology.main.ontology.1", "First ontology description", "First ontology display"
        self.rid2, self.desc2, self.disp2 = "ri.ontology.main.ontology.2", "Second ontology description", "Second ontology display"

    def test_list_ontologies(self):

        when(self.api_service).list_ontologies(
            auth_header=self.AUTH_HEADER
        ).thenReturn(ListOntologiesResponse(
            data=[
                Ontology(description=self.desc1, display_name=self.disp1, rid=self.rid1),
                Ontology(description=self.desc2, display_name=self.disp2, rid=self.rid2)
            ]
        ))
        expected_ontologies = [
            FinalOntology(
                rid=ResourceIdentifier.try_parse(self.rid1),
                description=self.desc1,
                display_name=self.disp1,
                client=None
            ),
            FinalOntology(
                rid=ResourceIdentifier.try_parse(self.rid2),
                description=self.desc2,
                display_name=self.disp2,
                client=None
            )
        ]
        expect(self.client.list_ontologies()).to(
            equal(expected_ontologies)
        )

    def test_list_object_types(self):
        obj1_api_name, obj1_desc, obj1_pk = "ObjectType1", "ObjectType1 description", "ObjectType1PK"
        obj1_propname, obj1_propdesc, obj1_propbase = 'ObjectType1Prop1', "", 'String'
        obj1_rid = "ri.ontology.main.object-type.1"

        obj2_api_name, obj2_desc, obj2_pk = "ObjectType2", "ObjectType2 description", "ObjectType2PK"
        obj2_propname, obj2_propdesc, obj2_propbase = 'ObjectType2Prop1', "", 'String'
        obj2_rid = "ri.ontology.main.object-type.2"

        obj1 = ObjectType(
            api_name=obj1_api_name,
            description=obj1_desc,
            primary_key=obj1_pk,
            properties={obj1_propname: Property(description=obj1_propdesc, base_type=obj1_propbase)},
            rid=obj1_rid
        )
        obj2 = ObjectType(
            api_name=obj2_api_name,
            description=obj2_desc,
            primary_key=obj2_pk,
            properties={obj2_propname: Property(description=obj2_propdesc, base_type=obj2_propbase)},
            rid=obj2_rid
        )

        when(self.api_service).list_object_types(
            auth_header=self.AUTH_HEADER,
            ontology_rid=self.rid1
        ).thenReturn(
            ListObjectTypesResponse(data=[obj1, obj2], next_page_token=None)
        )

        expect(list(self.client.list_object_types(ontology_rid=self.rid1))).to(equal(
            [
                FinalObjectType(
                    api_name=obj1_api_name, description=obj1_desc, primary_key=obj1_pk, rid=obj1_rid,
                    properties={obj1_propname: {'description': obj1_propdesc, 'base_type': obj1_propbase}}
                ),
                FinalObjectType(
                    api_name=obj2_api_name, description=obj2_desc, primary_key=obj2_pk, rid=obj2_rid,
                    properties={obj2_propname: {'description': obj2_propdesc, 'base_type': obj2_propbase}}
                )
            ]
        ))

    def test_get_object_type(self):
        pass

