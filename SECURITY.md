# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in AdaptiveMind, please report it responsibly.

### How to Report

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please send an email to the maintainer with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes (optional)

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 7 days
- **Resolution Timeline**: Depends on severity
  - Critical: 24-48 hours
  - High: 7 days
  - Medium: 30 days
  - Low: 90 days

### Disclosure Policy

- We follow responsible disclosure practices
- Security researchers will be credited (unless they prefer anonymity)
- Public disclosure after the fix is released

## Security Best Practices

When using AdaptiveMind:

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use `.env` files (gitignored) for secrets
3. **Network Binding**: Only bind to localhost in development
4. **Audit Logging**: Enable audit logging for production use
5. **Access Control**: Implement proper authentication for exposed endpoints

## Security Features

AdaptiveMind includes:

- ✅ API key enforcement
- ✅ Structured audit logging
- ✅ Privacy-first local architecture
- ✅ Configurable security policies
- ✅ Input validation

## License

This security policy is part of the AdaptiveMind project, licensed under CC-BY 4.0.

---

Copyright © 2025 Jimmy De Jesus (Bravetto)

