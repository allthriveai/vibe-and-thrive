#!/usr/bin/env node
/**
 * Pre-commit hook to detect TypeScript `any` type usage.
 *
 * Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive
 *
 * AI assistants love to use `any` as a quick fix for type errors.
 * This defeats the purpose of TypeScript and hides bugs.
 *
 * Warns but doesn't block commits.
 */

const fs = require('fs');
const path = require('path');

// Patterns that indicate `any` type usage
const ANY_PATTERNS = [
  // Type annotations
  /:\s*any\b/,
  /:\s*any\s*[,)=\]]/,
  // Generic parameters
  /<any>/,
  /<any,/,
  /,\s*any>/,
  // Type assertions
  /as\s+any\b/,
  // Array of any
  /any\[\]/,
  // Function parameters
  /\(\s*\w+\s*:\s*any\b/,
];

// Patterns that indicate acceptable usage (false positives)
const IGNORE_PATTERNS = [
  /\/\/\s*noqa:\s*any/i,
  /\/\/\s*eslint-disable.*any/i,
  /\/\*\s*eslint-disable.*any/i,
  // Type guard functions
  /isAny/i,
  // Comments
  /^\s*\/\//,
  /^\s*\/\*/,
  /^\s*\*/,
  // String literals containing "any"
  /['"`].*any.*['"`]/,
];

// Words containing "any" that are NOT type annotations
const FALSE_POSITIVE_WORDS = [
  'company', 'companies', 'many', 'anyway', 'anyone', 'anything', 'anywhere',
  'fantasy', 'nanny', 'uncanny', 'botany', 'accompany', 'tiffany', 'germany',
  'tyranny', 'mahogany', 'miscellany'
];

// Check if line should be ignored
function shouldIgnore(line) {
  return IGNORE_PATTERNS.some(pattern => pattern.test(line));
}

// Check if a match is actually a type annotation or a false positive word
function isRealAnyType(line, match) {
  // Get context around the match (the word containing "any")
  const start = Math.max(0, match.index - 20);
  const end = Math.min(line.length, match.index + match[0].length + 20);
  const context = line.substring(start, end).toLowerCase();

  // Check if any false positive word is in the context of this match
  for (const word of FALSE_POSITIVE_WORDS) {
    if (context.includes(word)) {
      // Make sure the "any" we matched isn't part of a type annotation
      // by checking if `: any` or `as any` etc. is in the same region
      const typeAnnotationPattern = /:\s*any\b|<any|as\s+any|any\[\]/;
      if (!typeAnnotationPattern.test(context)) {
        return false;
      }
    }
  }
  return true;
}

// Check if line contains any type
function hasAnyType(line) {
  if (shouldIgnore(line)) {
    return false;
  }

  // Check each pattern and verify it's a real any type
  for (const pattern of ANY_PATTERNS) {
    const match = pattern.exec(line);
    if (match && isRealAnyType(line, match)) {
      return true;
    }
  }
  return false;
}

// Check a single file
function checkFile(filepath) {
  const findings = [];

  try {
    const content = fs.readFileSync(filepath, 'utf-8');
    const lines = content.split('\n');

    lines.forEach((line, index) => {
      if (hasAnyType(line)) {
        // Extract context around the `any`
        const match = line.match(/:\s*any|<any|as\s+any|any\[\]/);
        if (match) {
          findings.push({
            line: index + 1,
            content: line.trim().substring(0, 80),
          });
        }
      }
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
    // Only check TypeScript files
    if (!/\.(ts|tsx)$/.test(file)) {
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

    console.log(`\n⚠️  TypeScript 'any' type detected: ${total} instance(s) in ${allFindings.size} file(s)\n`);

    allFindings.forEach((findings, filepath) => {
      console.log(`  ${filepath}:`);
      findings.forEach(f => {
        console.log(`    Line ${f.line}: ${f.content}`);
      });
    });

    console.log('\n💡 Tip: Create proper interfaces instead of using "any".');
    console.log('   Ask AI: "Fix this without using any. Create proper types."\n');
    console.log('   Suppress with: // noqa: any\n');

    // Warn only, don't block
    return 0;
  }

  return 0;
}

// Run
const files = process.argv.slice(2);
process.exit(main(files));
