"""
Configuration Manager for Text Morph
Handles loading and accessing configuration from config.yaml
"""

import yaml
import os
from pathlib import Path
from typing import Any, Dict, Optional
from exceptions import ConfigurationError


class ConfigManager:
    """Manages application configuration from YAML file."""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one config instance."""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration YAML file
        """
        if self._config is None:
            self.config_path = config_path
            self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        try:
            config_file = Path(self.config_path)
            
            if not config_file.exists():
                raise ConfigurationError(
                    f"Configuration file not found: {self.config_path}"
                )
            
            with open(config_file, 'r', encoding='utf-8') as file:
                self._config = yaml.safe_load(file)
            
            if self._config is None:
                raise ConfigurationError("Configuration file is empty")
                
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Error parsing YAML config: {str(e)}")
        except Exception as e:
            raise ConfigurationError(f"Error loading configuration: {str(e)}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to config value (e.g., 'api.huggingface.timeout')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
            
        Example:
            config.get('api.huggingface.timeout')
            config.get('summarization.extractive.short.max_length')
        """
        keys = key_path.split('.')
        value = self._config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_app_config(self) -> Dict[str, Any]:
        """Get application configuration."""
        return self.get('app', {})
    
    def get_api_config(self, service: str) -> Dict[str, Any]:
        """
        Get API configuration for specific service.
        
        Args:
            service: 'huggingface' or 'groq'
        """
        return self.get(f'api.{service}', {})
    
    def get_summarization_params(self, method: str, length: str) -> Dict[str, Any]:
        """
        Get summarization parameters.
        
        Args:
            method: 'extractive' or 'abstractive'
            length: 'short', 'medium', or 'long'
        """
        return self.get(f'summarization.{method}.{length}', {})
    
    def get_paraphrasing_params(self) -> Dict[str, Any]:
        """Get paraphrasing parameters."""
        return self.get('paraphrasing', {})
    
    def get_limits(self) -> Dict[str, int]:
        """Get text processing limits."""
        return self.get('limits', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self.get('logging', {})
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Get theme color configuration."""
        return self.get('theme.colors', {})
    
    def get_error_message(self, error_type: str, **kwargs) -> str:
        """
        Get formatted error message.
        
        Args:
            error_type: Type of error message
            **kwargs: Values to format into message
        """
        message = self.get(f'error_messages.{error_type}', 'An error occurred')
        try:
            return message.format(**kwargs)
        except KeyError:
            return message
    
    def get_success_message(self, message_type: str, **kwargs) -> str:
        """
        Get formatted success message.
        
        Args:
            message_type: Type of success message
            **kwargs: Values to format into message
        """
        message = self.get(f'success_messages.{message_type}', 'Success!')
        try:
            return message.format(**kwargs)
        except KeyError:
            return message
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """
        Check if a feature is enabled.
        
        Args:
            feature_name: Name of the feature (e.g., 'enable_extractive')
        """
        return self.get(f'features.{feature_name}', False)
    
    def get_cache_config(self) -> Dict[str, Any]:
        """Get cache configuration."""
        return self.get('cache', {})
    
    def get_export_config(self) -> Dict[str, Any]:
        """Get export configuration."""
        return self.get('export', {})
    
    def get_performance_config(self) -> Dict[str, Any]:
        """Get performance configuration."""
        return self.get('performance', {})
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._config = None
        self._load_config()
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get entire configuration dictionary."""
        return self._config
    
    def validate_config(self) -> bool:
        """
        Validate that all required configuration keys exist.
        
        Returns:
            True if valid, raises ConfigurationError otherwise
        """
        required_keys = [
            'app',
            'api.huggingface',
            'api.groq',
            'summarization',
            'paraphrasing',
            'limits',
            'logging'
        ]
        
        for key in required_keys:
            if self.get(key) is None:
                raise ConfigurationError(f"Required configuration key missing: {key}")
        
        return True
    
    def __repr__(self) -> str:
        """String representation of ConfigManager."""
        return f"ConfigManager(config_path='{self.config_path}')"


# Create global config instance
config = ConfigManager()


# Convenience functions for common config access
def get_app_name() -> str:
    """Get application name."""
    return config.get('app.name', 'Text Morph')


def get_app_version() -> str:
    """Get application version."""
    return config.get('app.version', '1.0.0')


def get_hf_model() -> str:
    """Get Hugging Face model name."""
    return config.get('api.huggingface.model_name', 'facebook/bart-large-cnn')


def get_groq_model() -> str:
    """Get GROQ model name."""
    return config.get('api.groq.model_name', 'llama-3.1-8b-instant')


def get_timeout(service: str) -> int:
    """Get API timeout for service."""
    return config.get(f'api.{service}.timeout', 60)


def get_max_input_length() -> int:
    """Get maximum input length."""
    return config.get('limits.max_input_length', 10000)


def is_logging_enabled() -> bool:
    """Check if file logging is enabled."""
    return config.get('logging.file.enabled', True)


if __name__ == "__main__":
    # Test configuration loading
    try:
        print(f"App Name: {get_app_name()}")
        print(f"Version: {get_app_version()}")
        print(f"HF Model: {get_hf_model()}")
        print(f"GROQ Model: {get_groq_model()}")
        print(f"Max Input Length: {get_max_input_length()}")
        print("\nConfiguration loaded successfully!")
    except ConfigurationError as e:
        print(f"Configuration Error: {e}")