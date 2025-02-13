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
from expects import expect, equal, raise_error
from unittest.mock import patch

from palantir.objects.client import ObjectsClient
from palantir.objects.core import Ontology
from palantir.objects import list_ontologies, ontology
from palantir.core.types import ResourceIdentifier, PalantirContext

from palantir.core.config import StaticTokenProvider, StaticHostnameProvider, AuthToken, StaticOntologyRidProvider


class TestObjects:

    AUTH_HEADER: str = "auth-header"

    @pytest.fixture(autouse=True)
    def before(self):
        self.ontology1 = Ontology(
            rid=ResourceIdentifier.try_parse("ri.ontology.main.ontology.1"),
            description="Description for first ontology",
            display_name="Display for first ontology",
            client=None
        )
        self.ontology2 = Ontology(
            rid=ResourceIdentifier.try_parse("ri.ontology.main.ontology.2"),
            description="Description for second ontology",
            display_name="Display for second ontology",
            client=None
        )

    def test_list_ontologies_with_no_input(self):
        with patch.object(
                ObjectsClient, 'list_ontologies', return_value=[self.ontology1, self.ontology2]
        ) as mocked_method:
            found_ontologies = list_ontologies()
            mocked_method.assert_called()
            expect(found_ontologies[0]).to(equal(self.ontology1))
            expect(found_ontologies[1]).to(equal(self.ontology2))

    def test_list_ontologies_with_ctx_input(self):
        with patch('palantir.objects.ObjectsClient') as mocked_client:
            mocked_client.return_value.list_ontologies.return_value = [self.ontology1, self.ontology2]
            ctx: PalantirContext = PalantirContext(
                StaticHostnameProvider("unused"),
                StaticTokenProvider(AuthToken(self.AUTH_HEADER))
            )
            found_ontologies = list_ontologies(ctx)
            mocked_client.assert_called()
            expect(mocked_client.call_args[0][0].ctx).to(equal(ctx))
            expect(found_ontologies[0]).to(equal(self.ontology1))
            expect(found_ontologies[1]).to(equal(self.ontology2))

    def test_ontology_with_rid_input(self):
        with patch('palantir.objects.list_ontologies') as mocked_list:
            mocked_list.return_value = [self.ontology1, self.ontology2]
            expect(ontology(str(self.ontology1.rid))).to(equal(self.ontology1))
            expect(ontology(str(self.ontology2.rid))).to(equal(self.ontology2))
            expect(lambda: ontology("bad_rid")).to(raise_error(ValueError))

    def test_ontology_with_no_input(self):
        with patch('palantir.objects.context') as mocked_context:
            with patch('palantir.objects.list_ontologies') as mocked_list:
                mocked_list.return_value = [self.ontology1, self.ontology2]
                ctx: PalantirContext = PalantirContext(
                    StaticHostnameProvider("unused"),
                    StaticTokenProvider(AuthToken(self.AUTH_HEADER)),
                    StaticOntologyRidProvider(str(self.ontology1.rid))
                )
                mocked_context.return_value = ctx
                expect(ontology()).to(equal(self.ontology1))

                ctx.ontology_rid_provider = StaticOntologyRidProvider(str(self.ontology2.rid))
                mocked_context.return_value = ctx
                expect(ontology()).to(equal(self.ontology2))

                ctx.ontology_rid_provider = StaticOntologyRidProvider("bad_rid")
                mocked_context.return_value = ctx
                expect(lambda: ontology()).to(raise_error(ValueError))

    def test_ontology_with_ctx_input(self):
        with patch('palantir.objects.list_ontologies') as mocked_list:
            mocked_list.return_value = [self.ontology1, self.ontology2]
            ctx: PalantirContext = PalantirContext(
                StaticHostnameProvider("unused"),
                StaticTokenProvider(AuthToken(self.AUTH_HEADER)),
                StaticOntologyRidProvider(str(self.ontology1.rid))
            )
            expect(ontology(ctx=ctx)).to(equal(self.ontology1))

            ctx.ontology_rid_provider = StaticOntologyRidProvider(str(self.ontology2.rid))
            expect(ontology(ctx=ctx)).to(equal(self.ontology2))

            ctx.ontology_rid_provider = StaticOntologyRidProvider("bad_rid")
            expect(lambda: ontology(ctx=ctx)).to(raise_error(ValueError))

