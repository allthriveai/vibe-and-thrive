#!/usr/bin/env node
/**
 * Pre-commit hook to detect unsafe HTML injection patterns.
 *
 * Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive
 *
 * AI assistants sometimes use innerHTML or dangerouslySetInnerHTML
 * without sanitization, creating XSS vulnerabilities.
 *
 * Warns but doesn't block commits.
 */

const fs = require('fs');
const path = require('path');

// Patterns that indicate unsafe HTML usage
const UNSAFE_PATTERNS = [
  {
    pattern: /\.innerHTML\s*=/,
    name: 'innerHTML assignment',
    risk: 'XSS if user content is included',
  },
  {
    pattern: /\.outerHTML\s*=/,
    name: 'outerHTML assignment',
    risk: 'XSS if user content is included',
  },
  {
    pattern: /dangerouslySetInnerHTML/,
    name: 'dangerouslySetInnerHTML',
    risk: 'React XSS if content not sanitized',
  },
  {
    pattern: /document\.write\s*\(/,
    name: 'document.write()',
    risk: 'XSS and performance issues',
  },
  {
    pattern: /\.insertAdjacentHTML\s*\(/,
    name: 'insertAdjacentHTML()',
    risk: 'XSS if user content is included',
  },
  {
    pattern: /\[innerHTML\]/,
    name: 'Angular [innerHTML]',
    risk: 'XSS if content not sanitized',
  },
  {
    pattern: /v-html\s*=/,
    name: 'Vue v-html',
    risk: 'XSS if content not sanitized',
  },
];

// Patterns that indicate safe usage (sanitization)
const SAFE_PATTERNS = [
  /DOMPurify/i,
  /sanitize/i,
  /xss/i,
  /escape/i,
  /noqa:\s*unsafe-html/i,
  /eslint-disable.*xss/i,
];

// Check if line has sanitization nearby
function hasSanitization(content, lineIndex, lines) {
  // Check 5 lines before and after
  const start = Math.max(0, lineIndex - 5);
  const end = Math.min(lines.length, lineIndex + 5);
  const context = lines.slice(start, end).join('\n');

  return SAFE_PATTERNS.some(pattern => pattern.test(context));
}

// Check a single file
function checkFile(filepath) {
  const findings = [];

  try {
    const content = fs.readFileSync(filepath, 'utf-8');
    const lines = content.split('\n');

    lines.forEach((line, index) => {
      // Skip comments
      const trimmed = line.trim();
      if (trimmed.startsWith('//') || trimmed.startsWith('*') || trimmed.startsWith('/*')) {
        return;
      }

      UNSAFE_PATTERNS.forEach(({ pattern, name, risk }) => {
        if (pattern.test(line)) {
          // Check if there's sanitization nearby
          if (!hasSanitization(content, index, lines)) {
            findings.push({
              line: index + 1,
              pattern: name,
              risk: risk,
              content: line.trim().substring(0, 60),
            });
          }
        }
      });
    });
  } catch (error) {
    console.error(`Error reading ${filepath}: ${error.message}`);
  }

  return findings;
}

// Main
function main(files) {
  const allFindings = new Map();

  files.forEach(file => {
    // Only check JS/TS files and HTML templates
    if (!/\.(js|jsx|ts|tsx|vue|svelte|html)$/.test(file)) {
      return;
    }

    const findings = checkFile(file);
    if (findings.length > 0) {
      allFindings.set(file, findings);
    }
  });

  if (allFindings.size > 0) {
    let total = 0;
    allFindings.forEach(findings => total += findings.length);

    console.log(`\n⚠️  Unsafe HTML patterns detected: ${total} instance(s)\n`);

    allFindings.forEach((findings, filepath) => {
      console.log(`  ${filepath}:`);
      findings.forEach(f => {
        console.log(`    Line ${f.line}: ${f.pattern}`);
        console.log(`      Risk: ${f.risk}`);
      });
    });

    console.log('\n💡 Tip: Never render user content as HTML without sanitization.');
    console.log('   Use a library like DOMPurify to sanitize HTML.');
    console.log('   Or use textContent/innerText for plain text.\n');
    console.log('   Example: DOMPurify.sanitize(userContent)\n');
    console.log('   Suppress with: // noqa: unsafe-html\n');

    // Warn only, don't block
    return 0;
  }

  return 0;
}

// Run
const files = process.argv.slice(2);
process.exit(main(files));
