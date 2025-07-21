# Str8ZeROCLI Code Generation Automation

This document explains how to use the code generation automation script to add new components to the Str8ZeROCLI project.

## Usage

The automation script helps you:
- Generate new code files in the correct directories
- Automatically create documentation
- Keep the project organized

### Basic Usage

```python
# Import the auto_generate function
from scripts.auto_generate import auto_generate

# Generate a new file
auto_generate(
    module='agents',           # Module category
    filename='my_agent.py',    # File name
    content='# Your code here',# File content
    description='Description for documentation'
)
```

### Available Modules

- `cli`: Core CLI functionality
- `agents`: Custom agent implementations
- `profiles`: User profile templates
- `config`: Configuration files
- `examples`: Example code
- `docs`: Documentation files
- `scripts`: Utility scripts

### Example

To create a new agent:

```bash
python -c "from scripts.auto_generate import auto_generate; auto_generate('agents', 'voice_agent.py', '# Voice agent code', 'Agent for voice processing')"
```

## Documentation

Documentation is automatically generated in the `docs/` directory, with one markdown file per module.