import random
import secrets
import string
from abc import abstractmethod

# email,password generators
# for bigger testing it might be better to write it
# using factory pattern as the concrete generation
# could be substituted


def get_random_string():
    return "".join(random.choices(string.ascii_letters, k=10))


def get_random_email():
    return f"{get_random_string()}@mail.com"


def get_random_password():
    return get_random_string()


class TokenGeneratorInterface:
    @abstractmethod
    def get(self) -> str:
        pass


class SecretsTokenGenerator(TokenGeneratorInterface):
    def __init__(self, nbytes=16):
        self.nbytes = nbytes

    def get(self) -> str:
        return secrets.token_hex(self.nbytes)


token_generator: TokenGeneratorInterface = SecretsTokenGenerator()
