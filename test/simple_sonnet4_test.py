#!/usr/bin/env python3
import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from generators.phishing_generator import PhishingGenerator

def main():
    generator = PhishingGenerator()

    # Ultra-sophisticated profile for CFO
    profile = {
        'phishing_signs': {
            'spelling_errors': 'high',        # Only 1 subtle error
            'urgency': 'high',               # Subtle professional urgency
            'suspicious_sender': 'high',      # Sophisticated spoofing
            'suspicious_links': 'high',       # Legitimate-looking URLs
            'attachments': 'high'            # Business documents
        },
        'risk_level': 'high',
        'target_info': 'Chief Financial Officer'
    }

    print('=== CLAUDE SONNET 4 - SOPHISTICATED EXECUTIVE PHISHING ===')
    print('Target: Chief Financial Officer')
    print('All difficulty levels: HIGH (most sophisticated)')
    print('\nGenerating content...\n')

    try:
        result = generator.generate_email(profile)

        print('SUCCESS! Generated sophisticated phishing email:')
        print('='*60)

        # Print each field separately to avoid encoding issues
        print(f"From: {result.get('sender_name', 'N/A')} <{result.get('sender_email', 'N/A')}>")
        print(f"Subject: {result.get('subject', 'N/A')}")
        print("\nBody:")
        print(result.get('body', 'N/A'))
        print('='*60)

        return True

    except Exception as e:
        print(f'Error: {e}')
        return False

if __name__ == "__main__":
    main()