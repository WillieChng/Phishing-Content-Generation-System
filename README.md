# Phishing Content Generator

A CLI-based phishing content generation system for security awareness training using Claude API.

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Claude API key
```

## Usage

### Generate phishing email:
```bash
python src/main.py generate --signs urgency,generic_greeting --risk high --target "IT Department"
```

### List available phishing signs:
```bash
python src/main.py list-signs
```

### Validate configuration:
```bash
python src/main.py validate-config
```

## Available Phishing Signs

- `spelling_errors` - Include subtle spelling or grammar errors
- `urgency` - Create a sense of urgency or threat
- `suspicious_sender` - Use a suspicious or spoofed sender address
- `generic_greeting` - Use generic greetings like "Dear Customer"
- `suspicious_links` - Include suspicious-looking links
- `attachments` - Reference unexpected attachments

## Project Structure

```
├── src/
│   ├── api/                # Claude API integration
│   ├── generators/         # Phishing content generators
│   ├── config/            # Configuration management
│   └── main.py            # CLI entry point
├── tests/                 # Test files
├── requirements.txt       # Python dependencies
└── setup.py              # Package setup
```