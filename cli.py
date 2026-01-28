"""Enhanced CLI for coercive control analysis with Click."""

import click
import sys
from pathlib import Path

from data_processor import DataProcessor
from report_generator import ReportGenerator
from config.settings import DEFAULT_REPORT_FORMAT
from security.anonymization import DataAnonymizer


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Coercive Control Analysis Tool - Analyze documents and conversations for patterns of abuse."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--platform', '-p', 
              type=click.Choice(['whatsapp', 'sms', 'discord', 'telegram', 'generic', 'pdf',
                                'facebook_json', 'facebook_html', 'instagram', 
                                'imessage_txt', 'imessage_csv', 'email', 'mbox']),
              help='Platform type for conversation files (auto-detected if not specified)')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--format', '-f', type=click.Choice(['html', 'json', 'txt']),
              default=DEFAULT_REPORT_FORMAT, help='Report format')
@click.option('--anonymize', is_flag=True, help='Anonymize sensitive information')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def analyze(input_file, platform, output, format, anonymize, verbose):
    """Analyze a single file for coercive control patterns."""
    try:
        if verbose:
            click.echo(f"Analyzing: {input_file}")
            click.echo(f"Platform: {platform or 'auto-detect'}")

        # Process the file
        processor = DataProcessor(input_file)
        results = processor.process(platform=platform)

        # Anonymize if requested
        if anonymize:
            if verbose:
                click.echo("Anonymizing sensitive data...")
            anonymizer = DataAnonymizer()

            # Anonymize conversation data if present
            if results.get('analysis_type') == 'conversation_analysis':
                analysis = results.get('analysis', {})
                abuse_patterns = analysis.get('abuse_patterns', {})
                for category, data in abuse_patterns.items():
                    if 'messages' in data:
                        data['messages'] = anonymizer.anonymize_conversation(data['messages'])

        # Generate report
        if verbose:
            click.echo("Generating report...")

        report_gen = ReportGenerator()
        report_path = report_gen.generate_report(results, format=format, output_filename=output)

        click.echo(f"✓ Analysis complete!")
        click.echo(f"Report saved to: {report_path}")

        # Print summary
        if results.get('analysis_type') == 'conversation_analysis':
            analysis = results.get('analysis', {})
            freq = analysis.get('frequency_patterns', {})
            abuse = analysis.get('abuse_patterns', {})
            darvo = analysis.get('darvo_tactics', {})

            click.echo("\nSummary:")
            click.echo("  Messages: {}".format(freq.get('total_messages', 0)))
            click.echo("  Abuse patterns detected: {}".format(len(abuse)))

            if analysis.get('escalation_patterns', {}).get('escalation_detected'):
                click.secho("  ⚠ ESCALATION DETECTED", fg='red', bold=True)
            
            # DARVO summary
            if darvo:
                severity = darvo.get('severity_assessment', {})
                forensic = darvo.get('forensic_summary', {})
                
                if forensic.get('full_darvo_pattern_detected'):
                    click.secho("  ⚠ COMPLETE DARVO PATTERN DETECTED", fg='red', bold=True)
                
                if severity:
                    risk_level = severity.get('risk_level', 'unknown')
                    click.echo(f"  DARVO Risk Level: {risk_level.upper()}")
                    
                    if risk_level in ['critical', 'high']:
                        click.secho(f"    Severity Score: {severity.get('total_score', 0)}", fg='red')
                    else:
                        click.echo(f"    Severity Score: {severity.get('total_score', 0)}")
                
                if forensic.get('high_risk_indicators'):
                    click.secho("  🚨 HIGH RISK: Child-focused manipulation detected", fg='red', bold=True)

        elif results.get('analysis_type') == 'document_analysis':
            abuse = results.get('abuse_patterns', {})
            click.echo("\nSummary:")
            click.echo("  Pages: {}".format(results.get('total_pages', 0)))
            click.echo("  Abuse pattern categories: {}".format(len(abuse)))

    except Exception as e:
        click.secho(f"Error: {e}", fg='red', err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_files', nargs=-1, type=click.Path(exists=True), required=True)
@click.option('--output-dir', '-o', type=click.Path(), default='output',
              help='Output directory for reports')
@click.option('--format', '-f', type=click.Choice(['html', 'json', 'txt']),
              default=DEFAULT_REPORT_FORMAT, help='Report format')
@click.option('--anonymize', is_flag=True, help='Anonymize sensitive information')
def batch(input_files, output_dir, format, anonymize):
    """Analyze multiple files in batch mode."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    click.echo(f"Processing {len(input_files)} files...")

    results = []
    for i, filepath in enumerate(input_files, 1):
        try:
            click.echo(f"[{i}/{len(input_files)}] Processing: {filepath}")

            processor = DataProcessor(filepath)
            result = processor.process()

            # Anonymize if requested
            if anonymize:
                anonymizer = DataAnonymizer()
                if result.get('analysis_type') == 'conversation_analysis':
                    analysis = result.get('analysis', {})
                    abuse_patterns = analysis.get('abuse_patterns', {})
                    for category, data in abuse_patterns.items():
                        if 'messages' in data:
                            data['messages'] = anonymizer.anonymize_conversation(data['messages'])

            # Generate report
            report_gen = ReportGenerator(str(output_path))
            filename = f"report_{Path(filepath).stem}.{format}"
            report_path = report_gen.generate_report(result, format=format, output_filename=filename)

            results.append({
                'file': filepath,
                'report': report_path,
                'success': True
            })

            click.echo(f"  ✓ Report saved: {report_path}")

        except Exception as e:
            click.secho(f"  ✗ Error: {e}", fg='red')
            results.append({
                'file': filepath,
                'error': str(e),
                'success': False
            })

    # Summary
    successful = sum(1 for r in results if r['success'])
    click.echo("\nBatch processing complete!")
    click.echo("Successful: {}/{}".format(successful, len(input_files)))


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--password', prompt=True, hide_input=True, help='Encryption password')
def encrypt(input_file, output_file, password):
    """Encrypt a file with a password."""
    try:
        from security.encryption import DataEncryptor

        # Generate key from password
        key, salt = DataEncryptor.generate_key_from_password(password)

        # Create encryptor
        encryptor = DataEncryptor(key)

        # Encrypt file
        encryptor.encrypt_file(input_file, output_file)

        # Save salt (needed for decryption)
        salt_file = Path(output_file).with_suffix('.salt')
        with open(salt_file, 'wb') as f:
            f.write(salt)

        click.echo(f"✓ File encrypted: {output_file}")
        click.echo(f"✓ Salt saved: {salt_file}")
        click.echo("Keep the salt file safe - it's needed for decryption!")

    except Exception as e:
        click.secho(f"Error: {e}", fg='red', err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--password', prompt=True, hide_input=True, help='Decryption password')
@click.option('--salt-file', type=click.Path(exists=True), help='Salt file (auto-detected if not specified)')
def decrypt(input_file, output_file, password, salt_file):
    """Decrypt a file with a password."""
    try:
        from security.encryption import DataEncryptor

        # Auto-detect salt file if not specified
        if not salt_file:
            salt_file = Path(input_file).with_suffix('.salt')
            if not salt_file.exists():
                raise ValueError("Salt file not found. Please specify with --salt-file")

        # Load salt
        with open(salt_file, 'rb') as f:
            salt = f.read()

        # Generate key from password
        key, _ = DataEncryptor.generate_key_from_password(password, salt)

        # Create encryptor
        encryptor = DataEncryptor(key)

        # Decrypt file
        encryptor.decrypt_file(input_file, output_file)

        click.echo(f"✓ File decrypted: {output_file}")

    except Exception as e:
        click.secho(f"Error: {e}", fg='red', err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file')
def anonymize_file(input_file, output):
    """Anonymize sensitive information in a text file."""
    try:
        from security.anonymization import DataAnonymizer

        # Read file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Anonymize
        anonymizer = DataAnonymizer()
        anonymized = anonymizer.anonymize_text(content)

        # Determine output path
        if not output:
            output = Path(input_file).with_suffix('.anonymized.txt')

        # Write anonymized content
        with open(output, 'w', encoding='utf-8') as f:
            f.write(anonymized)

        click.echo(f"✓ Anonymized file saved: {output}")

        # Show mapping summary
        mapping = anonymizer.get_replacement_mapping()
        total_replacements = sum(len(m) for m in mapping.values())
        click.echo(f"Total replacements made: {total_replacements}")

    except Exception as e:
        click.secho(f"Error: {e}", fg='red', err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
