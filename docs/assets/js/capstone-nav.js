/** Secondary nav for MMC / DeepMind capstone cluster (footer-linked only). */
(function () {
  const links = [
    { href: "index.html", label: "Hub" },
    { href: "next-steps.html", label: "Status" },
    { href: "deliverables/index.html", label: "Weekly Labs" },
    { href: "paper.html", label: "Research Paper" },
    { href: "gclp-checklist.html", label: "GCLP Checklist" },
    { href: "un-sdg.html", label: "UN SDG" },
    { href: "curriculum.html", label: "Curriculum" },
    { href: "problem-impact.html", label: "Problem & Impact" },
    { href: "methods-evidence.html", label: "Methods" },
    { href: "implementation-plan.html", label: "Implementation" },
    { href: "report.html", label: "Report" },
    { href: "slides.html", label: "Slides" },
    { href: "video-script.html", label: "Video Script" },
    { href: "responsible-innovation.html", label: "Responsible AI" },
    { href: "reflection.html", label: "Reflection" },
    { href: "submission.html", label: "Submission" },
  ];

  function currentFile() {
    return (window.location.pathname.split("/").pop() || "index.html").toLowerCase();
  }

  function inDeliverables() {
    return window.location.pathname.replace(/\\/g, "/").includes("/deliverables/");
  }

  document.addEventListener("DOMContentLoaded", () => {
    const host = document.querySelector("[data-capstone-nav]");
    if (!host) return;
    const file = currentFile();
    const nested = inDeliverables();
    host.innerHTML = links
      .map((link) => {
        let href = link.href;
        if (nested) {
          href = link.href.startsWith("deliverables/")
            ? link.href.replace(/^deliverables\//, "")
            : "../" + link.href;
        }
        const name = link.href.toLowerCase();
        const active =
          (!nested && (file === name || (file === "index.html" && name === "index.html"))) ||
          (nested && name === "deliverables/index.html");
        return `<a href="${href}"${active ? ' aria-current="page"' : ""}>${link.label}</a>`;
      })
      .join("");
  });
})();
