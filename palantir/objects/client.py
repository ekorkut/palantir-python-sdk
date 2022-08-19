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

from palantir.core.types import PalantirContext, ResourceIdentifier
from palantir.core.rpc import ConjureClient
from palantir.core.util import page_results
from palantir.objects.rpc.api import APIService
from palantir.objects.core import Ontology, ObjectType


class ObjectServices:
    def __init__(self, ctx: PalantirContext):
        self.factory = ConjureClient()
        self.ctx = ctx

    @property
    def api_service(self) -> APIService:
        return self.factory.service(
            APIService,
            f"https://{self.ctx.hostname}/api/v1",
        )


class ObjectsClient:
    def __init__(self, services: ObjectServices):
        self.services = services
        self.ctx = services.ctx

    @property
    def _api_service(self) -> APIService:
        return self.services.api_service

    def list_ontologies(self) -> typing.List[Ontology]:
        """
        :return: the list of ontologies visible to the user, implementing the `endpoint`_
        .. _endpoint:
            https://www.palantir.com/docs/foundry/api/ontology-resources/ontology/list-ontologies/
        """
        return [
            Ontology(
                description=ont.description,
                rid=ResourceIdentifier.try_parse(ont.rid),
                display_name=ont.display_name,
                client=self
            )
            for ont in self._api_service.list_ontologies(auth_header=self.ctx.auth_token).data
        ]

    def list_object_types(self, ontology_rid) -> typing.Generator["ObjectType", None, None]:
        for obj_type in page_results(
            values_extractor=lambda page: page.data,
            token_extractor=lambda page: page.next_page_token,
            page_supplier=lambda next_page_token: self._api_service.list_object_types(
                auth_header=self.ctx.auth_token, ontology_rid=ontology_rid
            ),
        ):
            yield ObjectType(
                api_name=obj_type.api_name,
                description=obj_type.description,
                primary_key=obj_type.primary_key,
                properties=obj_type.properties,
                rid=ResourceIdentifier.try_parse(obj_type.rid)
            )
