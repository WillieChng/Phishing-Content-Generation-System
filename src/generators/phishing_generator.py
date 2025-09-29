import json
import logging
from typing import Dict, List, Any, Optional
from api.claude_client import ClaudeAPI

logger = logging.getLogger(__name__)

class PhishingGenerator:
    """Main phishing content generator class."""

    PHISHING_SIGNS = [
        'spelling_errors',
        'urgency',
        'suspicious_sender',
        'generic_greeting',
        'suspicious_links',
        'attachments'
    ]

    DIFFICULTY_LEVELS = ['low', 'medium', 'high']

    # Difficulty level descriptions for each phishing sign
    SIGN_DIFFICULTY_SPECS = {
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

    def __init__(self):
        self.claude_api = ClaudeAPI()

    def validate_profile(self, profile: Dict[str, Any]) -> bool:
        """Validate the phishing profile."""
        if 'phishing_signs' not in profile:
            raise ValueError('phishing_signs is required')

        if 'risk_level' not in profile:
            raise ValueError('risk_level is required')

        # Validate phishing signs - can be list or dict with difficulty levels
        phishing_signs = profile['phishing_signs']

        if isinstance(phishing_signs, list):
            # Legacy format: list of sign names
            for sign in phishing_signs:
                if sign not in self.PHISHING_SIGNS:
                    raise ValueError(f'Invalid phishing sign: {sign}. Valid options: {", ".join(self.PHISHING_SIGNS)}')
        elif isinstance(phishing_signs, dict):
            # New format: dict with sign names and difficulty levels
            for sign, difficulty in phishing_signs.items():
                if sign not in self.PHISHING_SIGNS:
                    raise ValueError(f'Invalid phishing sign: {sign}. Valid options: {", ".join(self.PHISHING_SIGNS)}')
                if difficulty not in self.DIFFICULTY_LEVELS:
                    raise ValueError(f'Invalid difficulty level: {difficulty}. Valid options: {", ".join(self.DIFFICULTY_LEVELS)}')
        else:
            raise ValueError('phishing_signs must be a list or dict')

        return True

    def generate_email(self, profile: Dict[str, Any]) -> Dict[str, str]:
        """Generate a phishing email based on the profile."""
        self.validate_profile(profile)

        try:
            content = self.claude_api.generate_phishing_content(profile)
            return self._parse_generated_content(content)
        except Exception as error:
            logger.error(f'Error generating phishing email: {error}')
            raise error

    def _parse_generated_content(self, content: str) -> Dict[str, str]:
        """Parse the generated content from Claude API."""
        try:
            # Try to extract JSON from the response
            if '{' in content and '}' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                json_str = content[start:end]
                parsed = json.loads(json_str)

                # Normalize keys to match expected format
                normalized = {}
                key_mappings = {
                    'sender_email': 'sender_email',
                    'senderEmail': 'sender_email',
                    'sender_name': 'sender_name',
                    'senderName': 'sender_name',
                    'subject': 'subject',
                    'body': 'body'
                }

                for key, value in parsed.items():
                    normalized_key = key_mappings.get(key, key)
                    normalized[normalized_key] = value

                return normalized

            # Fallback parsing if JSON is not found
            return self._fallback_parse(content)

        except json.JSONDecodeError as error:
            logger.error(f'Error parsing generated content: {error}')
            return self._fallback_parse(content)

    def _fallback_parse(self, content: str) -> Dict[str, str]:
        """Fallback parsing method."""
        return {
            'sender_email': 'phishing@example.com',
            'sender_name': 'System Administrator',
            'subject': 'Action Required - Account Verification',
            'body': content
        }

    def get_available_phishing_signs(self) -> List[str]:
        """Get list of available phishing signs."""
        return self.PHISHING_SIGNS.copy()

    def create_default_profile(
        self,
        signs: Optional[List[str]] = None,
        risk_level: str = 'medium',
        target_info: str = 'General employee',
        use_difficulty_levels: bool = False,
        default_difficulty: str = 'medium'
    ) -> Dict[str, Any]:
        """Create a default phishing profile."""
        if signs is None or len(signs) == 0:
            signs = ['urgency', 'generic_greeting']

        if use_difficulty_levels:
            # Create dict format with difficulty levels
            phishing_signs = {sign: default_difficulty for sign in signs}
        else:
            # Legacy list format
            phishing_signs = signs

        return {
            'phishing_signs': phishing_signs,
            'risk_level': risk_level,
            'target_info': target_info
        }

    def get_difficulty_specs(self) -> Dict[str, Dict[str, str]]:
        """Get difficulty specifications for all phishing signs."""
        return self.SIGN_DIFFICULTY_SPECS.copy()

    def get_available_difficulty_levels(self) -> List[str]:
        """Get list of available difficulty levels."""
        return self.DIFFICULTY_LEVELS.copy()