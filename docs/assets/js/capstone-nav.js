/** Secondary nav for the MMC / DeepMind capstone cluster. */
(function () {
  const groups = [
    {
      title: "Submit",
      links: [
        { href: "index.html", label: "Capstone hub" },
        { href: "next-steps.html", label: "Status" },
        { href: "submission.html", label: "Submission package" },
        { href: "gclp-checklist.html", label: "GCLP checklist" },
      ],
    },
    {
      title: "Artifacts",
      links: [
        { href: "report.html", label: "8-page-or-less report" },
        { href: "slides.html", label: "8-slide deck" },
        { href: "paper.html", label: "Research paper" },
        { href: "research-sources.html", label: "Research sources" },
        { href: "deliverables/index.html", label: "Weekly labs" },
      ],
    },
    {
      title: "Research & program context",
      links: [
        { href: "problem-impact.html", label: "Problem & impact" },
        { href: "methods-evidence.html", label: "Methods & evidence" },
        { href: "implementation-plan.html", label: "Implementation" },
        { href: "responsible-innovation.html", label: "Responsible AI" },
        { href: "un-sdg.html", label: "UN SDG alignment" },
        { href: "curriculum.html", label: "Curriculum map" },
        { href: "reflection.html", label: "Reflection" },
      ],
    },
  ];

  const quick = [
    { href: "index.html", label: "Hub" },
    { href: "report.html", label: "Report" },
    { href: "slides.html", label: "Slides" },
    { href: "research-sources.html", label: "Sources" },
    { href: "submission.html", label: "Package" },
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

  function injectProjectMapStyles() {
    if (document.getElementById("capstone-project-map-styles")) return;
    const style = document.createElement("style");
    style.id = "capstone-project-map-styles";
    style.textContent = `
      .capstone-menu summary::after { content: none !important; }
      .capstone-menu-trigger {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        width: 100%;
        padding: 0.95rem 1rem;
        border: 1px solid var(--line);
        background: linear-gradient(135deg, rgba(127,255,178,.065), transparent 58%), var(--panel);
        transition: border-color .18s ease, background .18s ease, transform .18s ease;
      }
      .capstone-menu-trigger:hover,
      .capstone-menu[open] .capstone-menu-trigger {
        color: var(--fg);
        border-color: rgba(127,255,178,.45);
        background: linear-gradient(135deg, rgba(127,255,178,.11), transparent 62%), var(--panel-2);
      }
      .capstone-menu-copy { display: grid; gap: .18rem; min-width: 0; }
      .capstone-menu-eyebrow {
        font-family: var(--font-mono);
        font-size: .66rem;
        letter-spacing: .08em;
        text-transform: uppercase;
        color: var(--accent-2);
      }
      .capstone-menu-label {
        font-family: var(--font-sans);
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: -.01em;
        color: var(--fg);
        text-transform: none;
      }
      .capstone-menu-meta {
        font-family: var(--font-sans);
        font-size: var(--text-xs);
        font-weight: 400;
        letter-spacing: 0;
        text-transform: none;
        color: var(--muted);
      }
      .capstone-menu-icon {
        position: relative;
        flex: 0 0 2rem;
        width: 2rem;
        height: 2rem;
        border: 1px solid var(--line);
        background: rgba(127,255,178,.035);
      }
      .capstone-menu-icon::before,
      .capstone-menu-icon::after {
        content: "";
        position: absolute;
        left: 50%;
        top: 50%;
        width: .72rem;
        height: 1px;
        background: var(--accent);
        transform: translate(-50%, -50%);
        transition: opacity .18s ease, transform .18s ease;
      }
      .capstone-menu-icon::after { transform: translate(-50%, -50%) rotate(90deg); }
      .capstone-menu[open] .capstone-menu-icon::after { opacity: 0; }
      .capstone-menu-panel {
        margin-top: .55rem;
        padding: 1.1rem;
        background: linear-gradient(145deg, rgba(127,255,178,.045), transparent 54%), var(--panel);
        box-shadow: 0 14px 40px rgba(0,0,0,.18);
      }
      .capstone-menu-group a {
        display: inline-block;
        padding: .16rem 0;
      }
      @media (max-width: 560px) {
        .capstone-menu-meta { line-height: 1.45; }
        .capstone-menu-trigger { align-items: flex-start; }
      }
    `;
    document.head.appendChild(style);
  }

  document.addEventListener("DOMContentLoaded", () => {
    const host = document.querySelector("[data-capstone-nav]");
    if (!host) return;
    injectProjectMapStyles();

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
      `<summary class="capstone-menu-trigger">` +
      `<span class="capstone-menu-copy">` +
      `<span class="capstone-menu-eyebrow">Project map</span>` +
      `<span class="capstone-menu-label">Explore the full capstone</span>` +
      `<span class="capstone-menu-meta">Report &middot; research &middot; assurance &middot; program map &middot; weekly labs</span>` +
      `</span>` +
      `<span class="capstone-menu-icon" aria-hidden="true"></span>` +
      `</summary>` +
      `<div class="capstone-menu-panel">${menuHtml}</div>` +
      `</details>`;
  });
})();
