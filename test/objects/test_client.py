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
from palantir.objects.rpc.api import APIService, ListOntologiesResponse, Ontology
from palantir.objects.types import (
    Ontology as FinalOntology
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

    def test_list_ontologies(self):
        rid1 = "ri.ontology.main.ontology.1"
        desc1 = "First ontology description"
        disp1 = "First ontology display"
        rid2 = "ri.ontology.main.ontology.2"
        desc2 = "Second ontology description"
        disp2 = "Second ontology display"

        when(self.api_service).list_ontologies(
            auth_header=self.AUTH_HEADER
        ).thenReturn(ListOntologiesResponse(
            data=[
                Ontology(
                    description=desc1,
                    display_name=disp1,
                    rid=rid1
                ),
                Ontology(
                    description=desc2,
                    display_name=disp2,
                    rid=rid2
                )
            ]
        ))
        expected_ontologies = [
            FinalOntology(
                rid=ResourceIdentifier.try_parse(rid1),
                description=desc1,
                display_name=disp1
            ),
            FinalOntology(
                rid=ResourceIdentifier.try_parse(rid2),
                description=desc2,
                display_name=disp2
            )
        ]
        expect(self.client.list_ontologies()).to(
            equal(expected_ontologies)
        )
