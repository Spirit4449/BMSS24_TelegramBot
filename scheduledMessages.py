from datetime import datetime, timedelta

def get_scheduled_messages():
    messages = [
        ("Message 1", datetime.now() + timedelta(seconds=10)),
        ("Message 2", datetime.now() + timedelta(seconds=20)),
        ("Message 3", datetime.now() + timedelta(seconds=30))
    ]
    return messages
