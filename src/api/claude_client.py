import json
import logging
from typing import Dict, List, Optional, Any
from anthropic import Anthropic
from config.settings import load_config

logger = logging.getLogger(__name__)

class ClaudeAPI:
    """Claude API client for generating phishing content."""

    def __init__(self):
        self.config = load_config()
        self.client = Anthropic(
            api_key=self.config.claude.api_key
        )

    async def generate_content(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Generate content using Claude API."""
        if options is None:
            options = {}

        try:
            message = self.client.messages.create(
                model=self.config.claude.model,
                max_tokens=options.get('max_tokens', 1000),
                temperature=options.get('temperature', 0.7),
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return message.content[0].text

        except Exception as error:
            logger.error(f"Claude API Error: {error}")
            raise Exception(f"Failed to generate content: {str(error)}")

    def generate_phishing_content(self, phishing_profile: Dict[str, Any]) -> str:
        """Generate phishing content based on profile."""
        prompt = self._build_phishing_prompt(phishing_profile)
        try:
            # Use synchronous call for simplicity
            message = self.client.messages.create(
                model=self.config.claude.model,
                max_tokens=1000,
                temperature=0.8,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return message.content[0].text

        except Exception as error:
            logger.error(f"Claude API Error: {error}")
            raise Exception(f"Failed to generate phishing content: {str(error)}")

    def _build_phishing_prompt(self, profile: Dict[str, Any]) -> str:
        """Build the prompt for phishing content generation."""
        phishing_signs = profile.get('phishing_signs', [])
        target_info = profile.get('target_info', 'General employee')

        prompt = f"""Generate a phishing email for security awareness training purposes only. This is for defensive security education.

Target Context: {target_info}

Include the following phishing signs with specific difficulty levels:"""

        # Handle both legacy list format and new dict format
        if isinstance(phishing_signs, dict):
            # New format with difficulty levels
            difficulty_specs = self._get_difficulty_specs()
            for sign, difficulty in phishing_signs.items():
                if sign in difficulty_specs and difficulty in difficulty_specs[sign]:
                    spec = difficulty_specs[sign][difficulty]
                    prompt += f'\n- {sign.replace("_", " ").title()} ({difficulty} difficulty): {spec}'
        else:
            # Legacy list format - use default descriptions
            if 'spelling_errors' in phishing_signs:
                prompt += '\n- Include subtle spelling or grammar errors'
            if 'urgency' in phishing_signs:
                prompt += '\n- Create a sense of urgency or threat'
            if 'suspicious_sender' in phishing_signs:
                prompt += '\n- Use a suspicious or spoofed sender address'
            if 'generic_greeting' in phishing_signs:
                prompt += '\n- Use generic greetings like "Dear Customer"'
            if 'suspicious_links' in phishing_signs:
                prompt += '\n- Include suspicious-looking links (use example.com for safety)'
            if 'attachments' in phishing_signs:
                prompt += '\n- Reference unexpected attachments'

        prompt += """\n\nGenerate JSON with:
{
  "sender_email": "sender email address",
  "sender_name": "sender display name",
  "subject": "email subject",
  "body": "email body content"
}

Make it realistic but clearly identifiable as a phishing attempt for training purposes."""

        return prompt

    def _get_difficulty_specs(self) -> Dict[str, Dict[str, str]]:
        """Get difficulty specifications for phishing signs."""
        return {
            'spelling_errors': {
                'low': 'Obvious spelling/grammar errors (3-5 errors)',
                'medium': 'Moderate spelling/grammar errors (1-2 errors)',
                'high': 'Subtle typos or minor grammar issues (1 error)'
            },
            'urgency': {
                'low': 'Extreme urgency with threatening language and deadlines',
                'medium': 'Moderate urgency with time pressure',
                'high': 'Subtle urgency using professional language'
            },
            'suspicious_sender': {
                'low': 'Obviously fake sender (random characters, misspelled domains)',
                'medium': 'Suspicious but plausible sender (slight domain variations)',
                'high': 'Sophisticated spoofing (legitimate-looking but incorrect domain)'
            },
            'generic_greeting': {
                'low': 'Very generic ("Dear Customer", "Dear User")',
                'medium': 'Semi-generic with partial personalization',
                'high': 'Generic but professional sounding greeting'
            },
            'suspicious_links': {
                'low': 'Obviously suspicious URLs (random characters, wrong domains)',
                'medium': 'Suspicious but convincing URLs (slight misspellings)',
                'high': 'Sophisticated URL spoofing (legitimate-looking domains)'
            },
            'attachments': {
                'low': 'Unexpected executable files (.exe, .scr)',
                'medium': 'Suspicious document files (.doc, .pdf)',
                'high': 'Legitimate-looking business documents with subtle warnings'
            }
        }