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

import typing

from palantir.objects.types import Ontology
from palantir.core.types import PalantirContext, ResourceIdentifier
from palantir.core import context

from palantir.objects.client import ObjectsClient, ObjectServices


def list_ontologies(
    ctx: PalantirContext = None,
) -> typing.List[Ontology]:
    obj_client = ObjectsClient(ObjectServices(ctx or context()))
    ontologies = obj_client.list_ontologies()
    return [
        Ontology(
            description=ont.description,
            rid=ResourceIdentifier.try_parse(ont.rid),
            display_name=ont.display_name,
        )
        for ont in ontologies.data
    ]
