/** Shared primary nav for ControlSift static pages (header only). */
(function () {
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
      '<span class="brand-parent">evidence triage research</span>';
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

    host.innerHTML = items.join("");
  }

  function enhanceFooter() {
    const wrap = document.querySelector(".site-footer .wrap");
    if (!wrap || wrap.dataset.chrome === "1") return;
    wrap.dataset.chrome = "1";
    // Keep footer minimal: strip injected / redundant nav links (Capstone lives in header).
    const linksHost = wrap.querySelector(".footer-links");
    if (linksHost) linksHost.remove();
    Array.from(wrap.querySelectorAll(":scope > a")).forEach((a) => a.remove());
  }

  function boot() {
    enhanceBrand();
    renderNav();
    enhanceFooter();
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
