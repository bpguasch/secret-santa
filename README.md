# Secret Santa
Python implementation of a Secret Santa generator that notifies participants by email of whom they have to gift. Allows for defining restrictions between participants to prevent somebody from gifting specific people.

Enjoy it and have fun 😁 I'll be happy to know if you use it, so don't hesitate to contact me!

## In this page
- [Features](#features)
- [Installation instructions](#installation-instructions)
- [Usage instructions](#usage-instructions)
- [Full working example](#full-working-example)
- [Documentation](#documentation)

## Features
This package provides the following functionalities:

- **100% free Secret Santa generator**: generate with very few lines of code the pairings for your yearly family Secret Santa! You only need to specify the participants.
- **Specify avoid rules**: easily specify which participants should avoid whom and let the algorithm work its magic! If you provide too many rules and the scenario cannot be solved, you will be rapidly alerted.
- **Communication via email**: communicate each participant by email whom they have to gift. You can send the emails using any account that you own.
- **Email body customisation**: provide your own email template for the automatically generated emails.
- **Dry run mode**: test your rules in a safe environment that prevents emails from being sent.

## Installation instructions

### Install it using pip
This software has been packaged and uploaded to [PyPi, the Python Package Index](https://pypi.org/). To install it, simply run the following command:

```bash
pip install secret-santa-bpguasch
```

You can now review the [usage instructions](#usage-instructions).

### Use it in an AWS Lambda function

AWS Lambda is a serverless compute service that lets you run code without provisioning or managing servers. This Python package is provided as well as an AWS Lambda Layer for you to use in your functions. Follow these steps to add the Secret Santa Lambda Layer to your AWS Lambda function:

1. From this repository, download the **python.zip** file
2. Navigate to the AWS Lambda section in the AWS Console, and select **Layers** under **Additional resources**
3. Select **Create layer**, give it a name and upload the file you recently downloaded
4. Open the Lambda function in which you would like to use the layer
5. Scroll to the bottom of the page and select **Add a layer**
6. Select **Custom layers** and choose the layer you just created

## Usage instructions

In your Python script, start by importing the package:

```python
from secret_santa_bpguasch import *
```

The application will email each participant whom they have to gift. For this reason, you have to provide some configuration parameters to send emails using one of your accounts:
```python
email_config = EmailServer(
    host="smtp.gmail.com",
    port=465,
    username='',
    password=''
)
```

Most likely you will need to create a dedicated App password to log into your email account programmatically. Taking Gmail as an example, you can learn more about it [here](https://support.google.com/accounts/answer/185833?hl=en). As the username field, you should specify your email address.

Next, define some configuration parameters for the Secret Santa Generator:

```python
game_config = Game(
    name="Smith Secret Santa",
    budget=30,
    subject="Smith's family Secret Santa 2022"
)
```

The game name will appear as the email sender identity (name). The subject represents the email subject and the budget value is used to compose the default email body. By default, each participant will receive and email with the following body: 
> ¡Hello, *giver_name*! You are *receiver_name*'s Secret Santa this year. Remember that the maximum budget is $*budget*. Happy shopping and merry Christmas :)

Optionally, you can define in the game configuration a method that generates the email body for a pairing of giver-receiver. Said method must receive a list as an argument and return a string. You can use this feature to customise the email as you want with HTML. To provide your generator method, you can do the following:

```python
def my_custom_email_body_generator(pairing: list) -> str:
    return 'The giver is {} and the receiver is {}'.format(pairing[0], pairing[1])
```

Then, you can include your method in the configuration as follows:

```python
game_config = Game(
    name="Smith Secret Santa",
    budget=30,
    subject="Smith's family Secret Santa 2022",
    body_generator_func=my_custom_email_body_generator
)
```

By doing this, your method will be automatically invoked whenever an email has to be sent to the giver.

Next, you need to supply the participants in the form of a dictionary:

```python
participants = {
    'borja': {
        "email": "borja@secretsanta.com",
        "avoidGiftingTo": ["mark"]
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
```

Finally, you can create an instance of SecretSanta to generate the pairings:

```python
secret_santa = SecretSanta(
    game_config,
    email_config,
    participants
)

# Call the method dry run to run tests and verify your configuration. 
# When you generate pairings in dry run mode, no emails are sent.
secret_santa.dry_run()

# When you are confident about the configuration, you can call the play method
#secret_santa.play()
```

## Full working example

The whole script together would look as follows:

```python
from secret_santa_bpguasch import *


def my_custom_email_body_generator(pairing: list) -> str:
    return 'The giver is {} and the receiver is {}'.format(pairing[0], pairing[1])


if __name__ == '__main__':
    email_config = EmailServer(
        host="smtp.gmail.com",
        port=465,
        username='',
        password=''
    )

    game_config = Game(
        name="Smith Secret Santa",
        budget=30,
        subject="Smith's family Secret Santa 2022",
        body_generator_func=my_custom_email_body_generator
    )   

    participants = {
        'borja': {
            "email": "borja@secretsanta.com",
            "avoidGiftingTo": ["mark"]
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

    secret_santa = SecretSanta(
        game_config,
        email_config,
        participants
    )

    secret_santa.dry_run()
```

## Documentation

The **secret-santa-bpguasch** Python package is organised in different modules. An overview of the classes contained in each module that can be worked with is provided below. Check the docstring for a detailed description of each method parameter:

### secret_santa_bpguasch.config

> A module with classes that encapsulate configuration attributes.

<details>
    <summary>Click to show package contents</summary>

#### InvalidConfigurationException

Exception subclass that represents an invalid configuration, either because the data is wrong formatted or because the scenario cannot be solved given the specified restrictions.

#### EmailServer

Class that encapsulates email server configuration parameters

###### Constructor

```python
EmailServer(host: str, port: int, username: str, password: str)
```

Parameters:

| **Name**  | **Type** | **Description**       |
|-----------|----------|-----------------------|
| host      | `str`    | Email server host     |
| port      | `int`    | Email server port     |
| username  | `str`    | Email server username |
| password  | `str`    | Email server password |

#### Game

Class that encapsulates game configuration parameters

###### Constructor

```python
Game(name: str, budget: float, subject: str, body_generator_func=None)
```

Parameters:

| **Name**            | **Type**     | **Description**                                                                 |
|---------------------|--------------|---------------------------------------------------------------------------------|
| name                | `str`        | Game name. Will appear as the sender identity (name)                            |
| budget              | `float`      | Budget for the present. Will appear in the default email body                   |
| subject             | `str`        | Subject of the email that each participant receives                             |
| body_generator_func | `descriptor` | Descriptor of a method used to generate a custom email body for a given pairing |

</details>

### secret_santa_bpguasch.algorithm

> A module with the class that implements the Secret Santa algorithm.

<details>
    <summary>Click to show package contents</summary>
    
#### SecretSanta

Class that implements the Secret Santa algorithm and participants notification

###### Constructor

```python
SecretSanta(game_config: Game, email_config: EmailServer, participants: dict)
```

Parameters:

| **Name**            | **Type**      | **Description**                       |
|---------------------|---------------|---------------------------------------|
| game_config         | `Game`        | Game configuration attributes         |
| email_config        | `EmailServer` | Email server configuration attributes |
| participants        | `dict`        | Game participants                     |

The constructor will raise an `InvalidConfigurationException` exception if the validation of the participants argument fails. The validation will fail if the structure does not have the expected fields and field types or if the scenario cannot be solved due to the specified restrictions.

###### Methods

| **Signature** | **Description**                                                                                                                                                                                                                                                       | **Return** | **Throws** |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|------------|
| dry_run()     | Creates giver-receiver pairings applying the specified participant restrictions. Doesn't send any email communication. Use this method to test your scenario configuration. The first element of the returned value represents the giver and the second the receiver. | `list`     | -          |
| play()        | Creates giver-receiver pairings applying the specified participant restrictions. Sends individual emails to participants to let them know whom they have to gift. The first element of the returned value represents the giver and the second the receiver.           | `list`     | -          |


</details>
