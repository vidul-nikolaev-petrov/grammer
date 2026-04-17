const fs = require("fs");
const path = require("path");
const cheerio = require("cheerio");

// CONFIG
const MIRROR_DIR = "./mirror/beron.mon.bg/rechnik";
const OUTPUT_FILE = "./dictionaryData.js";

// STRINGS TO IGNORE
const ERR_404 =
    "Страницата, която търсите, не съществува или не може да бъде открита.";
const GENERIC_TITLE = "Официален правописен речник на българския език • БЕРОН";

build();

function build() {
    const index = [];
    const resolvedMirrorPath = path.resolve(MIRROR_DIR);

    console.log(`Deep Indexing: ${resolvedMirrorPath}`);

    function walk(dir) {
        if (!fs.existsSync(dir)) return;

        const files = fs.readdirSync(dir);
        for (const file of files) {
            const fullPath = path.join(dir, file);

            if (fs.statSync(fullPath).isDirectory()) {
                walk(fullPath);
            } else if (file.endsWith(".html") || !file.includes(".")) {
                try {
                    const html = fs.readFileSync(fullPath, "utf8");
                    const $ = cheerio.load(html);

                    // 1. Get Main Title (for context/grouping)
                    let word =
                        $("h1").first().text().trim() ||
                        $("title").text().trim();
                    if (
                        !word ||
                        word.includes(ERR_404) ||
                        word === GENERIC_TITLE
                    )
                        continue;

                    word = word
                        .replace("• БЕРОН", "")
                        .replace(" - БЕРОН", "")
                        .trim();

                    const relativePath = fullPath
                        .replace(resolvedMirrorPath, "")
                        .replace(/\\/g, "/")
                        .replace(/\/index\.html$/, "");

                    // 2. INDEX HEADWORD
                    index.push({ t: word, l: relativePath, type: "headword" });

                    // 3. TARGET ELEMENTS WITH data-ref ATTRIBUTE
                    // This finds <h2>, <p>, <li>, etc., that have the rule number
                    $("[data-ref]").each((_, el) => {
                        const ruleNum = $(el).attr("data-ref");
                        const content = $(el).text().trim();

                        if (ruleNum && content) {
                            index.push({
                                t: content,
                                l: relativePath,
                                type: "rule",
                                r: ruleNum,
                                parent: word,
                            });
                        }
                    });

                    // 4. (Optional) INDEX REMAINING PARAGRAPHS
                    // We check if it's already indexed as a rule to avoid duplicates
                    $("p").each((_, el) => {
                        const hasDataRef = $(el).attr("data-ref");
                        const pText = $(el).text().trim();

                        if (
                            !hasDataRef &&
                            pText.length > 10 &&
                            pText !== word
                        ) {
                            index.push({
                                t: pText,
                                l: relativePath,
                                type: "content",
                                parent: word,
                            });
                        }
                    });
                } catch (e) {
                    /* Skip unreadable files */
                }
            }
        }
    }

    walk(resolvedMirrorPath);
    fs.writeFileSync(OUTPUT_FILE, `module.exports = ${JSON.stringify(index)};`);
    console.log(`Done! Indexed ${index.length} entries.`);
}
