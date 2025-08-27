"""Azure authentication utilities using User Assigned Managed Identity (UAMI)."""

import os
import structlog
from azure.identity import ManagedIdentityCredential, DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from typing import Optional

logger = structlog.get_logger()


class AzureAuthManager:
    """Manages Azure authentication using User Assigned Managed Identity."""
    
    def __init__(self, client_id: Optional[str] = None):
        """
        Initialize Azure Auth Manager with UAMI.
        
        Args:
            client_id: User Assigned Managed Identity client ID
        """
        self.client_id = client_id or os.getenv("AZURE_CLIENT_ID")
        self._credential = None
        
    def get_credential(self):
        """Get Azure credential using UAMI or fallback to DefaultAzureCredential."""
        if self._credential is None:
            if self.client_id:
                logger.info("Using User Assigned Managed Identity", client_id=self.client_id)
                self._credential = ManagedIdentityCredential(client_id=self.client_id)
            else:
                logger.info("Using DefaultAzureCredential (fallback)")
                self._credential = DefaultAzureCredential()
        return self._credential
    
    def get_secret_client(self, vault_url: str) -> SecretClient:
        """
        Get Azure Key Vault SecretClient using UAMI.
        
        Args:
            vault_url: Key Vault URL (e.g., https://your-vault.vault.azure.net/)
        """
        credential = self.get_credential()
        return SecretClient(vault_url=vault_url, credential=credential)
    
    async def get_secret(self, vault_url: str, secret_name: str) -> str:
        """
        Retrieve a secret from Azure Key Vault.
        
        Args:
            vault_url: Key Vault URL
            secret_name: Name of the secret to retrieve
        """
        try:
            secret_client = self.get_secret_client(vault_url)
            secret = secret_client.get_secret(secret_name)
            logger.info("Successfully retrieved secret", secret_name=secret_name)
            return secret.value
        except Exception as e:
            logger.error("Failed to retrieve secret", secret_name=secret_name, error=str(e))
            raise
    
    async def get_database_connection_string(self, vault_url: str, secret_name: str = "database-connection-string") -> str:
        """
        Get database connection string from Key Vault.
        
        Args:
            vault_url: Key Vault URL
            secret_name: Secret name containing the database connection string
        """
        return await self.get_secret(vault_url, secret_name)