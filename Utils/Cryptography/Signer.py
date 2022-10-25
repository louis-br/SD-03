from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
import base64
import json


class Signer():
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate(self):
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def b64_encode(self, bytes: bytes):
        return base64.b64encode(bytes).decode(encoding="utf-8")

    def b64_decode(self, str: str):
        return base64.b64decode(str)

    def public_key_b64(self):
        return self.b64_encode(self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ))

    def from_public_key_b64(self, public_key: str):
        public_key = self.b64_decode(public_key)
        self.public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key)

    def sign_b64(self, data: bytes):
        if not self.private_key:
            return None
        return self.b64_encode(self.private_key.sign(data))

    def verify_b64(self, signature: bytes, data: bytes):
        signature = self.b64_decode(signature)
        return self.public_key.verify(signature, data)

    def json_dict_bytes(self, dict: dict):
        return json.dumps(dict, sort_keys=True, ensure_ascii=True).encode(encoding="utf-8")
