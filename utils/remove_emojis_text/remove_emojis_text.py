import emoji

def remove_emojis_text(text):
    new_text = emoji.replace_emoji(str(text), replace='')
    return new_text