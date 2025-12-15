#!/usr/bin/env node
/**
 * Pre-commit hook to detect DRY violations and code duplication in TypeScript/JavaScript files.
 *
 * Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive
 *
 * Checks for:
 * 1. Duplicate code blocks (similar consecutive lines)
 * 2. Repeated string literals
 * 3. Repeated object patterns (like className in React)
 */

const fs = require('fs');

// Configuration
const MIN_DUPLICATE_LINES = 6;
const MIN_STRING_LENGTH = 30;
const MIN_STRING_OCCURRENCES = 4;
const MIN_CLASSNAME_OCCURRENCES = 3;

/**
 * Normalize a line for comparison
 */
function normalizeLine(line) {
  return line
    .trim()
    .replace(/\/\/.*$/, '') // Remove single-line comments
    .replace(/\s+/g, ' ')   // Normalize whitespace
    .trim();
}

/**
 * Extract string literals from code
 */
function extractStrings(content) {
  const strings = [];
  const lines = content.split('\n');

  const stringRegex = /(['"`])(?:(?!\1)[^\\]|\\.)*?\1/g;

  lines.forEach((line, index) => {
    if (line.trim().startsWith('import ') || line.trim().startsWith('//')) {
      return;
    }

    let match;
    while ((match = stringRegex.exec(line)) !== null) {
      const str = match[0].slice(1, -1);
      if (str.length >= MIN_STRING_LENGTH && !isCommonPattern(str)) {
        strings.push({ line: index + 1, value: str });
      }
    }
  });

  return strings;
}

/**
 * Check if string matches common patterns we should ignore
 */
function isCommonPattern(str) {
  const patterns = [
    /^https?:\/\//,           // URLs
    /^\w+@\w+\.\w+/,          // Emails
    /^[A-Z_]+$/,              // Constants
    /^\d{4}-\d{2}-\d{2}/,     // Dates
    /^application\/\w+/,      // MIME types
    /^Bearer\s/,              // Auth headers
    /^#[0-9a-fA-F]{3,8}$/,    // Color codes
    /^on[A-Z]/,               // Event handlers
    /^use[A-Z]/,              // Custom hooks
  ];
  return patterns.some(p => p.test(str));
}

/**
 * Check for consecutive duplicate blocks
 */
function checkConsecutiveDuplicates(lines) {
  const findings = [];
  const normalized = lines.map(normalizeLine);

  for (let i = 0; i < normalized.length - MIN_DUPLICATE_LINES; i++) {
    if (!normalized[i] || normalized[i].length < 5) continue;

    const block = normalized.slice(i, i + MIN_DUPLICATE_LINES);

    for (let j = i + MIN_DUPLICATE_LINES; j <= normalized.length - MIN_DUPLICATE_LINES; j++) {
      const compareBlock = normalized.slice(j, j + MIN_DUPLICATE_LINES);

      if (JSON.stringify(block) === JSON.stringify(compareBlock)) {
        if (block.every(line => line.length > 5)) {
          findings.push({
            type: 'duplicate_block',
            startLine: i + 1,
            endLine: i + MIN_DUPLICATE_LINES,
            duplicateAt: j + 1,
            preview: lines[i].trim().slice(0, 40) + '...'
          });
        }
        break;
      }
    }
  }

  return findings;
}

/**
 * Check for repeated string literals
 */
function checkStringDuplicates(strings) {
  const findings = [];
  const counts = {};

  strings.forEach(({ line, value }) => {
    if (!counts[value]) {
      counts[value] = { count: 0, lines: [] };
    }
    counts[value].count++;
    counts[value].lines.push(line);
  });

  Object.entries(counts).forEach(([str, { count, lines }]) => {
    if (count >= MIN_STRING_OCCURRENCES) {
      findings.push({
        type: 'repeated_string',
        count,
        lines,
        preview: str.length > 50 ? str.slice(0, 50) + '...' : str
      });
    }
  });

  return findings;
}

/**
 * Check for repeated className patterns (React specific)
 */
function checkRepeatedClassNames(content) {
  const findings = [];
  const classNameRegex = /className\s*=\s*["'`]([^"'`]+)["'`]/g;
  const classes = {};

  let match;
  const lines = content.split('\n');

  lines.forEach((line, index) => {
    while ((match = classNameRegex.exec(line)) !== null) {
      const className = match[1];
      if (className.length > 30) {
        if (!classes[className]) {
          classes[className] = { count: 0, lines: [] };
        }
        classes[className].count++;
        classes[className].lines.push(index + 1);
      }
    }
  });

  Object.entries(classes).forEach(([className, { count, lines }]) => {
    if (count >= MIN_CLASSNAME_OCCURRENCES) {
      const isCommonUtility = /^(flex|grid|text|bg|p-|m-|w-|h-)/.test(className);
      if (!isCommonUtility) {
        findings.push({
          type: 'repeated_className',
          count,
          lines,
          preview: className.slice(0, 60) + '...'
        });
      }
    }
  });

  return findings;
}

/**
 * Check a single file
 */
function checkFile(filepath) {
  const findings = [];

  try {
    const content = fs.readFileSync(filepath, 'utf-8');
    const lines = content.split('\n');

    findings.push(...checkConsecutiveDuplicates(lines));

    const strings = extractStrings(content);
    findings.push(...checkStringDuplicates(strings));

    if (filepath.endsWith('.tsx') || filepath.endsWith('.jsx')) {
      findings.push(...checkRepeatedClassNames(content));
    }

  } catch (error) {
    console.error(`Error reading ${filepath}: ${error.message}`);
  }

  return findings;
}

/**
 * Format findings for display
 */
function formatFindings(filepath, findings) {
  if (findings.length === 0) return '';

  let output = `\n${filepath}:\n`;

  findings.forEach(finding => {
    switch (finding.type) {
      case 'duplicate_block':
        output += `  - Duplicate block at lines ${finding.startLine}-${finding.endLine} `;
        output += `(also at line ${finding.duplicateAt}): ${finding.preview}\n`;
        break;
      case 'repeated_string':
        output += `  - String repeated ${finding.count}x (lines ${finding.lines.join(', ')}): `;
        output += `"${finding.preview}"\n`;
        break;
      case 'repeated_className':
        output += `  - className repeated ${finding.count}x (lines ${finding.lines.join(', ')}): `;
        output += `"${finding.preview}"\n`;
        break;
    }
  });

  return output;
}

/**
 * Main entry point
 */
function main() {
  const args = process.argv.slice(2);
  const verbose = args.includes('--verbose');
  const files = args.filter(arg => arg !== '--verbose');

  if (files.length === 0) {
    console.log('No files to check');
    process.exit(0);
  }

  let totalIssues = 0;
  let fileCount = 0;
  const fileFindings = [];

  files.forEach(file => {
    if (!/\.(ts|tsx|js|jsx)$/.test(file)) return;

    const findings = checkFile(file);
    if (findings.length > 0) {
      fileCount++;
      totalIssues += findings.length;
      fileFindings.push({ file, findings });
    }
  });

  if (totalIssues > 0) {
    if (verbose) {
      fileFindings.forEach(({ file, findings }) => {
        console.log(formatFindings(file, findings));
      });
    } else {
      console.log(`DRY: ${totalIssues} potential issue(s) in ${fileCount} file(s). Run with --verbose for details.`);
    }
  }

  // Always return 0 (warning only)
  process.exit(0);
}

main();
