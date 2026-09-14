const fs = require('fs').promises;
const path = require('path');
const acorn = require('acorn'); // JavaScript parser
const { promisify } = require('util');

class CodeAnalyzer {
  constructor() {
    this.rules = {
      missingFiles: ['consensus.js'],
      // Add more rules as needed
    };
  }

  async scan() {
    const issues = [];
    const files = await fs.readdir(path.join(__dirname, '../'));

    // Check for missing files
    this.rules.missingFiles.forEach(file => {
      if (!files.includes(file)) {
        issues.push({ type: 'missing_file', file });
      }
    });

    // Analyze JavaScript files for potential issues
    await this.analyzeJavaScriptFiles(files, issues);

    return issues;
  }

  async analyzeJavaScriptFiles(files, issues) {
    for (const file of files) {
      if (file.endsWith('.js')) {
        const filePath = path.join(__dirname, '../', file);
        const content = await fs.readFile(filePath, 'utf-8');

        // Parse the JavaScript file to an AST
        try {
          const ast = acorn.parse(content, { ecmaVersion: 2020 });
          this.checkForUnusedVariables(ast, issues, file);
          // Add more checks as needed
        } catch (error) {
          issues.push({ type: 'parsing_error', file, message: error.message });
        }
      }
    }
  }

  checkForUnusedVariables(ast, issues, file) {
    const variableNames = new Set();
    const usedNames = new Set();

    // Traverse the AST to collect variable names and used names
    acorn.walk.simple(ast, {
      VariableDeclaration(node) {
        node.declarations.forEach(decl => {
          variableNames.add(decl.id.name);
        });
      },
      Identifier(node) {
        usedNames.add(node.name);
      }
    });

    // Identify unused variables
    variableNames.forEach(name => {
      if (!usedNames.has(name)) {
        issues.push({ type: 'unused_variable', file, variable: name });
      }
    });
  }
}

module.exports = CodeAnalyzer;
