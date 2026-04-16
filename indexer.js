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

                    // 1. Get Main Title
                    let word =
                        $("h1").first().text().trim() ||
                        $("title").text().trim();

                    // 2. GUARD: Skip error pages
                    if (
                        !word ||
                        word.includes(ERR_404) ||
                        word === GENERIC_TITLE
                    )
                        continue;

                    // Clean Title
                    word = word
                        .replace("• БЕРОН", "")
                        .replace(" - БЕРОН", "")
                        .trim();

                    // Calculate relative path for port 8080
                    const relativePath = fullPath
                        .replace(resolvedMirrorPath, "")
                        .replace(/\\/g, "/")
                        .replace(/\/index\.html$/, "");

                    // 3. INDEX TITLE (The primary headword)
                    index.push({ t: word, l: relativePath, type: "headword" });

                    // 4. DEEP INDEX BODY PARAGRAPHS
                    // We target <p> tags that have actual content
                    $("p").each((_, el) => {
                        const pText = $(el).text().trim();

                        // Only index if paragraph is long enough to be a rule/description
                        // and isn't just the title again or empty
                        if (
                            pText.length > 10 &&
                            pText !== word &&
                            !pText.includes(ERR_404)
                        ) {
                            index.push({
                                t: pText,
                                l: relativePath,
                                type: "content",
                                parent: word, // Keep reference to which word this belongs to
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
    console.log(
        `Done! Indexed ${index.length} total entries (Headwords + Paragraphs).`,
    );
}

build();
