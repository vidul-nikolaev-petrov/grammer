const puppeteer = require("puppeteer");
const fs = require("fs-extra");
const path = require("path");

const BASE = "https://beron.mon.bg/rechnik/";
const OUT_DIR = "./mirror";
const MAX = 4000;

function saveFile(url, buffer, contentType) {
    const u = new URL(url);

    let filePath = path.join(OUT_DIR, u.hostname, u.pathname);

    if (filePath.endsWith("/")) filePath += "index";

    // guess extension if missing
    if (!path.extname(filePath)) {
        if (contentType?.includes("text/html")) filePath += ".html";
        else if (contentType?.includes("text/css")) filePath += ".css";
        else if (contentType?.includes("javascript")) filePath += ".js";
        else if (contentType?.includes("image/png")) filePath += ".png";
        else if (contentType?.includes("image/jpeg")) filePath += ".jpg";
    }

    fs.ensureDirSync(path.dirname(filePath));
    fs.writeFileSync(filePath, buffer);
}

(async () => {
    const browser = await puppeteer.launch({ headless: "new" });

    console.log("Crawler started...");

    for (let i = 0; i <= MAX; i++) {
        const url = `${BASE}${i}`;

        console.log("→ Crawling:", url);

        const page = await browser.newPage();

        const responses = [];

        // 🎯 INTERCEPT ALL NETWORK RESPONSES
        page.on("response", async (res) => {
            try {
                const reqUrl = res.url();
                const ct = res.headers()["content-type"] || "";

                const buffer = await res.buffer();
                saveFile(reqUrl, buffer, ct);

                responses.push(reqUrl);
            } catch {}
        });

        try {
            const res = await page.goto(url, {
                waitUntil: "networkidle2",
                timeout: 3000,
            });

            if (!res || res.status() === 404) {
                console.log("   skip (404)");
                await page.close();
                continue;
            }

            const html = await page.content();

            const filePath = path.join(
                OUT_DIR,
                "beron.mon.bg",
                "rechnik",
                `${i}.html`,
            );

            await fs.ensureDir(path.dirname(filePath));
            await fs.writeFile(filePath, html);

            console.log("   saved HTML + assets:", i);
        } catch (err) {
            console.log("❌ Failed:", url, err.message);
        }

        await page.close();
    }

    await browser.close();
    console.log("Done.");
})();
