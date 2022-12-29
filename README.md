# Secret Santa
Python implementation of a Secret Santa generator that notifies participants by email of whom they have to gift. Allows for defining restrictions between participants to prevent somebody from gifting specific people.

## In this page
- [Installation instructions](#installation-instructions)
- [Usage instructions](#usage-instructions)
- [Full working example](#full-working-example)
- [Documentation]()

## Installation instructions

### Install it using pip
This software has been packaged and uploaded to [PyPi, the Python Package Index](https://pypi.org/). To install it, simply run the following command:

```bash
pip install secret-santa-bpguasch
```

You can now review the [usage instructions](#usage-instructions).

### Use it in an AWS Lambda function

AWS Lambda is a serverless compute service that lets you run code without provisioning or managing servers. This Python package is provided as well as an AWS Lambda Layer for you to use in your functions. Follow these steps to add the Secret Santa Lambda Layer to your AWS Lambda function:

1. From this repository, download the **secret_santa_layer.tar.gz** file
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