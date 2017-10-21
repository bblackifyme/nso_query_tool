"""Module for Input class."""
from ForEach import ForEach

class QueryInput():
    """Class to abstract the building of a query.

    Simplifies and abstracts the foreach, expressions & filters.
    """

    def __init__(self, _from, select, where=False):
        """Contructor for Input."""
        self._from = _from
        self.select = select
        self.where = where
        self.foreach = self.foreach()
        self.expressions = []
        self._build_expressions()


    def foreach(self):
        device_filters = []
        path = ""
        for item in self._from:
                if item != "path":
                    device_filters.append(item)
                else:
                    path = item['path']
        return ForEach(where_filters=self.where, device_filters=device_filters, path=path ).foreach()

    def _build_expressions(self):
        """Method to collate and build JSON data for select statemenets."""
        for statement in self.select:
            self._add_select(path=statement, label=statement)

    def _add_select(self, path, result_type="string", label=False):
        """Add a selection statement to the query.

        Expression form:
        {"expression":"name","result-type":["string"]}
        """
        if label is False:
            self.expressions.append({
                "expression": path, "result-type": [result_type]})
        else:
            self.expressions.append({
                "label": label,
                "expression": path,
                "result-type": [result_type]
                    })

    def build_foreach(self):
        """Translate the from and where statements.

        into an XPATH path to use as the foreach
        """
        # Build filters for end of Path
        # This may get funky with OR filters
        # TODO This got spagetti pretty quick...
        # TODO Simplify...
        if self.where is not False and self._from != ["*"]:
            filters = " and "
            for item in self.where:
                filters += item + " "
            filters += "]"
        elif self.where is not False and self._from == ["*"]:
            filters = ""
            for item in self.where:
                if item is self.where[0]:
                    filters += item + " "
                else:
                    filters += "and " + item + " "
            filters += "]"
        else:
            filters = "]"

        # build device selections
        base = "/devices/device["
        for selection in self._from:
            # Determine if this is the first FROM statement
            if selection == self._from[0]:
                or_tracker = ""
            else:
                or_tracker = " or "
            # Begin adding in the selections
            if "device-group" in selection:
                xpath = "name=/devices/device-group[name='{}']/member".format(
                    selection["device-group"])
                base += or_tracker + xpath
            elif "device" in selection:
                base += or_tracker + "name='{}'".format(selection["device"])
            elif selection == "*":
                pass
            else:
                # TODO Implmenet custum error. For now Index is close enough...
                raise IndexError(str(selection) + "Is not an option")

        if self.where is False and self._from != ["*"]:
            return base + filters
        elif self.where is False:
            return "/devices/device"
        else:
            return base + filters

if __name__ == "__main__":
    select= ['name',"config/ios:ip/http/server", "platform/model", "platform/version", "platform/name"]
    _from= ["*"]
    #where= ["config/ios:ip/http/server='true'"]
    print QueryInput(_from=_from, select=select, where=where).foreach
