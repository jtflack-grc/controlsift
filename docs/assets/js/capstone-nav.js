/** Secondary nav for MMC / DeepMind capstone cluster — compact dropdown, not a link farm. */
(function () {
  const groups = [
    {
      title: "Submit",
      links: [
        { href: "index.html", label: "Hub" },
        { href: "next-steps.html", label: "Status" },
        { href: "submission.html", label: "Submission" },
        { href: "video-script.html", label: "Video script" },
        { href: "gclp-checklist.html", label: "GCLP checklist" },
      ],
    },
    {
      title: "Artifacts",
      links: [
        { href: "report.html", label: "Report" },
        { href: "slides.html", label: "Slides" },
        { href: "paper.html", label: "Research paper" },
        { href: "deliverables/index.html", label: "Weekly labs" },
      ],
    },
    {
      title: "Context",
      links: [
        { href: "un-sdg.html", label: "UN SDG" },
        { href: "curriculum.html", label: "Curriculum" },
        { href: "problem-impact.html", label: "Problem & impact" },
        { href: "methods-evidence.html", label: "Methods" },
        { href: "implementation-plan.html", label: "Implementation" },
        { href: "responsible-innovation.html", label: "Responsible AI" },
        { href: "reflection.html", label: "Reflection" },
      ],
    },
  ];

  const quick = [
    { href: "index.html", label: "Hub" },
    { href: "report.html", label: "Report" },
    { href: "slides.html", label: "Slides" },
    { href: "video-script.html", label: "Video" },
    { href: "submission.html", label: "Submit" },
  ];

  function currentFile() {
    return (window.location.pathname.split("/").pop() || "index.html").toLowerCase();
  }

  function inDeliverables() {
    return window.location.pathname.replace(/\\/g, "/").includes("/deliverables/");
  }

  function resolveHref(href, nested) {
    if (!nested) return href;
    if (href.startsWith("deliverables/")) return href.replace(/^deliverables\//, "");
    return "../" + href;
  }

  function isActive(href, file, nested) {
    const name = href.toLowerCase();
    if (nested) return name === "deliverables/index.html";
    return file === name || (file === "index.html" && name === "index.html");
  }

  document.addEventListener("DOMContentLoaded", () => {
    const host = document.querySelector("[data-capstone-nav]");
    if (!host) return;
    const file = currentFile();
    const nested = inDeliverables();

    const quickHtml = quick
      .map((link) => {
        const href = resolveHref(link.href, nested);
        const active = isActive(link.href, file, nested);
        return `<a class="capstone-pill"${active ? ' aria-current="page"' : ""} href="${href}">${link.label}</a>`;
      })
      .join("");

    const menuHtml = groups
      .map((group) => {
        const items = group.links
          .map((link) => {
            const href = resolveHref(link.href, nested);
            const active = isActive(link.href, file, nested);
            return `<li><a href="${href}"${active ? ' aria-current="page"' : ""}>${link.label}</a></li>`;
          })
          .join("");
        return `<div class="capstone-menu-group"><p class="capstone-menu-title">${group.title}</p><ul>${items}</ul></div>`;
      })
      .join("");

    host.classList.add("capstone-nav--compact");
    host.innerHTML =
      `<div class="capstone-quick" role="navigation" aria-label="Capstone shortcuts">${quickHtml}</div>` +
      `<details class="capstone-menu">` +
      `<summary>All capstone pages</summary>` +
      `<div class="capstone-menu-panel">${menuHtml}</div>` +
      `</details>`;
  });
})();
