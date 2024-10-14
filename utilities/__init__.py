import base64
from uuid import uuid4


def image_to_binary(filepath: str) -> str:
    prefix: str = "data:image/png;base64,"
    with open(filepath, "rb") as f:
        data: bytes = f.read()
    encoding: str = str(base64.b64encode(data))
    return f"{prefix}{encoding[2:-1]}"


def generated_id() -> str:
    return str(uuid4())[24:] + str(uuid4())[:8]
