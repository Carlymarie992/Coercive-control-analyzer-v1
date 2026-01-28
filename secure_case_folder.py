import os
from pathlib import Path
from cryptography.fernet import Fernet

class SecureCaseFolder:
    """
    Secure personal folder for ongoing documentation and evidence storage.
    """
    def __init__(self, case_id: str, base_dir: str = 'cases'):
        self.case_id = case_id
        self.base_dir = Path(base_dir)
        self.folder = self.base_dir / case_id
        self.folder.mkdir(parents=True, exist_ok=True)
        self.key_path = self.folder / 'key.key'
        self.key = self._load_or_create_key()
        self.fernet = Fernet(self.key)

    def _load_or_create_key(self):
        if self.key_path.exists():
            return self.key_path.read_bytes()
        key = Fernet.generate_key()
        self.key_path.write_bytes(key)
        return key

    def store_file(self, filename: str, data: bytes):
        encrypted = self.fernet.encrypt(data)
        with open(self.folder / filename, 'wb') as f:
            f.write(encrypted)

    def retrieve_file(self, filename: str) -> bytes:
        with open(self.folder / filename, 'rb') as f:
            encrypted = f.read()
        return self.fernet.decrypt(encrypted)

    def list_files(self):
        return [f.name for f in self.folder.iterdir() if f.is_file() and f.name != 'key.key']
