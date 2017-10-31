import unittest
#from nso_query_tool import NsoServer, NsoQuery, Input
from NsoServer import NsoServer
from NsoQuery import NsoQuery
from QueryInput import QueryInput as Input
from ForEach import ForEach

class TestNsoQueryTool(unittest.TestCase):
    """Test Suite for NSO Query Tool."""

    def setUp(self):
        """Create the NSO Server Object."""
        self.server = NsoServer('http://localhost:8080', "admin", "admin")

    def test_returns_200(self):
        """Test that a known proper query returns status code 200."""
        result = NsoQuery(self.server, _from= ["*"],select=["name"])
        self.assertEqual(result.results.status_code, 200)

    def test_Input_Builder_from_all(self):
        """Test to validate the _from = ['*'] functionality works."""
        foreach = Input(_from= ["*"], select=["name"]).build_foreach()
        self.assertEqual(foreach, "/devices/device")

    def test_Input_Builder_single_filter(self):
        """Test to validate the input builder works wih one filter."""
        foreach = Input(_from= ["*"], select=["name"], where=["name='test'"]).build_foreach()
        self.assertEqual(foreach, "/devices/device[name='test' ]")

    def test_Input_Builder_many_filters(self):
        """Test to validate the input builder works wih many filters."""
        foreach = Input(_from= ["*"], select=["name"], where=["name='test'", "port='22'"]).build_foreach()
        self.assertEqual(foreach, "/devices/device[name='test' and port='22' ]")

    def test_Input_Builder_single_expression(self):
        """Test to validate the input builder expressions are built properly."""
        expressions = Input(_from= ["*"], select=["name"], where=["name='test'", "port='22'"]).expressions
        self.assertEqual(expressions, [{'result-type': ['string'], 'expression': 'name', 'label': 'name'}])

    def test_Input_Builder_many_expressions(self):
        """Test to validate the input builder expressions are built properly for many selects."""
        expressions = Input(_from= ["*"], select=["name", "address"], where=["name='test'", "port='22'"]).expressions
        self.assertEqual(expressions, [{'result-type': ['string'], 'expression': 'name', 'label': 'name'},
            {'result-type': ['string'], 'expression': 'address', 'label': 'address'}])

    def test_Input_Builder_device_group_no_where(self):
        """Test to validate the input builder expressions are built properly for many selects."""
        foreach = Input(_from= [{"device-group":"test"}], select=["name"]).build_foreach()
        #"devices/device[name=/devices/device-group[name='acc1-pl']/member]
        self.assertEqual(foreach, "/devices/device[name=/devices/device-group[name='test']/member]")

    def test_multiple_device_groups(self):
        foreach = Input(_from= [{"device-group":"test"}, {"device-group":"test2"}], select=["name"]).build_foreach()
        correct_foreach = "/devices/device[name=/devices/device-group[name='test']/member or name=/devices/device-group[name='test2']/member]"
        self.assertEqual(foreach, correct_foreach)

    def test_device_group_and_device(self):
        foreach = Input(_from= [{"device-group":"test"}, {"device":"test2"}], select=["name"]).build_foreach()
        correct_foreach = "/devices/device[name=/devices/device-group[name='test']/member or name='test2']"
        self.assertEqual(foreach, correct_foreach)

    def test_returns_list(self):
        """Test that a known proper query returns data type list """
        result = NsoQuery(self.server, _from= ["*"], select=["name"])
        self.assertEqual(type(result.results.json), list)

    def test_result_is_dict(self):
        """Test that a known proper query results list contains only dictionarys """
        result = NsoQuery(self.server, _from= ["*"] ,select=["name"])
        for each in result.results.json:
            self.assertEqual(type(each), dict)

    def test_result_dict_keys(self):
        """Test that returned result row dictionarys have the correct keys """
        result = NsoQuery(self.server, _from= ["*"], select=["name"])
        for each in result.results.json:
            self.assertEqual("name" in each, True)

    def test_invalid_foreach(self):
        """Test that returned result row dictionarys have the correct keys """
        result = NsoQuery(self.server,_from= [{"device":"not a device"}], select=["name"])
        result.results.json = {"result":"No query results. Validate the foreach statement."}

    def test_foreach_builder(self):
        """ Test that the foreach builder works properly. """
        foreach = ForEach(device_filters=[{"device":"acc1-pl-sw1"}])
        correct_foreach = "devices/device[name='acc1-pl-sw1']"
        self.assertEqual(foreach.foreach(), correct_foreach)

    def test_foreach_builder_with_path(self):
        """ Test that the foreach builder works properly. """
        foreach = ForEach(device_filters=[{"device":"acc1-pl-sw1"}], path="config/ios:interface/GigabitEthernet")
        correct_foreach = "devices/device[name='acc1-pl-sw1']/config/ios:interface/GigabitEthernet"
        self.assertEqual(foreach.foreach(), correct_foreach)

    def test_foreach_builder_with_path_al(self):
        """ Test that the foreach builder works properly. """
        foreach = ForEach(device_filters=["*", path="config/ios:interface/GigabitEthernet")
        correct_foreach = "devices/device/config/ios:interface/GigabitEthernet"
        self.assertEqual(foreach.foreach(), correct_foreach)

    def test_foreach_builder_with_path_and_where(self):
        """ Test that the foreach builder works properly. """
        foreach = ForEach(device_filters=[{"device":"acc1-pl-sw1"}], path="config/ios:interface/GigabitEthernet", where_filters=["name=0/1"])
        correct_foreach = "devices/device[name='acc1-pl-sw1']/config/ios:interface/GigabitEthernet[name=0/1]"
        self.assertEqual(foreach.foreach(), correct_foreach)



if __name__ == '__main__':
    unittest.main()
