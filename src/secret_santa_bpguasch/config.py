# Copyright (C) 2022 Borja Pérez Guasch
# Author: Borja Pérez Guasch
# Contact: borjaperez@icloud.com
# License: MIT

"""A module with classes that encapsulate configuration attributes."""


class InvalidConfigurationException(Exception):
    """
    Exception subclass that represents an invalid configuration, either because the data is wrong formatted
    or because the scenario cannot be solved given the specified restrictions.
    """

    pass


class EmailServer:
    """
    Class that encapsulates email server configuration parameters
    """

    def __init__(self, host: str, port: int, username: str, password: str):
        """
        Initializer with parameters
        :param host: email server host
        :param port: email server port
        :param username: email server username
        :param password: email server password
        """

        self.host = host
        self.port = port
        self.username = username
        self.password = password


class Game:
    """
    Class that encapsulates gane configuration parameters
    """

    def __body_generator_func(self, pairing: list) -> str:
        return "¡Hello, {}! You are {}'s Secret Santa this year. " \
               "Remember that the maximum budget is ${}. Happy shopping and merry Christmas :)"\
            .format(pairing[0], pairing[1], self.budget)

    def __init__(self, name: str, budget: float, subject: str, body_generator_func=None):
        """
        Initializer with parameters
        :param name: game name. Will appear as the sender identity (name)
        :param budget: budget for the present. Will appear in the default email body
        :param subject: subject of the email that each participant receives
        :param body_generator_func: descriptor of a method used to generate a custom email body for a given pairing
        """

        self.name = name
        self.budget = budget
        self.subject = subject
        self.body_generator_func = body_generator_func if \
            body_generator_func is not None \
            else self.__body_generator_func

        # Test the body generator function to make sure it returns a string
        if type(self.body_generator_func(['', ''])) != str:
            raise InvalidConfigurationException('The body generator function must return a string')
