---
name: markdown-formatter
description: "Comprehensive markdown creation, formatting, and validation. Use when working with markdown files (.md) for: (1) Formatting existing markdown to improve consistency and readability, (2) Validating markdown for syntax errors, style compliance, broken links, or content quality issues, (3) Creating new markdown documents (READMEs, technical docs, API docs, articles), (4) Fixing markdown issues or applying best practices. Triggered by phrases like \"format this markdown\", \"validate this .md file\", \"create a README\", or \"fix markdown issues\"."
---

# Markdown Formatter

A comprehensive skill for creating beautiful, well-formatted, and validated markdown documents.

## Quick Start

### Format a Markdown File

Use the formatting script to automatically improve markdown formatting:

```bash
python3 scripts/format_markdown.py document.md -i
```

This will format the file in-place according to best practices.

### Validate a Markdown File

Use the validation script to check for issues:

```bash
python3 scripts/validate_markdown.py document.md
```

This checks for syntax errors, style issues, broken links, and content quality problems.

## Core Capabilities

### 1. Formatting Markdown

The `scripts/format_markdown.py` script automatically formats markdown files to improve consistency and readability.

**What it fixes:**

- **Headings**: Proper spacing before/after, consistent formatting, removes trailing punctuation
- **Lists**: Standardizes markers (uses `-` for unordered lists), ensures proper spacing
- **Tables**: Aligns columns for readability, consistent spacing
- **Code blocks**: Preserves formatting while ensuring proper structure
- **Whitespace**: Removes trailing whitespace, normalizes blank lines, ensures single newline at EOF
- **Blockquotes**: Ensures consistent spacing after `>` marker

**Usage:**

```bash
# Format and print to stdout
python3 scripts/format_markdown.py document.md

# Format in-place (modifies original file)
python3 scripts/format_markdown.py document.md -i

# Format and save to new file
python3 scripts/format_markdown.py document.md -o formatted.md
```

**When to use:** Apply formatting when markdown looks inconsistent, has spacing issues, poorly aligned tables, or doesn't follow best practices.

### 2. Validating Markdown

The `scripts/validate_markdown.py` script checks markdown files for various issues.

**What it checks:**

- **Syntax errors**: Unclosed code blocks, unmatched brackets, incomplete link syntax
- **Style guide compliance**: Line length, heading hierarchy, trailing punctuation, multiple blank lines, trailing whitespace, missing H1
- **Link validation**: Broken internal file links, invalid external URL formats
- **Content quality**: Missing image alt text, bare URLs not using link syntax

**Usage:**

```bash
# Full validation
python3 scripts/validate_markdown.py document.md

# Skip link checking (faster)
python3 scripts/validate_markdown.py document.md --no-links

# Skip style checks
python3 scripts/validate_markdown.py document.md --no-style

# JSON output (for programmatic use)
python3 scripts/validate_markdown.py document.md --json
```

**Output format:**

- **Issues**: Problems that must be fixed (syntax errors, broken links)
- **Warnings**: Style and quality suggestions (line length, missing H1, bare URLs)

**When to use:** Validate markdown before committing, publishing, or when troubleshooting rendering issues.

### 3. Creating New Markdown Documents

Use the templates in `assets/templates/` as starting points for common document types.

**Available templates:**

- **README.md**: Project README with features, installation, usage, API reference sections
- **TECHNICAL_SPEC.md**: Technical specification with requirements, architecture, implementation details
- **DOCUMENTATION.md**: General documentation template with clear sections
- **API.md**: API documentation with endpoints, parameters, response examples

**Workflow:**

1. Copy the appropriate template to your project
2. Fill in the placeholder content
3. Format using `format_markdown.py`
4. Validate using `validate_markdown.py`

**Example:**

```bash
# Copy template
cp assets/templates/README.md ./README.md

# Edit content with your information
# (use your editor)

# Format the file
python3 scripts/format_markdown.py README.md -i

# Validate the result
python3 scripts/validate_markdown.py README.md
```

