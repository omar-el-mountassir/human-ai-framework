# Human-AI Interaction Framework

A robust, ethical, and transparent collaborative framework between human users and AI systems for digital product design and development.

## Overview

The Human-AI Interaction Framework establishes a structured approach for collaboration between humans and AI systems in the context of digital product design and development. It defines roles, responsibilities, ethical principles, communication protocols, feedback mechanisms, and improvement processes to ensure effective and ethical collaboration.

## Features

- **Clear Role Definition**: Defines distinct responsibilities for both human users and AI systems
- **Ethical Guidelines**: Incorporates principles of transparency, accountability, privacy, and fairness
- **Structured Communication**: Establishes protocols for effective human-AI interaction
- **Feedback Mechanisms**: Provides methods for continuous improvement through feedback
- **Modular Architecture**: Designed with a clean, modular structure for extensibility
- **Configuration Management**: Supports different environments through hierarchical configuration
- **Comprehensive Testing**: Includes unit and integration tests for reliability

## Project Structure

```tree
human-ai-framework/
├── config/                  # Configuration files
│   ├── default.yaml         # Default configuration
│   ├── development.yaml     # Development environment configuration
│   ├── production.yaml      # Production environment configuration
│   └── testing.yaml         # Testing environment configuration
├── docs/                    # Documentation
├── src/                     # Source code
│   └── human_ai_framework/  # Main package
│       ├── core/            # Core framework implementation
│       ├── models/          # Data models
│       ├── services/        # Service implementations
│       ├── utils/           # Utility modules
│       ├── api/             # API implementation (if applicable)
│       ├── data/            # Data handling modules
│       ├── __init__.py      # Package initialization
│       ├── __main__.py      # Entry point
│       └── cli.py           # Command-line interface
├── tests/                   # Test suite
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── .env.example             # Example environment variables
├── pyproject.toml           # Project metadata and dependencies
└── README.md                # Project documentation
```

## Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**: This framework requires Python 3.8 or a later version. You can check your Python version by running `python --version` or `python3 --version` in your terminal. If you need to install Python, visit [python.org](https://www.python.org/).
- **`uv` (recommended)**: `uv` is a fast, Rust-written package and project manager. It's recommended for managing dependencies and virtual environments. It replaces tools like `pip`, `pip-tools`, `virtualenv` and more ([uv documentation](https://github.com/astral-sh/uv)). Install `uv` using one of the following methods:

  - **Standalone Installers (macOS, Linux, Windows)**: These installers don't require Rust or Python to be pre-installed.

    ```bash
    # On macOS and Linux.
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # On Windows.
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

  - **Via `pip` or `pipx`**: Use these if you already have Python and `pip` (or `pipx`) installed.

    ```bash
    # With pip.
    pip install uv

    # Or pipx.
    pipx install uv
    ```

- **Alternative: `pip` and `venv`**: If you prefer, you can use the standard Python tools: `pip` for package management and `venv` for creating virtual environments. These are usually included with Python installations.

### Using UV

```bash
# Clone the repository
git clone https://github.com/omar-el-mountassir/human-ai-framework.git
cd human-ai-framework

# Create a virtual environment and install dependencies
uv venv
uv pip install -e .

# For development dependencies
uv pip install -e ".[dev]"

# For documentation dependencies
uv pip install -e ".[docs]"
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/omar-el-mountassir/human-ai-framework.git
cd human-ai-framework

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install -e .

# For development dependencies
pip install -e ".[dev]"

# For documentation dependencies
pip install -e ".[docs]"
```

## Usage

### Command-Line Interface

The framework provides a command-line interface for interactive use:

```bash
# Run the CLI
haif --config config --env development

# With custom log level
haif --config config --env development --log-level DEBUG
```

### Programmatic Usage

```python
from human_ai_framework.core.framework import HumanAIFramework
from human_ai_framework.core.factory import HumanAIFrameworkFactory

# Create a default framework
framework = HumanAIFrameworkFactory.create_default_framework()

# Generate a summary of the framework
summary = framework.generate_framework_summary()
print(summary)

# Create a custom framework
from human_ai_framework.core.framework import (
    Role,
    EthicalPrinciple,
    CommunicationProtocol
)

custom_framework = HumanAIFrameworkFactory.create_custom_framework(
    human_responsibilities=["Define vision and strategy"],
    ai_responsibilities=["Generate insights and recommendations"],
    ethical_principles=[EthicalPrinciple.TRANSPARENCY, EthicalPrinciple.ACCOUNTABILITY]
)
```

## Configuration

The framework supports hierarchical configuration through YAML files and environment variables:

### Configuration Files

- `config/default.yaml`: Default configuration for all environments
- `config/development.yaml`: Development-specific configuration
- `config/production.yaml`: Production-specific configuration
- `config/testing.yaml`: Testing-specific configuration

### Environment Variables

Environment variables can be used to override configuration values. All environment variables should be prefixed with `HAIF_`:

```bash
# Example environment variables
HAIF_ENVIRONMENT=development
HAIF_LOG_LEVEL=INFO
HAIF_LOG_TO_FILE=false
```

## Development

### Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src

# Run specific test file
pytest tests/unit/test_framework.py
```

### Code Quality

```bash
# Run linting
ruff check src tests

# Run type checking
mypy src

# Run formatting
black src tests
```

### Documentation

```bash
# Generate documentation
mkdocs build

# Serve documentation locally
mkdocs serve
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- This framework is designed to promote ethical and effective collaboration between humans and AI systems
- Inspired by best practices in human-computer interaction and AI ethics
