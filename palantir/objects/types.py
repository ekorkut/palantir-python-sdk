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

from enum import Enum
from dataclasses import dataclass
from typing import Any


class FilterTerm(Enum):
    CONTAINS = "contains"
    EQUAL = "eq"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    IS_NULL = "is"


class OrderTerm(Enum):
    ASCENDING = ":asc"
    DESCENDING = ":desc"


@dataclass(frozen=True)
class PropertyFilter:
    property: str
    filter: FilterTerm
    value: Any




