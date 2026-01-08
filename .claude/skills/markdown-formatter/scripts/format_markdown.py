#!/usr/bin/env python3
"""
Markdown Formatting Script

Formats markdown files according to best practices:
- Consistent heading spacing
- Proper list formatting
- Table alignment
- Consistent code block formatting
- Removes trailing whitespace
- Standardizes line breaks
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List

class MarkdownFormatter:
    def __init__(self, content: str):
        self.lines = content.split('\n')
        self.formatted_lines = []
        self.in_code_block = False
        self.in_table = False
        self.code_block_indent = 0

    def format(self) -> str:
        """Format the markdown content"""
        i = 0
        while i < len(self.lines):
            line = self.lines[i]
            i = self._process_line(line, i)

        # Remove multiple consecutive blank lines
        self._normalize_blank_lines()

        # Ensure single newline at end of file
        while self.formatted_lines and not self.formatted_lines[-1].strip():
            self.formatted_lines.pop()
        self.formatted_lines.append('')

        return '\n'.join(self.formatted_lines)

    def _process_line(self, line: str, index: int) -> int:
        """Process a single line and return next index"""
        # Check for code block toggle
        if line.strip().startswith('```') or line.strip().startswith('~~~'):
            self.in_code_block = not self.in_code_block
            if self.in_code_block:
                self.code_block_indent = len(line) - len(line.lstrip())
            self.formatted_lines.append(line)
            return index + 1

        # Inside code block - preserve as is
        if self.in_code_block:
            self.formatted_lines.append(line)
            return index + 1

        # Check for table
        if self._is_table_line(line):
            return self._process_table(index)

        # Process different line types
        if self._is_heading(line):
            self._format_heading(line, index)
        elif self._is_list_item(line):
            self._format_list_item(line)
        elif self._is_blockquote(line):
            self._format_blockquote(line)
        else:
            # Regular line - just remove trailing whitespace
            self.formatted_lines.append(line.rstrip())

        return index + 1

    def _is_heading(self, line: str) -> bool:
        """Check if line is a heading"""
        return bool(re.match(r'^#{1,6}\s+.+', line))

    def _format_heading(self, line: str, index: int):
        """Format heading with proper spacing"""
        # Add blank line before heading (except at start or after another blank line)
        if (self.formatted_lines and
            self.formatted_lines[-1].strip() and
            index > 0):
            self.formatted_lines.append('')

        # Format heading: ensure single space after #
        match = re.match(r'^(#{1,6})\s*(.+)$', line)
        if match:
            hashes = match.group(1)
            text = match.group(2).strip()
            # Remove trailing punctuation from heading
            text = re.sub(r'[.!?:]+$', '', text)
            self.formatted_lines.append(f'{hashes} {text}')

    def _is_list_item(self, line: str) -> bool:
        """Check if line is a list item"""
        stripped = line.lstrip()
        # Unordered list
        if re.match(r'^[-*+]\s+', stripped):
            return True
        # Ordered list
        if re.match(r'^\d+\.\s+', stripped):
            return True
        return False

    def _format_list_item(self, line: str):
        """Format list item with proper spacing"""
        indent = len(line) - len(line.lstrip())
        stripped = line.lstrip()

        # Standardize unordered list markers to '-'
        if re.match(r'^[*+]\s+', stripped):
            stripped = re.sub(r'^[*+]\s+', '- ', stripped)

        # Ensure single space after marker
        stripped = re.sub(r'^(-|\d+\.)\s+', r'\1 ', stripped)

        self.formatted_lines.append(' ' * indent + stripped.rstrip())

    def _is_blockquote(self, line: str) -> bool:
        """Check if line is a blockquote"""
        return line.lstrip().startswith('>')

    def _format_blockquote(self, line: str):
        """Format blockquote with proper spacing"""
        indent = len(line) - len(line.lstrip())
        stripped = line.lstrip()

        # Ensure single space after >
        stripped = re.sub(r'^>\s*', '> ', stripped)

        self.formatted_lines.append(' ' * indent + stripped.rstrip())

    def _is_table_line(self, line: str) -> bool:
        """Check if line is part of a table"""
        stripped = line.strip()
        # Table separator line
        if re.match(r'^\|?[\s\-:|]+\|[\s\-:|]*$', stripped):
            return True
        # Table content line
        if '|' in stripped:
            return True
        return False

    def _process_table(self, start_index: int) -> int:
        """Process and format a table"""
        # Collect all table lines
        table_lines = []
        i = start_index

        while i < len(self.lines):
            line = self.lines[i]
            if not self._is_table_line(line):
                break
            table_lines.append(line)
            i += 1

        # Format the table
        formatted_table = self._format_table(table_lines)
        self.formatted_lines.extend(formatted_table)

        return i

    def _format_table(self, lines: List[str]) -> List[str]:
        """Format a table with proper alignment"""
        if not lines:
            return []

        # Parse table
        rows = []
        separator_index = -1

        for i, line in enumerate(lines):
            stripped = line.strip()
            # Remove leading/trailing pipes and split
            if stripped.startswith('|'):
                stripped = stripped[1:]
            if stripped.endswith('|'):
                stripped = stripped[:-1]

            cells = [cell.strip() for cell in stripped.split('|')]

            # Check if this is separator line
            if re.match(r'^[\s\-:]+$', stripped.replace('|', '')):
                separator_index = i

            rows.append(cells)

        if not rows:
            return []

        # Calculate column widths
        num_cols = max(len(row) for row in rows)
        col_widths = [0] * num_cols

        for row in rows:
            for j, cell in enumerate(row):
                if j < num_cols:
                    col_widths[j] = max(col_widths[j], len(cell))

        # Format rows
        formatted_rows = []
        for i, row in enumerate(rows):
            # Pad row to have all columns
            while len(row) < num_cols:
                row.append('')

            if i == separator_index:
                # Format separator row
                cells = []
                for j, cell in enumerate(row):
                    width = col_widths[j]
                    if ':' in cell:
                        if cell.startswith(':') and cell.endswith(':'):
                            cells.append(':' + '-' * (width - 2) + ':')
                        elif cell.startswith(':'):
                            cells.append(':' + '-' * (width - 1))
                        elif cell.endswith(':'):
                            cells.append('-' * (width - 1) + ':')
                        else:
                            cells.append('-' * width)
                    else:
                        cells.append('-' * width)
                formatted_rows.append('| ' + ' | '.join(cells) + ' |')
            else:
                # Format data row
                cells = []
                for j, cell in enumerate(row):
                    cells.append(cell.ljust(col_widths[j]))
                formatted_rows.append('| ' + ' | '.join(cells) + ' |')

        return formatted_rows

    def _normalize_blank_lines(self):
        """Remove multiple consecutive blank lines"""
        normalized = []
        prev_blank = False

        for line in self.formatted_lines:
            is_blank = not line.strip()

            # Skip if this is a blank line and previous was also blank
            if is_blank and prev_blank:
                continue

            normalized.append(line)
            prev_blank = is_blank

        self.formatted_lines = normalized

def format_file(file_path: str, in_place: bool = False) -> str:
    """Format a markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    formatter = MarkdownFormatter(content)
    formatted = formatter.format()

    if in_place:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formatted)
        return f"✅ Formatted {file_path}"
    else:
        return formatted

def main():
    parser = argparse.ArgumentParser(description='Format markdown files')
    parser.add_argument('file', help='Markdown file to format')
    parser.add_argument('-i', '--in-place', action='store_true',
                        help='Edit file in place')
    parser.add_argument('-o', '--output', help='Output file path')

    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        sys.exit(1)

    result = format_file(args.file, args.in_place)

    if args.in_place:
        print(result)
    elif args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"✅ Formatted output written to {args.output}")
    else:
        print(result)

if __name__ == '__main__':
    main()
