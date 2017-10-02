"""Class repersenting an NSO Server.

Is a container for server hostname, username and password
"""


class NsoServer():
    """Class that repersents the NSO servier and log in info.

    Usage: server = NsoServer("server", "user", "pass")
    """

    def __init__(self, server, username, password):
        """Contructor for NsoServer."""
        self.server = server
        self.username = username
        self.password = password
