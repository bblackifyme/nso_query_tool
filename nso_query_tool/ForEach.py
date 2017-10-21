
class ForEach(object):
    """Class reperesenting a foreach statement."""

    def __init__(self, device_filters, path="", where_filters=""):
        self.base = "devices/device"
        self.device_filters = ""
        self.where_filters = ""
        self.path =  path
        for item in device_filters:
            self.add_device_filters(item)
        if where_filters != False:
            for item in where_filters:
                self.add_where_filters(item)


    def add_device_filters(self, filters):
        """Add to the base for a device_filter.

            Filter is in the form of a dictionary:
            {"device-group":"name"} or {"device":"device_name"}
        """
        if self.device_filters == "":
            if "device-group" in filters:
                self.device_filter = "[name=/devices/device-group[name='{}']/member]".format(filters["device-group"])
            elif "device" in filters:
                self.device_filters = "[name='{}']".format(filters["device"])
        else:
            self.device_filters = self.device_filters[:-1]
            if "device-group" in filters:
                self.device_filters += " or name=/devices/device-group[name='{}']/member]".format(filters["device-group"])
            elif "device" in filters:
                self.device_filters += " or name='{}']".format(filters["device"])

    def add_where_filters(self, where_filter):
        """Add to the base the where statement filters."""
        if self.where_filters == "":
            self.where_filters += "[{}]".format(where_filter)
        else:
            self.where_filters = self.where_filters[:-1] + " and " + where_filter + "]"

    def foreach(self):
        if self.path is "":
            return self.base + self.device_filters + self.where_filters
        else:
            return self.base + self.device_filters + "/" + self.path + self.where_filters


if __name__ == "__main__":
    var = ForEach(device_filters=[{"device":"acc1-pl-sw1"}], path="config/ios:interface/GigabitEthernet", where_filters=["name=0/1"])
    print var.foreach()
