/** Shared primary nav for ControlSift static pages (header only). */
(function () {
  const links = [
    { href: "index.html", label: "Home" },
    { href: "results.html", label: "Results" },
    { href: "capstone/index.html", label: "Capstone" },
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
    enhanceBrand();
    renderNav();
    enhanceFooter();
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
