#!/usr/bin/env python3
"""
Markdown Validation Script

Validates markdown files for:
- Syntax errors
- Style guide compliance
- Link validity
- Content quality issues
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from urllib.parse import urlparse
import urllib.request
import urllib.error

class MarkdownValidator:
    def __init__(self, file_path: str, check_links: bool = True, check_style: bool = True):
        self.file_path = file_path
        self.check_links = check_links
        self.check_style = check_style
        self.issues = []
        self.warnings = []

        with open(file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
            self.lines = self.content.split('\n')

    def validate(self) -> Dict:
        """Run all validation checks"""
        self.check_syntax()

        if self.check_style:
            self.check_style_guide()

        if self.check_links:
            self.check_all_links()

        self.check_content_quality()

        return {
            'file': self.file_path,
            'valid': len(self.issues) == 0,
            'issues': self.issues,
            'warnings': self.warnings
        }

    def check_syntax(self):
        """Check for basic markdown syntax errors"""
        in_code_block = False
        code_block_fence = None

        for i, line in enumerate(self.lines, 1):
            # Check for code block fences
            if line.strip().startswith('```') or line.strip().startswith('~~~'):
                fence = line.strip()[:3]
                if not in_code_block:
                    in_code_block = True
                    code_block_fence = fence
                elif fence == code_block_fence:
                    in_code_block = False
                    code_block_fence = None

            if in_code_block:
                continue

            # Check for unmatched brackets in links
            open_brackets = line.count('[') - line.count(r'\[')
            close_brackets = line.count(']') - line.count(r'\]')
            open_parens = line.count('(') - line.count(r'\(')
            close_parens = line.count(')') - line.count(r'\)')

            if open_brackets != close_brackets:
                self.issues.append({
                    'line': i,
                    'type': 'syntax',
                    'message': f'Unmatched square brackets'
                })

            # Check for incomplete links [text]( without closing paren
            if re.search(r'\[([^\]]+)\]\([^)]*$', line):
                self.issues.append({
                    'line': i,
                    'type': 'syntax',
                    'message': 'Incomplete link syntax'
                })

        # Check if code block is not closed
        if in_code_block:
            self.issues.append({
                'line': len(self.lines),
                'type': 'syntax',
                'message': 'Unclosed code block'
            })

    def check_style_guide(self):
        """Check for style guide compliance"""
        in_code_block = False
        prev_heading_level = 0
        has_h1 = False

        for i, line in enumerate(self.lines, 1):
            # Track code blocks
            if line.strip().startswith('```') or line.strip().startswith('~~~'):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            # Check line length (excluding links)
            line_without_links = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)
            if len(line_without_links) > 120 and not line.strip().startswith('|'):
                self.warnings.append({
                    'line': i,
                    'type': 'style',
                    'message': f'Line exceeds 120 characters ({len(line)} chars)'
                })

            # Check heading hierarchy
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                level = len(heading_match.group(1))
                heading_text = heading_match.group(2)

                if level == 1:
                    has_h1 = True

                # Check for skipped heading levels
                if prev_heading_level > 0 and level > prev_heading_level + 1:
                    self.warnings.append({
                        'line': i,
                        'type': 'style',
                        'message': f'Heading level skipped (h{prev_heading_level} to h{level})'
                    })

                # Check for trailing punctuation in headings
                if heading_text.rstrip().endswith(('.', '!', '?', ':')):
                    self.warnings.append({
                        'line': i,
                        'type': 'style',
                        'message': 'Heading should not end with punctuation'
                    })

                prev_heading_level = level

            # Check for multiple consecutive blank lines
            if i < len(self.lines) and not line.strip():
                next_line = self.lines[i] if i < len(self.lines) else ''
                if not next_line.strip() and i + 1 < len(self.lines):
                    next_next_line = self.lines[i + 1] if i + 1 < len(self.lines) else ''
                    if not next_next_line.strip():
                        self.warnings.append({
                            'line': i,
                            'type': 'style',
                            'message': 'Multiple consecutive blank lines'
                        })

            # Check for trailing whitespace
            if line.endswith(' ') and line.strip():
                self.warnings.append({
                    'line': i,
                    'type': 'style',
                    'message': 'Trailing whitespace'
                })

        # Document should have an H1
        if not has_h1:
            self.warnings.append({
                'line': 1,
                'type': 'style',
                'message': 'Document should have a top-level heading (H1)'
            })

    def check_all_links(self):
        """Check for broken links"""
        # Find all markdown links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'

        for i, line in enumerate(self.lines, 1):
            matches = re.finditer(link_pattern, line)

            for match in matches:
                link_text = match.group(1)
                link_url = match.group(2)

                # Skip anchor links for now
                if link_url.startswith('#'):
                    continue

                # Check internal file links
                if not link_url.startswith(('http://', 'https://', 'mailto:', 'ftp://')):
                    self._check_internal_link(i, link_text, link_url)
                else:
                    # External links - basic URL format check
                    parsed = urlparse(link_url)
                    if not parsed.scheme or not parsed.netloc:
                        self.issues.append({
                            'line': i,
                            'type': 'link',
                            'message': f'Invalid URL format: {link_url}'
                        })

    def _check_internal_link(self, line_num: int, link_text: str, link_path: str):
        """Check if internal file link exists"""
        # Remove anchor from path
        link_path = link_path.split('#')[0]

        if not link_path:
            return

        # Resolve relative path
        base_dir = Path(self.file_path).parent
        target_path = (base_dir / link_path).resolve()

        if not target_path.exists():
            self.issues.append({
                'line': line_num,
                'type': 'link',
                'message': f'Broken link: {link_path} (file not found)'
            })

    def check_content_quality(self):
        """Check for content quality issues"""
        in_code_block = False

        for i, line in enumerate(self.lines, 1):
            # Track code blocks
            if line.strip().startswith('```') or line.strip().startswith('~~~'):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            # Check for images without alt text
            img_pattern = r'!\[\s*\]\([^)]+\)'
            if re.search(img_pattern, line):
                self.warnings.append({
                    'line': i,
                    'type': 'content',
                    'message': 'Image missing alt text'
                })

            # Check for bare URLs (not in links)
            url_pattern = r'(?<!\()(https?://[^\s)]+)(?!\))'
            if re.search(url_pattern, line):
                self.warnings.append({
                    'line': i,
                    'type': 'content',
                    'message': 'Bare URL found - consider using markdown link syntax'
                })

def main():
    parser = argparse.ArgumentParser(description='Validate markdown files')
    parser.add_argument('file', help='Markdown file to validate')
    parser.add_argument('--no-links', action='store_true', help='Skip link validation')
    parser.add_argument('--no-style', action='store_true', help='Skip style checks')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        sys.exit(1)

    validator = MarkdownValidator(
        args.file,
        check_links=not args.no_links,
        check_style=not args.no_style
    )

    result = validator.validate()

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"Validation Results: {result['file']}")
        print(f"{'='*60}\n")

        if result['valid']:
            print("✅ No issues found!")
        else:
            print(f"❌ Found {len(result['issues'])} issue(s)")

            for issue in result['issues']:
                print(f"\nLine {issue['line']} [{issue['type']}]:")
                print(f"  {issue['message']}")

        if result['warnings']:
            print(f"\n⚠️  Found {len(result['warnings'])} warning(s)")

            for warning in result['warnings']:
                print(f"\nLine {warning['line']} [{warning['type']}]:")
                print(f"  {warning['message']}")

        print()

    sys.exit(0 if result['valid'] else 1)

if __name__ == '__main__':
    main()
