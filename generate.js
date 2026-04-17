const fs = require("fs");

// Load indexed data
const dataModule = require("./dictionaryData.js");


let template = fs.readFileSync("./template.html", "utf8");

const string = JSON.stringify;
const dictionary = dataModule;
const searchIndex = dataModule.map(i => (i.t || "").toLowerCase());

let finalHtml = template.replace(
    `const dictionary = ["placeholder"];`,
    `const dictionary = ${string(dictionary)};`,
);

finalHtml = finalHtml.replace(
    `const searchIndex = ["placeholder"];`,
    `const searchIndex = ${string(searchIndex)};`,
);

fs.writeFileSync("./index.html", finalHtml);
console.log(
    `Standalone search engine created with ${dataModule.length} records.`,
);
