"""
Configuration Management Module
Configuration Management Module

Responsible for reading and creating system configuration file config.json
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    """Configuration management class"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration manager
        
        Args:
            config_path: Configuration file path, if None, use config.json in the same directory as main.py
        """
        if config_path is None:
            # Get current file directory (i.e., main.py directory)
            current_dir = Path(__file__).parent
            self.config_path = current_dir / "config.json"
        else:
            self.config_path = Path(config_path)
        
        self.config = self._load_or_create_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        # Get main.py directory as default database path
        main_dir = Path(__file__).parent
        
        return {
            "database": {
                "path": str(main_dir),
                "filename": "profile_data.db"
            },
            "server": {
                "port": 8088,
                "host": "0.0.0.0"
            }
        }
    
    def _load_or_create_config(self) -> Dict[str, Any]:
        """Load or create configuration file"""
        try:
            if self.config_path.exists():
                # Read existing configuration file
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Check and supplement missing configuration items
                default_config = self._get_default_config()
                updated = False
                
                # Check database configuration
                if 'database' not in config:
                    config['database'] = default_config['database']
                    updated = True
                else:
                    if 'path' not in config['database']:
                        config['database']['path'] = default_config['database']['path']
                        updated = True
                    if 'filename' not in config['database']:
                        config['database']['filename'] = default_config['database']['filename']
                        updated = True
                
                # Check server configuration
                if 'server' not in config:
                    config['server'] = default_config['server']
                    updated = True
                else:
                    if 'port' not in config['server']:
                        config['server']['port'] = default_config['server']['port']
                        updated = True
                    if 'host' not in config['server']:
                        config['server']['host'] = default_config['server']['host']
                        updated = True
                
                # Check system configuration
                if 'system' not in config:
                    config['system'] = default_config['system']
                    updated = True
                else:
                    if 'timezone_offset' not in config['system']:
                        config['system']['timezone_offset'] = default_config['system']['timezone_offset']
                        updated = True
                    if 'privacy_level' not in config['system']:
                        config['system']['privacy_level'] = default_config['system']['privacy_level']
                        updated = True
                
                # If updated, save configuration file
                if updated:
                    self._save_config(config)
                
                return config
            else:
                # Create default configuration file
                config = self._get_default_config()
                self._save_config(config)
                print(f"Default configuration file created: {self.config_path}")
                return config
                
        except Exception as e:
            print(f"Configuration file processing error: {e}")
            print("Using default configuration")
            return self._get_default_config()
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to save configuration file: {e}")
    
    def get_database_path(self) -> str:
        """Get complete database path"""
        db_dir = Path(self.config['database']['path'])
        db_filename = self.config['database']['filename']
        return str(db_dir / db_filename)
    
    def get_database_dir(self) -> str:
        """Get database directory path"""
        return self.config['database']['path']
    
    def get_server_port(self) -> int:
        """Get server port"""
        return self.config['server']['port']
    
    def get_server_host(self) -> str:
        """Get server host"""
        return self.config['server']['host']
    
    def get_timezone_offset(self) -> int:
        """Get timezone offset"""
        return self.config['system']['timezone_offset']
    
    def get_privacy_level(self) -> str:
        """Get privacy level"""
        return self.config['system']['privacy_level']
    
    def update_config(self, **kwargs):
        """Update configuration"""
        try:
            # Support nested updates
            for key, value in kwargs.items():
                if '.' in key:
                    # Support nested keys like database.path
                    keys = key.split('.')
                    current = self.config
                    for k in keys[:-1]:
                        if k not in current:
                            current[k] = {}
                        current = current[k]
                    current[keys[-1]] = value
                else:
                    self.config[key] = value
            
            self._save_config(self.config)
            print("Configuration updated")
            
        except Exception as e:
            print(f"Failed to update configuration: {e}")
    
    def get_config(self) -> Dict[str, Any]:
        """Get complete configuration"""
        return self.config.copy()

# Global configuration manager instance
_config_manager = None

def get_config_manager() -> ConfigManager:
    """Get configuration manager instance (singleton pattern)"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager 