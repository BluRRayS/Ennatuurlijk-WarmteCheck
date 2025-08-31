import json
import os
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from src.config import StorageConfig


class StorageServiceInterface(ABC):
    """Abstract interface for storage services."""

    @abstractmethod
    def upload(self, payload: Dict[str, Any]) -> None:
        """Upload payload to a storage medium."""
        pass


class AzureBlobStorageService(StorageServiceInterface):
    """Storage service for Azure Blob Storage."""

    def __init__(self, config: StorageConfig):
        """Initialize the Azure Blob Storage service."""
        if not config.account_name:
            raise ValueError("Azure Storage Account Name is not configured.")
        self.config = config

        account_url = f"https://{self.config.account_name}.blob.core.windows.net"
        self._client = BlobServiceClient(
            account_url=account_url, credential=DefaultAzureCredential()
        )

    def upload(self, payload: Dict[str, Any]) -> None:
        """Upload payload to Azure Blob Storage."""
        container_client = self._client.get_container_client(self.config.container_name)
        try:
            if not container_client.exists():
                container_client.create_container()
        except Exception:
            # Handle potential race conditions or permission issues gracefully
            pass

        blob_name = self.config.blob_name
        container_client.get_blob_client(blob_name).upload_blob(
            json.dumps(payload), overwrite=True
        )

        print(
            f"Payload uploaded to Azure Blob Storage: "
            f"{self.config.container_name}/{blob_name}"
        )


class LocalStorageService(StorageServiceInterface):
    """Storage service for the local file system."""

    def __init__(self, output_dir: str = "output"):
        """Initialize the local storage service."""
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def upload(self, payload: Dict[str, Any]) -> None:
        """Save payload to a local file with a timestamped name."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        file_name = f"{timestamp}_warmtecheck.json"
        file_path = os.path.join(self.output_dir, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"Payload saved to local file: {file_path}")


class MockStorageService(StorageServiceInterface):
    """Mock storage service for testing that does nothing."""

    def __init__(self) -> None:
        """Initialize the mock storage service."""
        self.call_count = 0
        self.last_payload: Dict[str, Any] = {}

    def upload(self, payload: Dict[str, Any]) -> None:
        """Mock upload that tracks calls but performs no I/O."""
        self.call_count += 1
        self.last_payload = payload
        print("MockStorageService: upload called (no action taken).")
