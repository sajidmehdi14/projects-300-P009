# Markdown Style Guide

Comprehensive style guide for writing beautiful, consistent markdown.

## Table of Contents

1. [Headings](#headings)
2. [Paragraphs and Line Breaks](#paragraphs-and-line-breaks)
3. [Lists](#lists)
4. [Links](#links)
5. [Images](#images)
6. [Code](#code)
7. [Tables](#tables)
8. [Blockquotes](#blockquotes)
9. [Emphasis](#emphasis)
10. [Horizontal Rules](#horizontal-rules)

## Headings

### Best Practices

- Use ATX-style headings (`#`) rather than Setext-style (`===` or `---`)
- Include a space after the `#` symbols
- Don't skip heading levels (e.g., don't jump from H1 to H3)
- Don't use punctuation at the end of headings
- Add a blank line before and after headings (except at the start of the document)
- Use only one H1 per document (the document title)

### Examples

**Good:**
```markdown
# Document Title

## Section

### Subsection

Content here.
```

**Bad:**
```markdown
#No space after hash
## Section.
#### Skipped H3
```

## Paragraphs and Line Breaks

### Best Practices

- Use blank lines to separate paragraphs
- Don't use multiple consecutive blank lines
- Keep line length under 120 characters where possible
- Don't use trailing spaces for line breaks (use `<br>` if needed)
- Remove trailing whitespace from lines

### Examples

**Good:**
```markdown
This is the first paragraph with some content.

This is the second paragraph.
```

**Bad:**
```markdown
First paragraph with trailing spaces
Second line forced with spaces


Multiple blank lines above
```

## Lists

### Best Practices

- Use `-` for unordered lists (consistent marker)
- Use `1.`, `2.`, `3.` for ordered lists
- Include a space after the list marker
- Indent nested lists by 2-4 spaces
- Add blank lines around lists (not between items)
- Align multi-line list items consistently

### Examples

**Good:**
```markdown
- First item
- Second item
  - Nested item
  - Another nested item
- Third item

1. First ordered item
2. Second ordered item
3. Third ordered item
```

**Bad:**
```markdown
* Mixed
- marker
+ styles

1.No space after marker
2.  Too many spaces
```

## Links

### Best Practices

- Use descriptive link text (not "click here")
- Use inline links for short URLs
- Use reference-style links for repeated or long URLs
- Ensure all links are valid
- Use relative paths for internal links
- Include `https://` for external links

### Examples

**Good:**
```markdown
See the [documentation](https://example.com/docs) for details.

Check out [this guide][guide] and [that tutorial][guide].

[guide]: https://example.com/guide
```

**Bad:**
```markdown
Click [here](example.com).

See http://example.com (bare URL)
```

## Images

### Best Practices

- Always include descriptive alt text
- Use relative paths for local images
- Keep image dimensions reasonable
- Consider using HTML for complex layouts
- Place images in an `images/` or `assets/` directory

### Examples

**Good:**
```markdown
![Architectural diagram showing system components](./images/architecture.png)

<img src="./images/logo.png" alt="Company logo" width="200">
```

**Bad:**
```markdown
![]( ./images/pic.png)

![](./images/diagram.png)
```

## Code

### Best Practices

- Use backticks for inline code
- Use triple backticks for code blocks
- Specify language for syntax highlighting
- Indent code blocks consistently
- Don't use indentation for code blocks (use fenced blocks)
- Keep code examples concise and relevant

### Examples

**Good:**
````markdown
Use the `print()` function to output text.

```python
def hello():
    print("Hello, world!")
```
````

**Bad:**
````markdown
Use the print() function without backticks.

```
# No language specified
def hello():
    print("Hello")
```
````

## Tables

### Best Practices

- Align columns for readability in source
- Include header row and separator
- Use colons in separator for alignment
- Keep table content concise
- Consider alternatives for complex data
- Ensure consistent spacing

### Examples

**Good:**
```markdown
| Name    | Age | City       |
|---------|-----|------------|
| Alice   | 30  | New York   |
| Bob     | 25  | London     |
| Charlie | 35  | Paris      |
```

**Bad:**
```markdown
|Name|Age|City|
|---|---|---|
|Alice|30|New York|
|Bob|25|London|
```

## Blockquotes

### Best Practices

- Use `>` for blockquotes
- Include space after `>`
- Use for quotes, notes, and callouts
- Nested quotes: increase `>` symbols
- Keep blockquote content focused

### Examples

**Good:**
```markdown
> This is a blockquote with proper spacing.
> It can span multiple lines.

> **Note:** Important information here.
```

**Bad:**
```markdown
>No space after angle bracket
>Multiple
>Lines
>Without
>Organization
```

## Emphasis

### Best Practices

- Use `*` or `_` for italic (prefer `*`)
- Use `**` or `__` for bold (prefer `**`)
- Use `***` for bold italic
- Don't use emphasis for headings or large blocks
- Use sparingly for maximum effect

### Examples

**Good:**
```markdown
This is *italic* text.

This is **bold** text.

This is ***bold italic*** text.
```

**Bad:**
```markdown
**Everything in bold loses emphasis.**

_Mixing_ **different* *styles_ is **confusing**.
```

## Horizontal Rules

### Best Practices

- Use `---` for horizontal rules
- Add blank lines before and after
- Use sparingly to separate major sections
- Don't use within lists or blockquotes

### Examples

**Good:**
```markdown
Section content here.

---

New section content here.
```

**Bad:**
```markdown
No spacing around rule
---
Makes it harder to read
```

## General Guidelines

### Line Length

- Aim for 80-120 characters per line
- Exception: Long links, tables, or code
- Break long sentences at natural points

### Whitespace

- One blank line between sections
- No multiple consecutive blank lines
- No trailing whitespace on lines
- Single newline at end of file

### Consistency

- Pick a style and stick with it
- Use consistent list markers
- Use consistent emphasis markers
- Use consistent heading style

### Accessibility

- Include alt text for all images
- Use descriptive link text
- Maintain proper heading hierarchy
- Ensure good contrast in code blocks

### File Organization

- Use meaningful file names
- Organize with directory structure
- Keep related files together
- Use lowercase with hyphens for file names
