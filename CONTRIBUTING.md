# Contributing to Coercive Control Analysis

Thank you for your interest in contributing to this project! This tool aims to support those affected by coercive control, and we welcome contributions that enhance its capabilities while maintaining the highest standards of privacy and security.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Security Considerations](#security-considerations)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

### Our Commitment

This project exists to support individuals affected by coercive control and domestic violence. We are committed to:

- Maintaining a safe, respectful, and inclusive environment
- Protecting user privacy and data security above all else
- Treating sensitive subject matter with appropriate care and respect
- Supporting survivors and those working to help them

### Expected Behavior

- Be respectful and considerate in all interactions
- Maintain confidentiality of any sensitive information
- Focus on constructive, solution-oriented discussions
- Acknowledge different perspectives and experiences
- Prioritize user safety and privacy in all decisions

### Unacceptable Behavior

- Harassment, discrimination, or disrespectful behavior
- Sharing sensitive or identifying information
- Trivializing abuse or coercive control
- Any behavior that could compromise user safety

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic understanding of domestic violence and coercive control concepts
- Familiarity with privacy and security best practices

### First Contributions

Good first issues are tagged with `good-first-issue` in our issue tracker. These are typically:
- Documentation improvements
- Adding new abuse indicator patterns
- Test coverage improvements
- Bug fixes with clear reproduction steps

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/coercive-control-analysis.git
   cd coercive-control-analysis
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov flake8  # Development dependencies
   ```

4. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Types of Contributions

1. **Bug Reports**: Help us identify and fix issues
2. **Feature Requests**: Suggest new capabilities
3. **Code Contributions**: Implement features or fixes
4. **Documentation**: Improve guides, examples, and API docs
5. **Testing**: Add test coverage or improve test quality
6. **Security**: Report vulnerabilities or improve security

### Contribution Workflow

1. Check existing issues and pull requests to avoid duplication
2. Create an issue to discuss significant changes before starting work
3. Fork the repository and create your feature branch
4. Make your changes following our code standards
5. Add or update tests as needed
6. Update documentation to reflect your changes
7. Submit a pull request with a clear description

## Code Standards

### Python Style Guide

We follow **PEP 8** with the following specifics:

- **Line Length**: Maximum 100 characters (127 for documentation)
- **Indentation**: 4 spaces (no tabs)
- **Naming Conventions**:
  - Functions/variables: `lowercase_with_underscores`
  - Classes: `CapitalizedWords`
  - Constants: `UPPERCASE_WITH_UNDERSCORES`

### Code Quality

```bash
# Run linting
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Format code (optional, but recommended)
# black . --line-length 100
```

### Documentation Standards

- **Docstrings**: All public functions, classes, and modules must have docstrings
- **Format**: Use Google-style docstrings
- **Example**:
  ```python
  def analyze_text(text):
      """
      Analyze text for abuse indicators.
      
      Args:
          text (str): Text to analyze
          
      Returns:
          dict: Dictionary of detected patterns
          
      Raises:
          ValueError: If text is empty
      """
  ```

### Import Organization

```python
# Standard library imports
import os
import sys

# Third-party imports
import click
from cryptography.fernet import Fernet

# Local imports
from config.settings import SETTING_NAME
from parsers.whatsapp_parser import WhatsAppParser
```

## Testing Guidelines

### Test Coverage

- **Minimum Coverage**: 90% for new code
- **Critical Paths**: 100% coverage for security-sensitive code
- **Test Files**: Mirror the structure of source files (e.g., `test_encryption.py` for `encryption.py`)

### Writing Tests

```python
import unittest
from your_module import your_function

class TestYourFunction(unittest.TestCase):
    def test_basic_functionality(self):
        """Test basic use case."""
        result = your_function("input")
        self.assertEqual(result, "expected")
    
    def test_edge_case(self):
        """Test edge case behavior."""
        with self.assertRaises(ValueError):
            your_function("")
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_analyze.py

# Run tests matching pattern
pytest -k "test_encryption"
```

### Test Data

- **Never use real sensitive data** in tests
- Use **mock data** that represents realistic patterns
- Store test fixtures in `tests/fixtures/`
- Document any external test data sources

## Security Considerations

### Critical Security Rules

1. **No Sensitive Data**: Never commit passwords, keys, real names, or personal information
2. **Encryption Keys**: Use environment variables, never hardcode
3. **Input Validation**: Validate and sanitize all user inputs
4. **Dependencies**: Regularly update and audit dependencies
5. **Privacy by Default**: Default to most private/secure settings

### Security Review Checklist

Before submitting code that handles sensitive data:

- [ ] Input is validated and sanitized
- [ ] Errors don't leak sensitive information
- [ ] File permissions are properly set
- [ ] Encryption is used where appropriate
- [ ] No secrets in code or tests
- [ ] Dependencies are up to date
- [ ] SQL injection / path traversal protections in place (if applicable)

### Reporting Security Issues

**Do NOT create public issues for security vulnerabilities.**

Instead:
1. Email security concerns to: cmcheney92@gmail.com
2. Use GitHub's Security Advisory feature
3. See [SECURITY.md](SECURITY.md) for full process

## Pull Request Process

### Before Submitting

1. **Update Documentation**: Ensure README and docstrings are current
2. **Add Tests**: Include tests for new functionality
3. **Run Tests**: Ensure all tests pass
4. **Check Linting**: Code passes flake8 checks
5. **Update CHANGELOG**: Add entry describing your changes
6. **Rebase**: Ensure your branch is up to date with main

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Security improvement

## Testing
Describe testing performed

## Security Considerations
Note any security implications

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings
```

### Review Process

1. **Automated Checks**: CI must pass (tests, linting)
2. **Code Review**: At least one maintainer review required
3. **Security Review**: Required for security-sensitive changes
4. **Documentation Review**: Check for clarity and completeness
5. **Merge**: Squash and merge once approved

## Reporting Bugs

### Before Reporting

1. Check if the issue already exists
2. Verify you're using the latest version
3. Collect relevant information

### Bug Report Template

```markdown
**Describe the Bug**
Clear description of the issue

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. With file '...'
3. See error

**Expected Behavior**
What should happen

**Screenshots/Logs**
If applicable (ensure no sensitive data)

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python Version: [e.g., 3.11]
- Installation Method: [pip/docker]

**Additional Context**
Any other relevant information
```

## Suggesting Enhancements

### Enhancement Template

```markdown
**Feature Description**
Clear description of proposed feature

**Use Case**
Who would benefit and how

**Alternatives Considered**
Other approaches you've thought of

**Implementation Ideas**
Technical approach (if you have one)

**Privacy/Security Impact**
Any privacy or security considerations
```

### Feature Acceptance Criteria

Features should:
- Align with project goals (supporting abuse victims)
- Maintain or improve privacy and security
- Be well-documented and tested
- Not introduce breaking changes (or be worth it)
- Consider resource constraints and performance

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant documentation

## Questions?

- **General Questions**: Open a GitHub Discussion
- **Contribution Help**: Tag issues with `help-wanted`
- **Security Questions**: Email cmcheney92@gmail.com

## License

By contributing, you agree that your contributions will be licensed under the SOLE PROPRIETOR LICENSE located in the SECURITY.md file.

---

Thank you for contributing to this important project!
