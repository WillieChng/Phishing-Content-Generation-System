#!/usr/bin/env python3
"""
Test script for Claude Sonnet 4 with sophisticated phishing scenario
"""

import sys
import os
from colorama import init, Fore, Style

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from generators.phishing_generator import PhishingGenerator

# Initialize colorama for Windows compatibility
init()

def main():
    generator = PhishingGenerator()

    # Ultra-sophisticated executive-level phishing profile
    sophisticated_profile = {
        'phishing_signs': {
            'spelling_errors': 'high',        # Only 1 subtle error
            'urgency': 'high',               # Subtle professional urgency
            'suspicious_sender': 'high',      # Sophisticated spoofing
            'suspicious_links': 'high',       # Legitimate-looking URLs
            'attachments': 'high'            # Business documents with warnings
        },
        'risk_level': 'high',
        'target_info': 'C-Level Executive - Chief Financial Officer'
    }

    print(f"{Fore.CYAN}=== TESTING CLAUDE SONNET 4 ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Profile:{Style.RESET_ALL} Ultra-Sophisticated Executive Target")
    print(f"{Fore.YELLOW}Target:{Style.RESET_ALL} Chief Financial Officer")
    print(f"{Fore.YELLOW}Difficulty:{Style.RESET_ALL} ALL signs set to HIGH (most sophisticated)")

    print(f"\n{Fore.MAGENTA}Expected characteristics:{Style.RESET_ALL}")
    print("• Only 1 subtle spelling/grammar error")
    print("• Professional, subtle urgency language")
    print("• Sophisticated domain spoofing")
    print("• Legitimate-looking URLs")
    print("• Business-appropriate attachments with subtle warnings")

    print(f"\n{Fore.CYAN}Generating content with Claude Sonnet 4...{Style.RESET_ALL}")

    try:
        result = generator.generate_email(sophisticated_profile)

        print(f"\n{Fore.GREEN}=== SUCCESS! GENERATED SOPHISTICATED PHISHING EMAIL ==={Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")

        if isinstance(result, dict):
            print(f"{Fore.YELLOW}From:{Style.RESET_ALL} {result.get('sender_name', 'N/A')} <{result.get('sender_email', 'N/A')}>")
            print(f"{Fore.YELLOW}Subject:{Style.RESET_ALL} {result.get('subject', 'N/A')}")
            print(f"{Fore.YELLOW}Body:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{result.get('body', 'N/A')}{Style.RESET_ALL}")
        else:
            print(f"{Fore.WHITE}{result}{Style.RESET_ALL}")

        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}Analysis:{Style.RESET_ALL}")
        print("✓ Check for subtle spelling errors (should have exactly 1)")
        print("✓ Notice the professional tone with subtle urgency")
        print("✓ Examine sender domain for sophisticated spoofing")
        print("✓ Look for legitimate-looking but suspicious URLs")
        print("✓ Check for business-appropriate attachment references")

        return True

    except Exception as e:
        print(f"\n{Fore.RED}ERROR: {e}{Style.RESET_ALL}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)