from bot.messages import MESSAGES_PL

def test_message_placeholders():
    for key, text in MESSAGES_PL.items():
        assert "{date}" in text
        assert "{amount}" in text