"""
Configuration management utilities
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import tomli
import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    """Application configuration with environment variable support"""

    # API settings
    api_key: Optional[str] = Field(default=None, env="YANZHITI_API_KEY")
    api_base_url: str = Field(default="https://api.example.com", env="YANZHITI_BASE_URL")

    # Model settings
    model: str = Field(default="default-model", env="YANZHITI_MODEL")
    max_tokens: int = Field(default=4096, env="YANZHITI_MAX_TOKENS")
    temperature: float = Field(default=1.0, env="YANZHITI_TEMPERATURE")

    # Execution settings
    timeout: int = Field(default=120, env="YANZHITI_TIMEOUT")
    max_retries: int = Field(default=3, env="YANZHITI_MAX_RETRIES")
    max_turns: int = Field(default=100, env="YANZHITI_MAX_TURNS")

    # UI settings
    verbose: bool = Field(default=False, env="YANZHITI_VERBOSE")
    debug: bool = Field(default=False, env="YANZHITI_DEBUG")
    color: bool = Field(default=True, env="YANZHITI_COLOR")

    # File settings
    max_file_size: int = Field(default=10 * 1024 * 1024, env="YANZHITI_MAX_FILE_SIZE")  # 10MB
    allowed_directories: list[str] = Field(default_factory=list, env="YANZHITI_ALLOWED_DIRS")

    # Permission settings
    permission_mode: str = Field(default="default", env="YANZHITI_PERMISSION_MODE")
    auto_approve: bool = Field(default=False, env="YANZHITI_AUTO_APPROVE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class ConfigManager:
    """Manager for loading and merging configuration from multiple sources"""

    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / ".yanzhiti"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self._config: Optional[AppConfig] = None

    def load(self) -> AppConfig:
        """Load configuration from all sources"""
        if self._config:
            return self._config

        # Start with environment variables (via AppConfig)
        config_dict = {}

        # Load from config files
        config_file = self._find_config_file()
        if config_file:
            file_config = self._load_config_file(config_file)
            config_dict.update(file_config)

        # Create config instance
        self._config = AppConfig(**config_dict)
        return self._config

    def _find_config_file(self) -> Optional[Path]:
        """Find configuration file"""
        # Check current directory
        for name in ["yanzhiti.toml", "yanzhiti.yaml", "yanzhiti.yml", ".yanzhiti.toml"]:
            path = Path.cwd() / name
            if path.exists():
                return path

        # Check config directory
        for name in ["config.toml", "config.yaml", "config.yml"]:
            path = self.config_dir / name
            if path.exists():
                return path

        return None

    def _load_config_file(self, path: Path) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(path, "rb") as f:
                if path.suffix == ".toml":
                    return tomli.load(f)
                else:
                    return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Failed to load config file {path}: {e}")
            return {}

    def save(self, config: Dict[str, Any], format: str = "toml") -> None:
        """Save configuration to file"""
        import tomli_w

        config_file = self.config_dir / f"config.{format}"

        if format == "toml":
            with open(config_file, "wb") as f:
                tomli_w.dump(config, f)
        else:
            with open(config_file, "w") as f:
                yaml.safe_dump(config, f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        config = self.load()
        return getattr(config, key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        if not self._config:
            self.load()

        if hasattr(self._config, key):
            setattr(self._config, key, value)


# Global config manager
_config_manager: Optional[ConfigManager] = None


def get_config() -> AppConfig:
    """Get application configuration"""
    global _config_manager
    if not _config_manager:
        _config_manager = ConfigManager()
    return _config_manager.load()


def get_config_manager() -> ConfigManager:
    """Get configuration manager"""
    global _config_manager
    if not _config_manager:
        _config_manager = ConfigManager()
    return _config_manager
