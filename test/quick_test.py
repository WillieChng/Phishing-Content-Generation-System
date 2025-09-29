#!/usr/bin/env python3
"""
Quick test script to test a single API call
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from generators.phishing_generator import PhishingGenerator

def main():
    generator = PhishingGenerator()
    test_profile = {
        'phishing_signs': {
            'spelling_errors': 'low',
            'urgency': 'low',
            'suspicious_sender': 'low',
            'generic_greeting': 'low'
        },
        'risk_level': 'low',
        'target_info': 'New Employee Training'
    }

    print('Testing single generation...')
    try:
        result = generator.generate_email(test_profile)
        print('\n=== SUCCESS ===')
        print('Result:', result)
        return True
    except Exception as e:
        print('\n=== ERROR ===')
        print('Error:', e)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)