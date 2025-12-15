/**
 * ESLint Configuration for Vibe Coding
 *
 * Catches common AI-generated code issues in JavaScript/TypeScript.
 * Copy to your project and customize as needed.
 *
 * Install: npm install -D eslint @eslint/js typescript-eslint
 */

import js from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      // ===========================================
      // AI agents often introduce these issues
      // ===========================================

      // Prevent unused variables (AI often leaves these behind)
      '@typescript-eslint/no-unused-vars': ['warn', {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
      }],

      // Prevent any type (AI loves to use any as a quick fix)
      '@typescript-eslint/no-explicit-any': 'warn',

      // Require explicit return types (AI often forgets these)
      '@typescript-eslint/explicit-function-return-type': ['warn', {
        allowExpressions: true,
        allowTypedFunctionExpressions: true,
      }],

      // Prevent console statements (AI adds these for debugging)
      'no-console': ['warn', { allow: ['warn', 'error'] }],

      // Prevent debugger statements
      'no-debugger': 'error',

      // Require const over let when possible
      'prefer-const': 'warn',

      // Prevent empty catch blocks (AI often swallows errors)
      'no-empty': ['warn', { allowEmptyCatch: false }],

      // ===========================================
      // Code quality rules
      // ===========================================

      // Enforce consistent naming
      '@typescript-eslint/naming-convention': [
        'warn',
        {
          selector: 'interface',
          format: ['PascalCase'],
        },
        {
          selector: 'typeAlias',
          format: ['PascalCase'],
        },
        {
          selector: 'variable',
          format: ['camelCase', 'UPPER_CASE', 'PascalCase'],
        },
        {
          selector: 'function',
          format: ['camelCase', 'PascalCase'],
        },
      ],

      // Prevent magic numbers
      'no-magic-numbers': ['warn', {
        ignore: [-1, 0, 1, 2],
        ignoreArrayIndexes: true,
        ignoreDefaultValues: true,
      }],

      // Enforce consistent brace style
      'curly': ['warn', 'all'],

      // Require === instead of ==
      'eqeqeq': ['error', 'always'],

      // Prevent nested ternaries (AI loves these)
      'no-nested-ternary': 'warn',

      // Limit function complexity
      'complexity': ['warn', 10],

      // Limit function length
      'max-lines-per-function': ['warn', {
        max: 50,
        skipBlankLines: true,
        skipComments: true,
      }],

      // Limit nesting depth
      'max-depth': ['warn', 4],

      // ===========================================
      // React-specific (uncomment if using React)
      // ===========================================
      // 'react/prop-types': 'off',  // Using TypeScript
      // 'react/react-in-jsx-scope': 'off',  // React 17+
      // 'react-hooks/rules-of-hooks': 'error',
      // 'react-hooks/exhaustive-deps': 'warn',
    },
  },
  {
    // Ignore patterns
    ignores: [
      'node_modules/**',
      'dist/**',
      'build/**',
      'coverage/**',
      '*.config.js',
      '*.config.ts',
    ],
  }
);
