# Copyright (C) 2022 Borja Pérez Guasch
# Author: Borja Pérez Guasch
# Contact: borjaperez@icloud.com
# License: MIT

"""A module with the class that implements the Secret Santa algorithm."""


import random

from .config import InvalidConfigurationException, EmailServer, Game
from .email import connect_to_email_server, build_email_message


class SecretSanta:
    """
    Class that implements the Secret Santa algorithm and participants notification
    """

    @staticmethod
    def __sanitise_participant_attrs(participants: dict, participant: str) -> dict:
        attrs = participants[participant]

        # Trim the email
        attrs['email'] = attrs['email'].strip()

        # Indicate that a person cannot gift himself
        attrs['avoidGiftingTo'].append(participant)

        # Trim the names in the avoidGiftingTo list and omit empty values
        attrs['avoidGiftingTo'] = [name.strip() for name in attrs['avoidGiftingTo'] if name.strip()]

        # Remove duplicates in the list of people to avoid and people not present in the participants dictionary
        ignored_names = set(attrs['avoidGiftingTo']) - set(participants.keys())

        if ignored_names:
            print('WARNING: ignored names {} in the list of avoided people by {}'.format(ignored_names, participant))

        attrs['avoidGiftingTo'] = list(set(attrs['avoidGiftingTo']).intersection(set(participants.keys())))

        return attrs

    def __validate_game_data(self, participants: dict) -> dict:
        """
        Verifies that the participants argument is a dictionary with the expected fields and field types.

        :param participants: dictionary with the people to participate in the Secret Santa
        :raise: InvalidConfigurationException if any of the validation steps fail
        :return: same participant data with sanitised fields to ensure execution completion
        """

        # Verify that participants is a dictionary
        if type(participants) != dict:
            raise InvalidConfigurationException('The participants argument must be a dictionary '
                                                'with the names of the participants as keys')

        # Verify that the keys of the dictionary are non-empty strings
        if any(type(participant) != str or not participant.strip() for participant in participants):
            raise InvalidConfigurationException('The participants argument must be a dictionary '
                                                'with the names of the participants as keys')

        # Trim the keys of the dictionary
        participants = {name.strip(): participants[name] for name in participants}

        # Verify that there are at least two participants
        if len(participants) < 2:
            raise InvalidConfigurationException('The participants dictionary must include at least two entries')

        # Verify that every participant is a dictionary
        if any(type(participants[participant]) != dict for participant in participants):
            raise InvalidConfigurationException('Each participant must be represented as a dictionary '
                                                'and must have the "email" and "avoidGiftingTo" fields')

        # Verify that the email field is present in every participant
        if any('email' not in participants[participant] for participant in participants):
            raise InvalidConfigurationException('Each participant must have an "email" field')

        # verify that the email field is a non-empty string
        if any(type(participants[participant]['email']) != str or not participants[participant]['email'].strip()
               for participant in participants):
            raise InvalidConfigurationException('The "email" field must be a non-empty string')

        # Verify that the avoidGiftingTo field is present in every participant
        if any('avoidGiftingTo' not in participants[participant] for participant in participants):
            raise InvalidConfigurationException('Each participant must have an "avoidGiftingTo" field')

        # Verify that the avoidGiftingTo field is a list
        if any(type(participants[participant]['avoidGiftingTo']) != list for participant in participants):
            raise InvalidConfigurationException('The "avoidGiftingTo" field must be a list of strings '
                                                'with the names of the participants to avoid')

        # Verify that all the elements of the avoidGiftingTo field are strings
        if any(type(name) != str for participant in participants
               for name in participants[participant]['avoidGiftingTo']):
            raise InvalidConfigurationException('The "avoidGiftingTo" field must be a list of strings '
                                                'with the names of the participants to avoid')

        # Sanitise participant fields
        return {name.strip(): self.__sanitise_participant_attrs(participants, name) for name in participants}

    def __validate_game_configuration(self):
        """
        Validates the configuration of the game, checking if it can be solved given the specified restrictions.

        :raise: InvalidConfigurationException if the validation fails
        :return: None
        """

        # Initialise the number of people a participant can receive a gift from
        receiver_counts = {name: len(self.__participants.keys()) for name in self.__participants.keys()}

        # Initialise who each participant can give to, taking into account the people to avoid
        giver_options = {
            name: list(set(self.__participants.keys()) - set(self.__participants[name]['avoidGiftingTo']))
            for name in self.__participants.keys()
        }

        # Check if somebody cannot gift to anybody
        for name in giver_options:
            if not giver_options[name]:
                raise InvalidConfigurationException("Invalid scenario. {} cannot buy anyone a gift".format(name))

        # Check if more than one people can only gift to the same person
        people_with_multiple_presents = {name: 0 for name in self.__participants.keys()}

        for giver in giver_options:
            if len(giver_options[giver]) == 1:
                people_with_multiple_presents[giver_options[giver][0]] += 1

        people_with_multiple_presents = [name for name in people_with_multiple_presents.keys()
                                         if people_with_multiple_presents[name] > 1]

        if people_with_multiple_presents:
            raise InvalidConfigurationException("Invalid scenario. The following people would receive more than "
                                                "one present: {}".format(','.join(people_with_multiple_presents)))

        # Check if somebody cannot receive any present
        for name, values in self.__participants.items():
            # Decrease by one the number of gifts a participant can receive when somebody avoids them
            for avoided_receiver in values['avoidGiftingTo']:
                receiver_counts[avoided_receiver] -= 1

        people_without_present = [name for name in receiver_counts.keys() if receiver_counts[name] <= 0]

        if people_without_present:
            raise InvalidConfigurationException("Invalid scenario. The following people won't receive "
                                                "a present: {}".format(','.join(people_without_present)))

    def __restart_pairings(self) -> (list[str], list[str], list):
        """
        Resets the pools of givers and receivers and the list of pairings

        :return: list of givers, list of receivers and empty list of pairings
        """

        names = list(self.__participants.keys())

        return names, names.copy(), []

    def __create_pairings(self):
        """
        Creates random pairings for the Secret Santa scenario taking into account the applied restrictions.

        :return: list of pairings
        """

        givers, receivers, pairings = self.__restart_pairings()

        # Go until we have assigned each giver a receiver
        while givers:
            # Take a random giver and remove it from the list
            giver = random.choice(givers)
            givers.remove(giver)

            # There is nobody left who the giver can gift to. Restart the procedure
            if all(receiver in self.__participants[giver]['avoidGiftingTo'] for receiver in receivers):
                givers, receivers, pairings = self.__restart_pairings()
                continue

            # Take a random receiver ensuring they don't have to be avoided, and remove it from the list
            receiver = random.choice(receivers)

            while receiver in self.__participants[giver]['avoidGiftingTo']:
                receiver = random.choice(receivers)

            receivers.remove(receiver)
            pairings.append([giver, receiver])

        # Return pairings sorted by giver to better compare results when printed in the console
        return sorted(pairings, key=lambda x: x[0])

    def __init__(self, game_config: Game, email_config: EmailServer, participants: dict):
        """
        Constructor with parameters
        :param game_config: game configuration attributes
        :param email_config: email server configuration attributes
        :param participants: game participants
        """

        self.__game_config = game_config
        self.__email_config = email_config
        self.__participants = self.__validate_game_data(participants)
        self.__validate_game_configuration()

    def dry_run(self, silent: bool = False) -> list:
        """
        Creates giver-receiver pairings applying the specified participant restrictions.
        Doesn't send any email communication. Use this method to test your scenario configuration

        :param silent: boolean that specifies whether logs should not be printed in the console
        :return: list of created pairings. The first element of each pairing represents the giver and the second
        the receiver
        """

        pairings = self.__create_pairings()

        if not silent:
            print('Pairings:', pairings)

        return pairings

    def play(self, silent: bool = False) -> list:
        """
        Creates giver-receiver pairings applying the specified participant restrictions.
        Sends individual emails to participants to let them know whom they have to gift

        :param silent: boolean that specifies whether logs should not be printed in the console
        :return: list of created pairings. The first element of each pairing represents the giver and the second
        the receiver
        """

        with connect_to_email_server(self.__email_config.host, self.__email_config.port) as server:
            server.login(self.__email_config.username, self.__email_config.password)

            pairings = self.dry_run(silent)

            for pairing in pairings:
                msg = build_email_message(
                    self.__game_config.subject,
                    self.__game_config.body_generator_func(pairing),
                    self.__game_config.name,
                    self.__email_config.username,
                    self.__participants[pairing[0]]['email']
                )

                server.send_message(msg)

                if not silent:
                    print('Email sent to {} ({})'.format(self.__participants[pairing[0]]['email'], pairing[0]))

            return pairings
