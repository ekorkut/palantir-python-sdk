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


from expects import expect, equal
from unittest.mock import patch

from palantir.objects.client import ObjectsClient
from palantir.objects.types import Ontology
from palantir.objects import list_ontologies
from palantir.core.types import ResourceIdentifier


class TestObjects:

    def test_list_ontologies(self):
        ont1 = Ontology(
            rid=ResourceIdentifier.try_parse("ri.ontology.main.ontology.1"),
            description="Description for first ontology",
            display_name="Display for first ontology"
        )
        ont2 = Ontology(
            rid=ResourceIdentifier.try_parse("ri.ontology.main.ontology.2"),
            description="Description for second ontology",
            display_name="Display for second ontology"
        )
        with patch.object(ObjectsClient, 'list_ontologies', return_value=[ont1, ont2]) as mocked_method:
            found_ontologies = list_ontologies()
            mocked_method.assert_called()
            expect(found_ontologies[0].description).to(equal(ont1.description))
            expect(found_ontologies[0].display_name).to(equal(ont1.display_name))
            expect(found_ontologies[0].rid).to(equal(ont1.rid))
            expect(found_ontologies[1].description).to(equal(ont2.description))
            expect(found_ontologies[1].display_name).to(equal(ont2.display_name))
            expect(found_ontologies[1].rid).to(equal(ont2.rid))
