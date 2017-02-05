class Page1Response:
    def __init__(self, response_id, step):
        self.id = response_id
        self.step = step

    def get_response_id(self):
        return self.id[0]

    def get_step(self):
        return self.step[0]


class Page2Response:
    def __init__(self, response_id, step, accounts):
        self.id = response_id
        self.step = step
        self.accounts = accounts

    def get_response_id(self):
        return self.id[0]

    def get_step(self):
        return self.step[0]

    def get_accounts(self):
        return self.accounts


class Page3Response:
    def __init__(self, code):
        self.code = code

    def get_code(self):
        return self.code
