#!/usr/bin/env python3

import sys
import os
import logging
import click
from colorama import init, Fore, Style

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from generators.phishing_generator import PhishingGenerator
from config.settings import validate_config

# Initialize colorama for Windows compatibility
init()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.group()
@click.version_option("1.0.0")
def cli():
    """Phishing content generation system for awareness training."""
    pass

@cli.command()
@click.option(
    '--signs', '-s',
    help='Comma-separated list of phishing signs to include',
    default='urgency,generic_greeting'
)
@click.option(
    '--risk', '-r',
    type=click.Choice(['low', 'medium', 'high']),
    default='medium',
    help='Risk level (low, medium, high)'
)
@click.option(
    '--target', '-t',
    default='General employee',
    help='Target information/context'
)
def generate(signs, risk, target):
    """Generate phishing email content."""
    try:
        # Validate configuration
        validate_config()

        generator = PhishingGenerator()

        # Parse phishing signs
        phishing_signs = [s.strip() for s in signs.split(',')]

        profile = {
            'phishing_signs': phishing_signs,
            'risk_level': risk,
            'target_info': target
        }

        click.echo(f"{Fore.BLUE}[GENERATING] Phishing email...{Style.RESET_ALL}")
        click.echo(f"{Fore.WHITE}Signs: {', '.join(phishing_signs)}{Style.RESET_ALL}")
        click.echo(f"{Fore.WHITE}Risk Level: {risk}{Style.RESET_ALL}")
        click.echo(f"{Fore.WHITE}Target: {target}{Style.RESET_ALL}")
        click.echo()

        result = generator.generate_email(profile)

        click.echo(f"{Fore.GREEN}[SUCCESS] Generated phishing email:{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}{'━' * 50}{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}From:{Style.RESET_ALL} {result.get('sender_name', 'Unknown')} <{result.get('sender_email', 'unknown@example.com')}>")
        click.echo(f"{Fore.CYAN}Subject:{Style.RESET_ALL} {result.get('subject', 'No Subject')}")
        click.echo(f"{Fore.YELLOW}{'━' * 50}{Style.RESET_ALL}")
        click.echo(result.get('body', 'No content generated'))
        click.echo(f"{Fore.YELLOW}{'━' * 50}{Style.RESET_ALL}")

    except Exception as error:
        click.echo(f"{Fore.RED}[ERROR] {str(error)}{Style.RESET_ALL}")
        sys.exit(1)

@cli.command('list-signs')
def list_signs():
    """List available phishing signs."""
    generator = PhishingGenerator()
    signs = generator.get_available_phishing_signs()

    click.echo(f"{Fore.BLUE}Available phishing signs:{Style.RESET_ALL}")
    for sign in signs:
        click.echo(f"{Fore.GREEN}• {sign}{Style.RESET_ALL}")

@cli.command('validate-config')
def validate_config_cmd():
    """Validate configuration."""
    try:
        validate_config()
        click.echo(f"{Fore.GREEN}[OK] Configuration is valid{Style.RESET_ALL}")
    except Exception as error:
        click.echo(f"{Fore.RED}[ERROR] Configuration error: {str(error)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == '__main__':
    cli()