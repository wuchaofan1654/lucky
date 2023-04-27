

class Addon(object):
    def __init__(self):
        self.num = 1

    def request(self, flow):
        flow.request.headers["count"] = str(self.num)

    def response(self, flow):
        self.num = self.num + 1
        flow.response.headers["count"] = str(self.num)


if __name__ == "__main__":
    pass

