#!/usr/bin/env python3
"""
Comprehensive test script for the difficulty level system.
Run this to test different difficulty combinations and see actual generated content.
"""

import sys
import os
import json
from colorama import init, Fore, Style

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from generators.phishing_generator import PhishingGenerator
from api.claude_client import ClaudeAPI

# Initialize colorama for Windows compatibility
init()

def print_header(title):
    """Print a formatted header."""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{title.center(60)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def print_profile(profile):
    """Print profile information nicely."""
    print(f"{Fore.YELLOW}Profile Configuration:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  Risk Level: {profile['risk_level']}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  Target: {profile['target_info']}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  Phishing Signs:{Style.RESET_ALL}")

    if isinstance(profile['phishing_signs'], dict):
        for sign, difficulty in profile['phishing_signs'].items():
            print(f"{Fore.GREEN}    • {sign}: {difficulty}{Style.RESET_ALL}")
    else:
        for sign in profile['phishing_signs']:
            print(f"{Fore.GREEN}    • {sign}{Style.RESET_ALL}")
    print()

def show_prompt_only(profile):
    """Show only the prompt that would be sent to Claude (for testing without API calls)."""
    client = ClaudeAPI()
    prompt = client._build_phishing_prompt(profile)

    print(f"{Fore.MAGENTA}Generated Prompt:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'-'*50}{Style.RESET_ALL}")
    print(prompt)
    print(f"{Fore.WHITE}{'-'*50}{Style.RESET_ALL}")

def print_generated_result(result):
    """Print generated phishing email content nicely."""
    print(f"{Fore.MAGENTA}Generated Content:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'-'*50}{Style.RESET_ALL}")

    if isinstance(result, dict) and 'error' in result:
        print(f"{Fore.RED}Error: {result['error']}{Style.RESET_ALL}")
        return

    if isinstance(result, dict):
        print(f"{Fore.YELLOW}From:{Style.RESET_ALL} {result.get('sender_name', 'N/A')} <{result.get('sender_email', 'N/A')}>")
        print(f"{Fore.YELLOW}Subject:{Style.RESET_ALL} {result.get('subject', 'N/A')}")
        print(f"{Fore.YELLOW}Body:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{result.get('body', 'N/A')}{Style.RESET_ALL}")
    else:
        print(f"{Fore.WHITE}{result}{Style.RESET_ALL}")

    print(f"{Fore.WHITE}{'-'*50}{Style.RESET_ALL}")

def test_difficulty_combinations():
    """Test various difficulty level combinations."""
    generator = PhishingGenerator()

    print_header("TESTING DIFFICULTY LEVEL SYSTEM")

    # Test configurations
    test_configs = [
        {
            "name": "All Low Difficulty (Easy to Detect)",
            "profile": {
                'phishing_signs': {
                    'spelling_errors': 'low',
                    'urgency': 'low',
                    'suspicious_sender': 'low',
                    'generic_greeting': 'low'
                },
                'risk_level': 'low',
                'target_info': 'New Employee Training'
            }
        },
        {
            "name": "All High Difficulty (Sophisticated)",
            "profile": {
                'phishing_signs': {
                    'spelling_errors': 'high',
                    'urgency': 'high',
                    'suspicious_sender': 'high',
                    'suspicious_links': 'high'
                },
                'risk_level': 'high',
                'target_info': 'IT Security Team'
            }
        },
        {
            "name": "Mixed Difficulty Levels",
            "profile": {
                'phishing_signs': {
                    'spelling_errors': 'low',      # Obvious errors
                    'urgency': 'high',             # Subtle urgency
                    'suspicious_sender': 'medium', # Moderately suspicious
                    'attachments': 'high',         # Sophisticated attachments
                    'generic_greeting': 'low'      # Very generic
                },
                'risk_level': 'medium',
                'target_info': 'Finance Department'
            }
        },
        {
            "name": "Executive Target (High Sophistication)",
            "profile": {
                'phishing_signs': {
                    'urgency': 'high',
                    'suspicious_sender': 'high',
                    'suspicious_links': 'high'
                },
                'risk_level': 'high',
                'target_info': 'C-Level Executive'
            }
        },
        {
            "name": "Legacy Format (Backward Compatibility)",
            "profile": {
                'phishing_signs': ['urgency', 'generic_greeting', 'attachments'],
                'risk_level': 'medium',
                'target_info': 'General Employee'
            }
        }
    ]

    for i, config in enumerate(test_configs, 1):
        print(f"{Fore.BLUE}Test {i}: {config['name']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'-'*40}{Style.RESET_ALL}")

        profile = config['profile']
        print_profile(profile)

        try:
            # Validate profile
            is_valid = generator.validate_profile(profile)
            print(f"{Fore.GREEN}[PASS] Validation: Passed{Style.RESET_ALL}")

            # Show the prompt that would be generated
            show_prompt_only(profile)

            # Generate actual content using Claude API
            print(f"{Fore.CYAN}Generating content with Claude API...{Style.RESET_ALL}")
            result = generator.generate_email(profile)
            print_generated_result(result)

        except Exception as e:
            print(f"{Fore.RED}[ERROR] Error: {e}{Style.RESET_ALL}")

        print(f"\n{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")

def test_validation_errors():
    """Test various validation scenarios."""
    print_header("TESTING VALIDATION ERRORS")

    generator = PhishingGenerator()

    error_tests = [
        {
            "name": "Invalid Difficulty Level",
            "profile": {
                'phishing_signs': {'urgency': 'extreme'},
                'risk_level': 'medium',
                'target_info': 'Employee'
            }
        },
        {
            "name": "Invalid Phishing Sign",
            "profile": {
                'phishing_signs': {'fake_sign': 'low'},
                'risk_level': 'medium',
                'target_info': 'Employee'
            }
        },
        {
            "name": "Missing Risk Level",
            "profile": {
                'phishing_signs': {'urgency': 'low'},
                'target_info': 'Employee'
            }
        }
    ]

    for i, test in enumerate(error_tests, 1):
        print(f"{Fore.BLUE}Error Test {i}: {test['name']}{Style.RESET_ALL}")
        try:
            generator.validate_profile(test['profile'])
            print(f"{Fore.RED}[FAIL] Expected error but validation passed{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.GREEN}[PASS] Expected error caught: {e}{Style.RESET_ALL}")
        print()

def show_available_options():
    """Show all available options."""
    print_header("AVAILABLE OPTIONS")

    generator = PhishingGenerator()

    print(f"{Fore.YELLOW}Available Phishing Signs:{Style.RESET_ALL}")
    for sign in generator.get_available_phishing_signs():
        print(f"{Fore.GREEN}  - {sign}{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}Available Difficulty Levels:{Style.RESET_ALL}")
    for level in generator.get_available_difficulty_levels():
        print(f"{Fore.GREEN}  - {level}{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}Difficulty Specifications:{Style.RESET_ALL}")
    specs = generator.get_difficulty_specs()
    for sign, difficulties in specs.items():
        print(f"{Fore.CYAN}  {sign}:{Style.RESET_ALL}")
        for level, desc in difficulties.items():
            print(f"{Fore.WHITE}    {level}: {desc}{Style.RESET_ALL}")
        print()

def main():
    """Main test function."""
    print(f"{Fore.MAGENTA}Phishing Content Generation System - Difficulty Level Testing{Style.RESET_ALL}")
    print(f"{Fore.WHITE}This script tests the new difficulty level system without making API calls.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}To generate actual content, you need to set up the Claude API key and uncomment the generation lines.{Style.RESET_ALL}")

    show_available_options()
    test_difficulty_combinations()
    test_validation_errors()

    print_header("TEST COMPLETE")
    print(f"{Fore.GREEN}All tests completed successfully!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}To generate actual phishing content:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. Set up your Claude API key in .env file{Style.RESET_ALL}")
    print(f"{Fore.WHITE}2. Uncomment the generation lines in this script{Style.RESET_ALL}")
    print(f"{Fore.WHITE}3. Run the script again{Style.RESET_ALL}")

if __name__ == "__main__":
    main()