# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are currently being supported with security updates. 

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | : white_check_mark:  |
| < 1.0   | :x:                 |

## Reporting a Vulnerability

We take the security of our project seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods: 

- **Email**:  Send an email to cmcheney92@gmail.com with the subject line "Security Vulnerability Report"
- **GitHub Security Advisory**: Use GitHub's private vulnerability reporting feature by going to the "Security" tab of this repository and clicking "Report a vulnerability"

### What to Include

Please include the following information in your report:

- **Description**: A clear description of the vulnerability
- **Steps to Reproduce**:  Detailed steps to reproduce the issue
- **Impact**:  Your assessment of the potential impact
- **Affected Components**: Which parts of the codebase are affected
- **Proposed Solution**: If you have ideas for how to fix it (optional)
- **Your Contact Information**: So we can follow up with questions

### Response Timeline

- **Initial Response**: We will acknowledge receipt of your vulnerability report within 48 hours
- **Status Updates**: We will provide regular updates on our progress every 7 days
- **Resolution**: We aim to resolve critical vulnerabilities within 30 days

### Our Commitment

- We will respond to your report promptly and keep you updated throughout the process
- We will credit you for the discovery (unless you prefer to remain anonymous)
- We will not take legal action against researchers who follow this disclosure process
- We will work with you to understand and resolve the issue quickly

## Security Best Practices

If you're contributing to this project, please follow these security guidelines:

### Data Handling
- Never commit sensitive data (API keys, passwords, personal information) to the repository
- Use environment variables for configuration secrets
- Sanitize all user inputs, especially when dealing with sensitive research data

### Dependencies
- Regularly update dependencies to patch known vulnerabilities
- Review new dependencies for security issues before adding them
- Use tools like `npm audit` or `pip-audit` to scan for vulnerabilities

### Code Review
- All code changes must be reviewed before merging
- Pay special attention to data processing and analysis functions
- Validate input parameters and handle edge cases securely

## Scope

This security policy applies to: 
- The main application code
- Data processing scripts
- Documentation and configuration files
- Any deployment or infrastructure code

### Out of Scope
- Third-party dependencies (please report directly to those projects)
- Issues in development/testing environments
- Social engineering attacks

## Recognition

We appreciate the efforts of security researchers and will acknowledge contributors who help improve our project's security.  With your permission, we will:

- Add your name to our security contributors list
- Mention your contribution in release notes
- Provide a reference letter if requested

## Questions? 

If you have questions about this security policy, please create a public issue in this repository or contact us at cmcheney92@gmail.com. 

---

**Last Updated**: 01/11/2026
**Policy Version**: 1.0
