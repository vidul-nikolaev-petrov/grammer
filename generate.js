const fs = require('fs');

// Load indexed data
const dataModule = require('./dictionaryData.js');

// Load HTML template
let template = fs.readFileSync('./template.html', 'utf8');

// Inject and save
const jsonData = JSON.stringify(dataModule);
const finalHtml = template.replace('const dictionary = [];', `const dictionary = ${jsonData};`);

fs.writeFileSync('./index.html', finalHtml);
console.log(`Standalone search engine created with ${dataModule.length} records.`);
