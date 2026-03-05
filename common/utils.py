import uuid


def generate_slug(text):
    """
    Very simple slug generator.
    """
    return f"{text.lower().replace(' ', '-')}-{uuid.uuid4().hex[:6]}"