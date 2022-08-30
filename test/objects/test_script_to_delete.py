import pytest


class TestMyScript:

    def test_script(self):
        pass
        """
        from palantir import objects

        my_ontology = objects.ontology()

        all_object_types = list(my_ontology.list_object_types())

        airport_type = my_ontology.object_type("ExampleDataAirport")
        bad_object_type = my_ontology.object_type("bad")

        print("Hello world")
        """

