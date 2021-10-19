class Result(object):
    def __init__(self, message, json_result=None, moreinfo=None):
        self.message = message
        self.json_result = json_result
        self.moreinfo = moreinfo
