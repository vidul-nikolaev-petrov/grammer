const express = require("express");
const dictionary = require("./dictionaryData");

const app = express();
const PORT = 3000;
const MIRROR_BASE_URL = "http://127.0.0.1:8080/rechnik";

const STYLES = `
    body { font-family: 'Segoe UI', Tahoma, sans-serif; max-width: 700px; margin: 0 auto; padding: 40px 20px; background: #f9f9f9; color: #2c3e50; }
    .card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    h1 { color: #2980b9; margin-top: 0; text-align: center; font-size: 2.5rem; }
    form { display: flex; margin: 20px 0; gap: 10px; }
    input { flex: 1; padding: 15px 20px; font-size: 1.1rem; border: 2px solid #eee; border-radius: 30px; outline: none; transition: 0.3s; }
    input:focus { border-color: #3498db; box-shadow: 0 0 8px rgba(52,152,219,0.2); }
    button { padding: 0 25px; background: #3498db; color: white; border: none; border-radius: 30px; cursor: pointer; font-weight: 600; }
    button:hover { background: #2980b9; }
    .result { padding: 15px; border-bottom: 1px solid #eee; display: block; text-decoration: none; transition: 0.2s; }
    .result:hover { background: #fdfdfd; transform: translateX(5px); }
    .result-title { font-size: 1.3rem; color: #2c3e50; font-weight: bold; }
    .result-url { font-size: 0.8rem; color: #95a5a6; display: block; margin-top: 4px; }
    .back { color: #7f8c8d; text-decoration: none; font-size: 0.9rem; margin-bottom: 20px; display: inline-block; }
`;

app.get("/", (req, res) => {
    res.send(`
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>БЕРОН: Локално търсене</title><style>${STYLES}</style></head>
        <body>
            <div class="card">
                <h1>БЕРОН</h1>
                <form action="/search" method="GET">
                    <input name="q" placeholder="Търси дума..." autofocus required />
                    <button type="submit">Търси</button>
                </form>
            </div>
        </body>
        </html>
    `);
});

app.get("/search", (req, res) => {
    const q = (req.query.q || "").toLowerCase();
    const results = dictionary
        .filter((item) => item.t.toLowerCase().includes(q))
        .slice(0, 40);

    res.send(`
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>Резултати: ${q}</title><style>${STYLES}</style></head>
        <body>
            <a href="/" class="back">← Назад</a>
            <div class="card">
                <h2>Намерени думи за "<b>${q}</b>"</h2>
                <div>
                    ${
                        results
                            .map((r) => {
                                const fileName = r.l.replace(/.*\/(\d+)\.html$/, "$1");
                                // Map the local path to your 8080 server URL
                                const fullUrl = `${MIRROR_BASE_URL}/${fileName}`;
                                return `
                            <a href="${fullUrl}" target="_blank" class="result">
                                <span class="result-title">${r.t}</span>
                                <span class="result-url">${fullUrl}</span>
                            </a>
                        `;
                            })
                            .join("") || "<p>Няма намерени резултати.</p>"
                    }
                </div>
            </div>
        </body>
        </html>
    `);
});

app.listen(PORT, () =>
    console.log(`Pretty Search running at http://localhost:${PORT}`),
);
