# Palantir Python SDK
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/palantir-sdk)
[![PyPI](https://img.shields.io/pypi/v/palantir-sdk)](https://pypi.org/project/palantir-sdk/)
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey.svg)](https://opensource.org/licenses/Apache-2.0)
[![Autorelease](https://img.shields.io/badge/Perform%20an-Autorelease-success.svg)](https://autorelease.general.dmz.palantir.tech/palantir/palantir-python-sdk)

This SDK is incubating and subject to change.

## Setup

```commandline
pip install palantir-sdk
```

```commandline
conda config --add channels conda-forge  # add conda-forge channel if not already enabled
conda install palantir-sdk
mamba install palantir-sdk  # alternatively install with mamba
```

Configuration for hostname and an authentication token are provided by environment variables (`PALANTIR_HOSTNAME`, `PALANTIR_TOKEN`):

* `PALANTIR_HOSTNAME` is the hostname of your instance e.g. `example.palantirfoundry.com`
* `PALANTIR_TOKEN` is a token acquired from the `Tokens` section of Foundry Settings 

Authentication tokens serve as a private password and allows a connection to Foundry data. Keep your token secret and do not share it with anyone else. Do not add a token to a source controlled or shared file.

In addition, if you interact with objects, configuration for ontology resource identifier can be provided by the environment variable `PALANTIR_ONTOLOGY_RID`.

## Examples

Using this SDK, you can interact both with datasets and objects.

### Dataset examples

#### Read a Foundry Dataset into a Pandas DataFrame
```python
from palantir.datasets import dataset

dataset("/Path/to/dataset") \
    .read_pandas()
```

```
            id        word  length     double boolean
0            0           A     1.0  11.878200       1
1            1           a     1.0  11.578800       0
2            2          aa     2.0  15.738500       1
3            3         aal     3.0   6.643900       0
4            4       aalii     5.0   2.017730       1
...        ...         ...     ...        ...     ...
235881  235881      zythem     6.0  19.427400       1
235882  235882      Zythia     6.0  14.397100       1
235883  235883      zythum     6.0   3.385820       0
235884  235884     Zyzomys     7.0   6.208830       1
235885  235885  Zyzzogeton    10.0   0.947821       0

[235886 rows x 5 columns]
```

#### Write a Pandas DataFrame to a Foundry Dataset
```python
import pandas as pd
from palantir.datasets import dataset

df = pd.DataFrame({
    "string": ["one", "two"],
    "integer": [1, 2]
})

ds = dataset(f"/Path/to/dataset", create=True)
ds.write_pandas(df)
```

#### List files in a Dataset
```python
from palantir.datasets import dataset

files = dataset("/Path/to/dataset") \
    .list_files() # returns a generator over pages of files

list(files)
```

```
[
    File("ri.foundry.main.dataset.2ed83c69-e87e-425e-9a1c-03b77b5b0831", "file.txt")
]
```

#### Read the contents of a file from a dataset (by name)
```python
from palantir.datasets import dataset

dataset("/Path/to/dataset") \
    .file("file.txt") \
    .read()
```
```python
b'Hello!'
```

#### Read the contents of a file from a dataset (by exploration / listing)
```python
from palantir.datasets import dataset

files = dataset("/Path/to/dataset").list_files()
next(files).read()
```
```
b'Hello!'
```

#### Dataset functions also accept Resource Identifiers (rids)
```python
from palantir.datasets import dataset

dataset("ri.foundry.main.dataset.a0a94f00-754e-49ff-a4f6-4f5cc200d45d") \
    .read_pandas()
```
```
  string  integer
0    one        1
1    two        2
```

### Object examples

#### List ontologies
```python
from palantir import objects
onts = objects.list_ontologies()
onts
```
```python
[
    Ontology(rid=ri.ontology.main.ontology.c61d9ab5-2919-4127-a0a1-ac64c0ce6367, description='The ontology shared with our suppliers', display_name='Shared ontology'),
    Ontology(rid=ri.ontology.main.ontology.00000000-0000-0000-0000-000000000000, description='The default Ontology.', display_name='Ontology')
]
```

#### Get an ontology to work with
You can use one of the outputs of `list_ontologies` as your handle to work with your ontology:
```python
# Use output of list_ontologies
from palantir import objects
onts = objects.list_ontologies()
my_ontology = onts[0]
my_ontology
```
```python
Ontology(rid=ri.ontology.main.ontology.c61d9ab5-2919-4127-a0a1-ac64c0ce6367, description='The ontology shared with our suppliers', display_name='Shared ontology')
```
, or you can use `ontology()` with a resource identifier (RID) input argument:
```python
# Get ontology from an ontology resource identifier (RID)
from palantir import objects
my_ontology = objects.ontology("ri.ontology.main.ontology.c61d9ab5-2919-4127-a0a1-ac64c0ce6367")
```
```python
Ontology(rid=ri.ontology.main.ontology.c61d9ab5-2919-4127-a0a1-ac64c0ce6367, description='The ontology shared with our suppliers', display_name='Shared ontology')
```
, or without any input argument if the environment variable `PALANTIR_ONTOLOGY_RID` is set:
```python
# Get ontology from the environment (if the environment variable `PALANTIR_ONTOLOGY_RID` is set)
from palantir import objects
my_ontology = objects.ontology()
```
```python
Ontology(rid=ri.ontology.main.ontology.c61d9ab5-2919-4127-a0a1-ac64c0ce6367, description='The ontology shared with our suppliers', display_name='Shared ontology')
```

#### List object types in your ontology
```python
all_object_types = my_ontology.list_object_types() # returns a generator
an_object_type = next(all_object_types)
an_object_type
```
```python
ObjectType(api_name="ExampleDataAirport", primary_key="['airport']", rid="ri.ontology.main.object-type.000fee5d-7c54-4c6c-afd1-cef71c167c08")
```

#### Get an object type in your ontology
```python
airport_type = my_ontology.object_type("ExampleDataAirport")
airport_type
```
```python
ObjectType(api_name="ExampleDataAirport", primary_key="['airport']", rid="ri.ontology.main.object-type.000fee5d-7c54-4c6c-afd1-cef71c167c08")
```

#### List object instances for an object type
You can use `list_objects()` on an object type to get instances:
```python
airports = my_ontology.object_type("ExampleDataAirport").list_objects()
an_airport = next(airports)
an_airport
```
```python
# TODO: Put output here
```
, optionally limiting the properties returned with `properties` input argument, and ordering the results using `order_by` input argument:
```python
# Get airports returning with only properties X, Y, and Z and ordered by X in ascending order
from palantir.objects import OrderTerm
airports = my_ontology.object_type("ExampleDataAirport").list_objects(
    properties=["airport", "airportCountryName", "numberOfCarriers"],
    order_by=[("airportCountryName", OrderTerm.ASCENDING), ("numberOfCarriers", OrderTerm.DESCENDING)]
)
an_airport = next(airports)
```
```python
# TODO: Put output here
```

#### Filtering objects
`list_objects` support filtering through the `filters` input argument. The filters applied on the same property are treated as "OR" and the ones on different properties treated as "AND":
```python
from palantir.objects import PropertyFilter, FilterTerm
ny_state_big_airports = my_ontology.object_type("ExampleDataAirport").list_objects(
    filters=[
        PropertyFilter("airportCountryName", FilterTerm.EQUAL, "United States"),
        PropertyFilter("airportStateCode", FilterTerm.EQUAL, "NY"),
        PropertyFilter("numberOfCarriers", FilterTerm.GREATER_THAN, 5)
    ]
)
next(ny_state_big_airports)
```
```python
# TODO: Put output here
```

#### Get object
You can get an object from an object type specifying its primary key, optionally limiting the properties returned.
```python
jfk_airport = my_ontology.object_type("ExampleDataAirport").object(
    "JFK",
    properties=["displayAirportName", "displayCityMarketNameFull"]
)
jfk_airport
```
```python
# TODO: Put output here
```
#### List linked objects
You can list the linked object instances on an object using `list_linked_objects`:
```python
all_aircraft_currently_in_jfk = jfk_airport.list_linked_objects(
    "airport-to-current-aircraft",   
)
next(all_aircraft_currently_in_jfk)
```
```python
# TODO: Put output here
```
, optionally limiting the properties returned with `properties` input argument and using the same filtering mechanism above through `filters` input argument:
```python
large_boeing_aircraft_currently_in_jfk = jfk_airport.list_linked_objects(
    "airport-to-current-aircraft",
    properties=["tailNumber", "model", "numberOfSeats"],
    filters=[        
        PropertyFilter("manufacturer", FilterTerm.EQUAL, "United States"),
        PropertyFilter("numberOfSeats", FilterTerm.GREATER_THAN_OR_EQUAL, 200),
    ]
)
```
```python
# TODO: Put output here
```

#### Get linked object
You can get a linked object instance from an instance specifying the link type and primary key for the linked object through input arguments:
```python
jfk_to_mia_route = jfk_airport.linked_object(
    "departing-airport-to-route",
    "primary_key_value_for_jfk_to_mia"
)
jfk_to_mia_route
```
```python
# TODO: Put output here
```

#### Searching and querying objects (Experimental)
You can search objects using the experimental [query language](https://www.palantir.com/docs/foundry/api/ontology-resources/objects/search/) and [search by JSON](https://www.palantir.com/docs/foundry/api/ontology-resources/objects/search-json/). Note that as the respective links indicate, these features are experimental at this point and may change or be removed.

```python
ny_state_big_airports = my_ontology.object_type("ExampleDataAirport").query(
    # TODO: "equivalent_query_string_here"
)
next(ny_state_big_airports)
```
```python
# TODO: Put output here
```
```python
ny_state_big_airports = my_ontology.object_type("ExampleDataAirport").search(
    # TODO: "equivalent_json_string_here"
)
next(ny_state_big_airports)
```
```python
# TODO: Put output here
```


## Contributing

See the [CONTRIBUTING.md](./CONTRIBUTING.md) document.  Releases are published to [pypi](https://pypi.org/project/palantir-sdk/) on tag builds and are automatically re-published to [conda](https://anaconda.org/conda-forge/palantir-sdk) using [conda-forge](https://github.com/conda-forge/palantir-sdk-feedstock/).

## License
This project is made available under the [Apache 2.0 License](/LICENSE).
