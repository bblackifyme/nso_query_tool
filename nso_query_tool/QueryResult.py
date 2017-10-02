"""Module for Query Result Class."""


class QueryResult():
    """Class that repersents the results of a query.

    Attributes:
        status_code: HTTP Status Code of the Query
        full: The full json result of the original api call
        error: If there is an error, the error message
        results: The parsed results each dict repersents the 'foreach' item
    """

    def __init__(self, request_results):
        """Contructor for QueryResult."""
        self.status_code = request_results.status_code
        if request_results.status_code == 200:
            self.full = request_results.json()
            if 'result' in request_results.json()[
                    "tailf-rest-query:query-result"]:
                self.json = self._collate_results(request_results.json()[
                    "tailf-rest-query:query-result"]['result'])
            else:
                self.json = {"error": "No query results."}
        else:
            self.error = request_results.text
            self.json = {
                "error": "Error code {}".format(request_results.status_code)
                    }

    def __str__(self):
        """String Repersentation of the results JSON."""
        return str(self.json)

    def __iter__(self):
        """Iterator for the results.

        Return the dictionary repersenting the row.
        """
        for row in self.json:
            yield row

    def length(self):
        """Return how many results were returned by the query."""
        return len(self.json)

    def _collate_results(self, request_json):
        """Put results in an easier to parse and read dict."""
        result_bucket = []
        for selection in request_json:
            result_bucket.append(selection["select"])
        collated_results = []
        for row in result_bucket:
            row_results = {}
            for item in row:
                row_results.update({item["label"]: item["value"]})
            collated_results.append(row_results)
        return collated_results
