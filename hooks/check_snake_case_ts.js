#!/usr/bin/env node
/**
 * Pre-commit hook to detect snake_case property names in TypeScript interfaces and types.
 *
 * Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive
 *
 * When working with APIs that return snake_case (like Django/Python backends),
 * AI agents often generate TypeScript interfaces with snake_case properties.
 * If your app transforms API responses to camelCase (via axios interceptors, etc.),
 * this mismatch causes subtle bugs where properties are undefined.
 *
 * Example bug:
 *   interface User {
 *     first_name: string;  // Wrong! API response is transformed to firstName
 *   }
 *   const name = user.first_name; // undefined!
 */

const fs = require('fs');
const path = require('path');

/**
 * Remove string literals from a line to avoid counting braces inside strings
 */
function removeStringsFromLine(line) {
  let result = '';
  let i = 0;
  let inSingleQuote = false;
  let inDoubleQuote = false;
  let inTemplate = false;

  while (i < line.length) {
    const char = line[i];
    const prevChar = i > 0 ? line[i - 1] : '';

    // Handle escape sequences
    if (prevChar === '\\') {
      result += ' ';
      i++;
      continue;
    }

    // Toggle string state
    if (char === "'" && !inDoubleQuote && !inTemplate) {
      inSingleQuote = !inSingleQuote;
      result += ' ';
      i++;
      continue;
    }
    if (char === '"' && !inSingleQuote && !inTemplate) {
      inDoubleQuote = !inDoubleQuote;
      result += ' ';
      i++;
      continue;
    }
    if (char === '`' && !inSingleQuote && !inDoubleQuote) {
      inTemplate = !inTemplate;
      result += ' ';
      i++;
      continue;
    }

    // Replace string content with spaces, keep braces outside strings
    if (inSingleQuote || inDoubleQuote || inTemplate) {
      result += ' ';
    } else {
      result += char;
    }
    i++;
  }

  return result;
}

// Configuration
const SNAKE_CASE_PATTERN = /^[a-z]+(_[a-z0-9]+)+$/;

// Properties that are allowed to be snake_case (HTTP headers, etc.)
const ALLOWED_SNAKE_CASE = new Set([
  'Content-Type',
  'X-CSRFToken',
  '__typename',
  '__retryCount',
  'grant_type',      // OAuth standard
  'client_id',       // OAuth standard
  'client_secret',   // OAuth standard
  'access_token',    // OAuth standard
  'refresh_token',   // OAuth standard
  'token_type',      // OAuth standard
]);

/**
 * Extract interface/type property names from TypeScript code
 */
function extractTypeProperties(content, filepath) {
  const findings = [];
  const lines = content.split('\n');

  // Track if we're inside an interface or type definition
  let insideTypeBlock = false;
  let braceDepth = 0;
  let currentTypeName = '';
  let typeStartLine = 0;

  // Patterns for interface/type definitions
  const typeStartPattern = /^\s*(export\s+)?(interface|type)\s+(\w+)/;
  const propertyPattern = /^\s*(['"]?)(\w+)\1\s*[?]?\s*:/;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;

    // Check for start of interface/type
    const typeMatch = line.match(typeStartPattern);
    if (typeMatch) {
      currentTypeName = typeMatch[3];
      typeStartLine = lineNum;

      // Check if it's a single-line type (type Foo = {...})
      // Use cleaned line to ignore braces in strings
      const cleanedTypeLine = removeStringsFromLine(line);
      if (cleanedTypeLine.includes('{')) {
        insideTypeBlock = true;
        braceDepth = (cleanedTypeLine.match(/{/g) || []).length - (cleanedTypeLine.match(/}/g) || []).length;
      }
      continue;
    }

    // Track braces for multi-line types
    if (currentTypeName && !insideTypeBlock && line.includes('{')) {
      insideTypeBlock = true;
      braceDepth = 1;
    }

    if (insideTypeBlock) {
      // Update brace depth (using cleaned line to ignore braces in strings)
      const cleanedLine = removeStringsFromLine(line);
      braceDepth += (cleanedLine.match(/{/g) || []).length;
      braceDepth -= (cleanedLine.match(/}/g) || []).length;

      // Check for property definitions
      const propMatch = line.match(propertyPattern);
      if (propMatch) {
        const propertyName = propMatch[2];

        // Check if it's snake_case
        if (SNAKE_CASE_PATTERN.test(propertyName) && !ALLOWED_SNAKE_CASE.has(propertyName)) {
          const camelCase = snakeToCamel(propertyName);
          findings.push({
            line: lineNum,
            property: propertyName,
            suggested: camelCase,
            typeName: currentTypeName,
            context: line.trim()
          });
        }
      }

      // Check if we've exited the type block
      if (braceDepth <= 0) {
        insideTypeBlock = false;
        currentTypeName = '';
      }
    }
  }

  return findings;
}

/**
 * Convert snake_case to camelCase
 */
function snakeToCamel(str) {
  return str.replace(/_([a-z0-9])/g, (_, char) => char.toUpperCase());
}

/**
 * Check a single file
 */
function checkFile(filepath) {
  try {
    const content = fs.readFileSync(filepath, 'utf-8');
    return extractTypeProperties(content, filepath);
  } catch (error) {
    console.error(`Error reading ${filepath}: ${error.message}`);
    return [];
  }
}

/**
 * Format findings for display
 */
function formatFindings(filepath, findings) {
  if (findings.length === 0) return '';

  let output = `\n${filepath}:\n`;

  findings.forEach(finding => {
    output += `  Line ${finding.line} in ${finding.typeName}: "${finding.property}" → "${finding.suggested}"\n`;
    output += `    ${finding.context}\n`;
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
    process.exit(0);
  }

  let totalIssues = 0;
  let fileCount = 0;
  const fileFindings = [];

  files.forEach(file => {
    // Only check TypeScript files
    if (!/\.(ts|tsx)$/.test(file)) return;

    // Skip test files and type declaration files
    if (/\.(test|spec|d)\.(ts|tsx)$/.test(file)) return;

    const findings = checkFile(file);
    if (findings.length > 0) {
      fileCount++;
      totalIssues += findings.length;
      fileFindings.push({ file, findings });
    }
  });

  if (totalIssues > 0) {
    console.log('\nsnake_case properties found in TypeScript interfaces/types!\n');

    if (verbose) {
      fileFindings.forEach(({ file, findings }) => {
        console.log(formatFindings(file, findings));
      });
    } else {
      console.log(`Found ${totalIssues} snake_case property(ies) in ${fileCount} file(s).`);
      console.log('\nTop issues:');
      fileFindings.slice(0, 3).forEach(({ file, findings }) => {
        findings.slice(0, 2).forEach(f => {
          console.log(`  ${path.basename(file)}: ${f.property} → ${f.suggested}`);
        });
      });
      if (totalIssues > 6) {
        console.log(`  ... and ${totalIssues - 6} more`);
      }
    }

    console.log('\nWhy this matters:');
    console.log('  If your API client transforms responses from snake_case to camelCase,');
    console.log('  these properties will be undefined at runtime!\n');
    console.log('Run with --verbose for full details.\n');

    // Warning only - allow commit to proceed
    process.exit(0);
  }

  process.exit(0);
}

main();
