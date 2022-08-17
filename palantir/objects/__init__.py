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
from palantir.core.types import PalantirContext
from palantir.core import context

from palantir.objects.client import ObjectsClient, ObjectServices


def list_ontologies(
    ctx: PalantirContext = None,
) -> typing.List[Ontology]:
    """
    Lists the ontologies visible to the user

    Args:
        ctx: An optional :class:`PalantirContext` (see :func:`palantir.core.context`) to override environment defaults.


    Returns: A list of ontologies visible to the user, implementing the `endpoint`_

    .. _endpoint:
            https://www.palantir.com/docs/foundry/api/ontology-resources/ontology/list-ontologies/

    Examples:
        >>> from palantir import objects

        >>> my_ontologies = objects.list_ontologies()
    """
    obj_client = ObjectsClient(ObjectServices(ctx or context()))
    ontologies = obj_client.list_ontologies()
    return ontologies


def get_ontology(rid: str = None, ctx: PalantirContext = None):
    """
    Create an object for the ontology

    Args:
        rid: An optional string for the resource identifier (rid) of the ontology. If provided, it overrides
         the ontology obtained from the environment.
        ctx: An optional :class:`PalantirContext` (see :func:`palantir.core.context`) to override environment defaults.

    Returns: A :class:`Ontology` object that can be used to interact with the specified ontology.

    Examples:
        >>> from palantir import objects

        >>> my_ontology = objects.get_ontology(rid="ri.ontology.main.ontology.c61d9ab5-2919-4127-a0a1-ac64c0ce6367")
    """
    all_ontologies = list_ontologies()
    if rid is not None:
        for ont in all_ontologies:
            if str(ont.rid) == rid:
                return ont
        raise ValueError("The ontology with the specified rid does not exist or is not visible to the user.")
    else:
        ctx = ctx or context()
        ontology_rid = ctx.ontology_rid_provider.get()
        if ontology_rid is None:
            raise ValueError("The ontology rid is not specified and it cannot be found in the environment either.")
        else:
            for ont in all_ontologies:
                if str(ont.rid) == ontology_rid:
                    return ont
            raise ValueError("The ontology obtained from the environment does not exist or is not visible to the user.")




