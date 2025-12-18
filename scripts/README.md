# AdaptiveMind Scripts Directory

This directory contains organized scripts for development, testing, and demonstration purposes.

## Directory Structure

### `/demo/` - Demonstration Scripts
- `simple_demo.py` - Simple standalone HTTP server for AdaptiveMind demonstration
- `working_demo.py` - Enhanced demonstration script with additional features

### `/debug/` - Debug and Development Scripts
- `debug_chat.py` - Chat debugging utilities
- `debug_config.py` - Configuration debugging utilities
- `debug_ollama.py` - Ollama backend debugging utilities

### `/server/` - Server Management Scripts
- `start_fixed_server.py` - Server startup script with fixed configuration

## Usage

### Running Demos
```bash
# Simple demo server
python scripts/demo/simple_demo.py

# Enhanced demo
python scripts/demo/working_demo.py
```

### Debugging
```bash
# Debug chat functionality
python scripts/debug/debug_chat.py

# Debug configuration
python scripts/debug/debug_config.py

# Debug Ollama integration
python scripts/debug/debug_ollama.py
```

### Server Management
```bash
# Start fixed server
python scripts/server/start_fixed_server.py
```

## Notes

- All scripts have been organized from the root directory into logical categories
- Scripts maintain their original functionality and command-line interfaces
- This organization improves code maintainability and developer experience

## Migration

If you have scripts that reference the old locations, update imports:
- `simple_demo.py` → `scripts/demo/simple_demo.py`
- `debug_chat.py` → `scripts/debug/debug_chat.py`
- `start_fixed_server.py` → `scripts/server/start_fixed_server.py`

## Consolidation Progress

**Current Progress: 10/10 items completed (100%)**

- [x] Analyze server implementation consolidation needs
- [x] Identify duplicate handler classes and demo code
- [x] Plan core module hierarchy unification
- [x] Create consolidated server implementation
- [x] Remove deprecated/experimental files
- [x] Restructure demo and test code organization
- [x] Fix imports in all moved scripts
- [x] Consolidate configuration management patterns
- [x] Clean up imports and dependencies
- [x] Update documentation for new structure
- [x] Validate consolidation doesn't break functionality

## Summary of Changes

### Removed Files
- `adaptivemind_core/server_enhanced.py` - Broken implementation with syntax errors
- `adaptivemind_core/app_broken2.py` - Experimental/obsolete implementation
- `jarvis_core/config.py` - Duplicate configuration file
- Root-level scattered scripts moved to organized structure

### Moved Files
- `simple_demo.py` → `scripts/demo/simple_demo.py`
- `working_demo.py` → `scripts/demo/working_demo.py`
- `debug_chat.py` → `scripts/debug/debug_chat.py`
- `debug_config.py` → `scripts/debug/debug_config.py`
- `debug_ollama.py` → `scripts/debug/debug_ollama.py`
- `start_fixed_server.py` → `scripts/server/start_fixed_server.py`

### Updated Files
- `jarvis_core/minimal_server.py` - Updated imports to use consolidated config
- `README.md` - Updated to reflect new structure
- All moved scripts - Fixed imports and path handling for new locations
