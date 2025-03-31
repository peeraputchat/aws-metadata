# AWS Instance Metadata Query Tool

A lightweight Python utility to fetch and display AWS EC2 instance metadata with JSON support.

## Features

- 🔥 Simple key-based metadata access
- 📄 JSON-formatted output
- ⚡ Fast with 2-second timeout
- 📋 List all available metadata keys
- 🔄 Dynamic instance identity document support

📋 Basic Commands
| Command | What It Does | Example |
|---------|--------------|---------|
| `-k` | Get specific metadata | `-k instance-id` |
| `-l` | List all available keys | `-l` |
| `-d` | Show all details (JSON) | `-d` |

## 🚀 Quick Start
```bash
python aws_metadata.py -k instance-id
