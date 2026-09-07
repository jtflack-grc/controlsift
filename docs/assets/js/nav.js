/** Shared primary nav for ControlSift static pages (header only). */
(function () {
  const links = [
    { href: "index.html", label: "Home" },
    { href: "results.html", label: "Results" },
    { href: "capstone/index.html", label: "Capstone" },
  ];

  const FONT_HREF =
    "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap";

  function pathNormalized() {
    return window.location.pathname.replace(/\\/g, "/");
  }

  function prefix() {
    const path = pathNormalized();
    if (path.includes("/capstone/deliverables/")) return "../../";
    if (path.includes("/capstone/") || path.includes("/assurance/")) return "../";
    return "";
  }

  function currentFile() {
    const parts = pathNormalized().split("/");
    return parts[parts.length - 1] || "index.html";
  }

  function pathIncludes(seg) {
    return pathNormalized().includes(seg);
  }

  function ensureFonts() {
    if (document.getElementById("cs-fonts")) return;
    const pre1 = document.createElement("link");
    pre1.rel = "preconnect";
    pre1.href = "https://fonts.googleapis.com";
    const pre2 = document.createElement("link");
    pre2.rel = "preconnect";
    pre2.href = "https://fonts.gstatic.com";
    pre2.crossOrigin = "anonymous";
    const link = document.createElement("link");
    link.id = "cs-fonts";
    link.rel = "stylesheet";
    link.href = FONT_HREF;
    document.head.appendChild(pre1);
    document.head.appendChild(pre2);
    document.head.appendChild(link);
  }

  function enhanceBrand() {
    const brand = document.querySelector(".nav > .brand, .site-header .brand");
    if (!brand || brand.dataset.chrome === "1") return;
    brand.dataset.chrome = "1";
    const home = prefix() + "index.html";
    brand.setAttribute("href", home);
    brand.setAttribute("aria-label", "ControlSift home");
    brand.textContent = "ControlSift";
  }

  function renderNav() {
    const host = document.querySelector("[data-site-nav]");
    if (!host) return;
    const p = prefix();
    const file = currentFile();
    const inAssurance = file === "assurance.html" || pathIncludes("/assurance/");
    const inCapstone = pathIncludes("/capstone/");

    const items = links.map((link) => {
      const href = p + link.href;
      let active =
        file === link.href ||
        (link.href === "index.html" && file === "" && !inCapstone && !inAssurance);
      if (link.href === "capstone/index.html" && inCapstone) active = true;
      if (link.href === "index.html" && (inCapstone || inAssurance)) active = false;
      return `<li><a href="${href}"${active ? ' aria-current="page"' : ""}>${link.label}</a></li>`;
    });

    host.innerHTML = items.join("");
  }

  function enhanceFooter() {
    const wrap = document.querySelector(".site-footer .wrap");
    if (!wrap || wrap.dataset.chrome === "1") return;
    wrap.dataset.chrome = "1";
    const linksHost = wrap.querySelector(".footer-links");
    if (linksHost) linksHost.remove();
    Array.from(wrap.querySelectorAll(":scope > a")).forEach((a) => a.remove());
    // Strip any leftover portfolio / mothership anchors that older pages may still hardcode.
    Array.from(wrap.querySelectorAll("a")).forEach((a) => {
      const href = (a.getAttribute("href") || "").toLowerCase();
      const text = (a.textContent || "").toLowerCase();
      if (
        href.includes("/portfolio") ||
        text.includes("mothership") ||
        text.includes("portfolio") ||
        text.includes("i on grc")
      ) {
        a.remove();
      }
    });
  }

  function boot() {
    ensureFonts();
    enhanceBrand();
    renderNav();
    enhanceFooter();
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
