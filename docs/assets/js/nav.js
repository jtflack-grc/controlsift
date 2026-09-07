/** Shared primary nav + mothership chrome for ControlSift static pages. */
(function () {
  const PORTFOLIO_URL = "https://jtflack-grc.github.io/portfolio/";
  const GITHUB_ORG = "https://github.com/jtflack-grc";

  const links = [
    { href: "index.html", label: "Home" },
    { href: "failure-lab.html", label: "Failure Lab" },
    { href: "results.html", label: "Results" },
    { href: "methods.html", label: "Methods" },
    { href: "assurance.html", label: "Assurance" },
    { href: "reproduce.html", label: "Reproduce" },
    { href: "capstone/index.html", label: "MMC Capstone" },
  ];

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

  function enhanceBrand() {
    const brand = document.querySelector(".nav > .brand, .site-header .brand");
    if (!brand || brand.dataset.chrome === "1") return;
    brand.dataset.chrome = "1";
    const home = prefix() + "index.html";
    brand.setAttribute("href", home);
    brand.setAttribute("aria-label", "ControlSift home");
    brand.innerHTML =
      '<span class="brand-mark">ControlSift</span>' +
      '<span class="brand-parent">i on GRC · research</span>';
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
      let active = file === link.href || (link.href === "index.html" && file === "" && !inCapstone && !inAssurance);
      if (link.href === "assurance.html" && inAssurance) active = true;
      if (link.href === "capstone/index.html" && inCapstone) active = true;
      if (link.href === "index.html" && (inCapstone || inAssurance)) active = false;
      return `<li><a href="${href}"${active ? ' aria-current="page"' : ""}>${link.label}</a></li>`;
    });

    items.push(
      `<li><a class="nav-external" href="${PORTFOLIO_URL}" rel="noopener">Portfolio<span class="ext" aria-hidden="true">↗</span></a></li>`
    );

    host.innerHTML = items.join("");
  }

  function enhanceFooter() {
    const wrap = document.querySelector(".site-footer .wrap");
    if (!wrap || wrap.dataset.chrome === "1") return;
    wrap.dataset.chrome = "1";

    let linksHost = wrap.querySelector(".footer-links");
    if (!linksHost) {
      linksHost = document.createElement("div");
      linksHost.className = "footer-links";
      // Move existing trailing anchors into the links cluster when present.
      Array.from(wrap.querySelectorAll(":scope > a")).forEach((a) => linksHost.appendChild(a));
      wrap.appendChild(linksHost);
    }

    if (!linksHost.querySelector("[data-portfolio-link]")) {
      const a = document.createElement("a");
      a.href = PORTFOLIO_URL;
      a.rel = "noopener";
      a.dataset.portfolioLink = "1";
      a.textContent = "i on GRC portfolio ↗";
      linksHost.appendChild(a);
    }

    if (!linksHost.querySelector("[data-github-link]")) {
      const g = document.createElement("a");
      g.href = GITHUB_ORG;
      g.rel = "noopener";
      g.dataset.githubLink = "1";
      g.textContent = "GitHub ↗";
      linksHost.appendChild(g);
    }
  }

  function boot() {
    enhanceBrand();
    renderNav();
    enhanceFooter();
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
