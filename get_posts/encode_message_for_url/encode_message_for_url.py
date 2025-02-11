import urllib


def encode_message_for_url(message):
    return urllib.parse.quote(message)