import { refMap } from "./refs.js";

document.addEventListener("click", (e) => {
    const link = e.target.closest("a");
    if (!link) return;

    const href = link.getAttribute("href");

    if (href && href.startsWith("#")) {
        const targetId = href.replace("#", "");
        const localElement = document.getElementById(targetId);

        if (localElement) {
            e.preventDefault();
            localElement.scrollIntoView();
        } else if (refMap[targetId]) {
            e.preventDefault();
            window.location.href = refMap[targetId] + "#" + targetId;
        }
    }
});

const startPrefetching = () => {
    const links = document.querySelectorAll("a[href]");
    const filesToPrefetch = new Set();
    const currentFile = window.location.pathname.split("/").pop();

    links.forEach((link) => {
        const href = link.getAttribute("href");
        let targetFile = null;

        if (href.startsWith("#")) {
            const targetId = href.replace("#", "");
            targetFile =
                typeof refMap !== "undefined" ? refMap[targetId] : null;
        } else if (href.endsWith(".html")) {
            targetFile = href.split("#")[0];
        }

        if (
            targetFile &&
            targetFile !== currentFile &&
            targetFile !== "index.html"
        ) {
            filesToPrefetch.add(targetFile);
        }
    });

    filesToPrefetch.forEach((file) => {
        const linkTag = document.createElement("link");
        linkTag.rel = "prefetch";
        linkTag.href = file;
        linkTag.as = "document";
        document.head.appendChild(linkTag);

        if (!linkTag.relList?.supports("prefetch")) {
            fetch(file, { priority: "low", mode: "no-cors" }).catch(() => {});
        }
    });
};

const initSamps = () => {
    const allSamps = document.querySelectorAll(".samp");
    let currentGroup = [];

    allSamps.forEach((samp) => {
        currentGroup.push(samp);
        const next = samp.nextElementSibling;

        if (!next || !next.classList.contains("samp")) {
            const [first, ...rest] = currentGroup;

            if (rest.length > 0) {
                first.classList.add("samp-clickable");

                const indicator = document.createElement("div");
                indicator.className = "samp-toggle";
                indicator.textContent = "+";
                first.appendChild(indicator);

                first.onclick = () => {
                    const isExpanding = indicator.textContent === "+";

                    rest.forEach((el) => {
                        el.classList.toggle("js-expanded", isExpanding);
                    });

                    indicator.textContent = isExpanding ? "−" : "+";
                };
            }
            currentGroup = [];
        }
    });
};

const topBtn = () => {
    const topBtn = document.getElementById("backToTop");

    if (topBtn) {
        window.addEventListener(
            "scroll",
            () => {
                const isVisible = window.scrollY > 300;
                topBtn.style.display = isVisible ? "block" : "none";
            },
            { passive: true },
        );

        topBtn.onclick = () => {
            window.scrollTo({ top: 0 });
        };
    }
};

const runAll = () => {
    topBtn();
    initSamps();
    setTimeout(startPrefetching, 100);
};

if (document.readyState !== "loading") {
    runAll();
} else {
    document.addEventListener("DOMContentLoaded", runAll);
}


