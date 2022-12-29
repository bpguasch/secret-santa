import unittest

from src.secret_santa_bpguasch import *

email_config = EmailServer(host="smtp.gmail.com", port=465, username='', password='')
game_config = Game(name="Smith Secret Santa", budget=30, subject="Smith's family Secret Santa 2022")


class TestInvalidScenarios(unittest.TestCase):
    def test_people_without_gift(self):
        participants = {
            'borja': {
                "email": "borja@secretsanta.com",
                "avoidGiftingTo": ["mark"]
            },
            'john': {
                "email": "john@secretsanta.com",
                "avoidGiftingTo": ["mark"]
            },
            'mark': {
                "email": "mark@secretsanta.com",
                "avoidGiftingTo": [""]
            }
        }

        try:
            ss = SecretSanta(game_config, email_config, participants)
            ss.dry_run(silent=True)
            self.assertTrue(False)
        except InvalidConfigurationException:
            self.assertTrue(True)

    def test_people_with_multiple_gifts(self):
        participants = {
            'borja': {
                "email": "borja@secretsanta.com",
                "avoidGiftingTo": ["mark"]
            },
            'john': {
                "email": "john@secretsanta.com",
                "avoidGiftingTo": [""]
            },
            'mark': {
                "email": "mark@secretsanta.com",
                "avoidGiftingTo": ["borja"]
            }
        }

        try:
            ss = SecretSanta(game_config, email_config, participants)
            ss.dry_run(silent=True)
            self.assertTrue(False)
        except InvalidConfigurationException:
            self.assertTrue(True)


class TestAlgorithmCompletion(unittest.TestCase):
    def test_with_restrictions(self):
        participants = {
            'borja': {
                "email": "borja@secretsanta.com",
                "avoidGiftingTo": ["mark"]
            },
            'john': {
                "email": "john@secretsanta.com",
                "avoidGiftingTo": ["borja"]
            },
            'mark': {
                "email": "mark@secretsanta.com",
                "avoidGiftingTo": []
            }
        }

        ss = SecretSanta(game_config, email_config, participants)

        for i in range(1000):
            ss.dry_run(silent=True)

        self.assertTrue(True)

    def test_without_restrictions(self):
        participants = {
            'borja': {
                "email": "borja@secretsanta.com",
                "avoidGiftingTo": []
            },
            'john': {
                "email": "john@secretsanta.com",
                "avoidGiftingTo": []
            },
            'mark': {
                "email": "mark@secretsanta.com",
                "avoidGiftingTo": []
            }
        }

        ss = SecretSanta(game_config, email_config, participants)

        for i in range(1000):
            ss.dry_run(silent=True)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
