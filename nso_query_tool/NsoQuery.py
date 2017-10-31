"""API Wrapper for the NSO Query API."""
import json
import requests
from QueryResult import QueryResult
from QueryInput import QueryInput


class NsoQuery():
    """Class repersenting a query made to the NSO.

    Sample usage:
            print query.results
    """

    def __init__(self, nso_server,
                 _from, select, where=False,
                 sortby=False, limit=False, offset=1):
        """Constructor for NsoQuery.

        Usage:
        input_object= NsoQuery(server, _from=_from, select=select, where=where)
        """
        self.inputs = QueryInput(select=select, _from=_from, where=where)
        self.server = nso_server.server
        self.username = nso_server.username
        self.password = nso_server.password
        self.foreach = self.inputs.foreach
        self.select = self.inputs.expressions
        self.sortby = sortby
        self.limit = limit
        self.offset = offset
        self.results = QueryResult(self._send_query(self._create_payload()))

    def _create_payload(self):
        """
        Create the JSON Payload for the HTTP Request.

        :return: Dictionary to be used for query payload/data
        """
        query = {"start-query": {
                    "foreach": self.foreach,
                    "select": self.select,
                    "offset": self.offset
                    }
                 }
        if self.limit is True:
            query["start-query"].update({"limit": self.limit})
        if self.sortby is True:
            # TODO Implement sortby
            pass

        return query

    def _send_query(self, payload):
        """Function for making a query against the NSO Query API."""
        url = "{}/api/query".format(self.server)
        headers = {
            'content-type': "application/vnd.yang.data+json",
            }

        get_result_handle = requests.request(
                                        "POST",
                                        url,
                                        data=json.dumps(payload),
                                        headers=headers,
                                        auth=(self.username, self.password),

                                        )
        try:
            if get_result_handle.status_code == 200:
                handle = get_result_handle.json()[
                        "tailf-rest-query:start-query-result"]["query-handle"]
            else:
                get_result_handle.raise_for_status()
        except KeyError:
            return get_result_handle

        handle_query = """
                { "tailf-rest-query:fetch-query-result": {"query-handle": %s}}
                       """ % handle
        return requests.request("POST",
                                url,
                                data=handle_query,
                                headers=headers,
                                auth=(self.username, self.password),
                                )
