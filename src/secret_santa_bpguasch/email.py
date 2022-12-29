# Copyright (C) 2022 Borja Pérez Guasch
# Author: Borja Pérez Guasch
# Contact: borjaperez@icloud.com
# License: MIT

"""A module with helper methods to work with email messaging."""


import smtplib
import ssl

from email.utils import formataddr
from email.message import EmailMessage


def connect_to_email_server(host: str, port: int) -> smtplib.SMTP_SSL:
    """
    Establishes a connection with an email server

    :param host: email server host
    :param port: email server port
    :return: object representing the connection with the server
    """

    context = ssl.create_default_context()
    return smtplib.SMTP_SSL(host, port, context=context)


def build_email_message(subject: str, body: str, sender_id: str, from_addr: str, to: str) -> EmailMessage:
    """
    Builds an object that encapsulates an email message

    :param subject: email subject
    :param body: email body
    :param sender_id: name representing the identity of the sender
    :param from_addr: sender address
    :param to: receiver address
    :return: object representing the email message
    """

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = formataddr((sender_id, from_addr))
    msg['To'] = to

    return msg