### 4. Learning Markdown Best Practices

For detailed guidance on markdown formatting, consult the reference files:

- **references/style-guide.md**: Comprehensive style guide covering all markdown elements with best practices and examples
  - Headings, paragraphs, lists, links, images
  - Code blocks, tables, blockquotes, emphasis
  - Line length, whitespace, consistency, accessibility

- **references/examples.md**: Practical examples for common use cases
  - README files
  - Technical documentation
  - API documentation
  - Tutorial content
  - Blog posts
  - Meeting notes

**When to reference:**

- When unsure about proper markdown syntax
- When creating a specific document type (README, API docs, etc.)
- When deciding between multiple formatting approaches
- When learning markdown best practices

Read these references when you need detailed guidance beyond the quick formatting/validation scripts.

## Workflow Examples

### Workflow 1: Fixing an Existing Markdown File

1. **Validate first** to understand issues:
   ```bash
   python3 scripts/validate_markdown.py document.md
   ```

2. **Review the issues and warnings** reported

3. **Format the file** to auto-fix formatting issues:
   ```bash
   python3 scripts/format_markdown.py document.md -i
   ```

4. **Validate again** to see remaining issues:
   ```bash
   python3 scripts/validate_markdown.py document.md
   ```

5. **Manually fix** any remaining issues (broken links, missing alt text, etc.)

### Workflow 2: Creating a New README

1. **Copy the template**:
   ```bash
   cp assets/templates/README.md ./README.md
   ```

2. **Edit with your content** using your preferred editor

3. **Format the file**:
   ```bash
   python3 scripts/format_markdown.py README.md -i
   ```

4. **Validate**:
   ```bash
   python3 scripts/validate_markdown.py README.md
   ```

5. **Fix any issues** reported by validation

### Workflow 3: Creating Technical Documentation

1. **Consult examples** for inspiration:
   ```bash
   # Read the examples reference
   cat references/examples.md | grep -A 50 "Technical Documentation"
   ```

2. **Choose appropriate template** (TECHNICAL_SPEC.md or DOCUMENTATION.md)

3. **Copy and edit** the template with your content

4. **Reference style-guide.md** if unsure about formatting specific elements

5. **Format and validate** as in previous workflows

## Common Issues and Solutions

### Issue: "Unclosed code block"

**Cause:** Code block started with ` ``` ` but not closed

**Solution:** Add matching ` ``` ` at the end of the code block

### Issue: "Broken link: file not found"

**Cause:** Markdown link points to non-existent file

**Solution:** Fix the link path or create the missing file

### Issue: "Heading level skipped (h2 to h4)"

**Cause:** Jumped from `##` to `####` without `###`

**Solution:** Use proper heading hierarchy: h1 → h2 → h3

### Issue: "Image missing alt text"

**Cause:** Image syntax `![]()` has empty alt text

**Solution:** Add descriptive alt text: `![Description](image.png)`

### Issue: "Multiple consecutive blank lines"

**Cause:** Multiple empty lines in a row

**Solution:** Run `format_markdown.py` to auto-fix, or manually remove extra blank lines

## Best Practices

1. **Always validate before committing** - Catch issues early
2. **Use the formatter liberally** - It's safe and improves consistency
3. **Check links after restructuring** - Ensure internal links still work
4. **Add alt text to images** - Improves accessibility
5. **Keep lines under 120 characters** - Better readability in source
6. **Use proper heading hierarchy** - Don't skip levels
7. **One H1 per document** - Usually the document title
8. **Consult the style guide** - When unsure about formatting

## Tips

- Run validation with `--no-links` for faster feedback during editing
- Use templates as starting points, not rigid structures
- The formatter preserves code block content - it's safe to use on technical docs
- JSON output from validator can be integrated into CI/CD pipelines
- Keep the style-guide.md reference handy for detailed guidance
