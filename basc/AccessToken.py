class AccessToken:

    def __init__(self, token):
        if not self.__is_valid_access_token(str(token)):
            raise TypeError("Invalid token: " + token)

        self.token = token

    def get_access_token(self):
        return self.token

    def __is_valid_access_token(self, token):
        return token is not None and token.startswith("A") and 108 == len(token)
