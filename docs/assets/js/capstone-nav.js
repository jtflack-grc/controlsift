/** Secondary nav for MMC / DeepMind capstone cluster (footer-linked only). */
(function () {
  const links = [
    { href: "index.html", label: "Hub" },
    { href: "un-sdg.html", label: "UN SDG" },
    { href: "curriculum.html", label: "Curriculum" },
    { href: "problem-impact.html", label: "Problem & Impact" },
    { href: "methods-evidence.html", label: "Methods" },
    { href: "responsible-innovation.html", label: "Responsible AI" },
    { href: "reflection.html", label: "Reflection" },
    { href: "submission.html", label: "Submission" },
  ];

  document.addEventListener("DOMContentLoaded", () => {
    const host = document.querySelector("[data-capstone-nav]");
    if (!host) return;
    const file = (window.location.pathname.split("/").pop() || "index.html").toLowerCase();
    host.innerHTML = links
      .map((link) => {
        const name = link.href.toLowerCase();
        const active =
          file === name ||
          (file === "" && name === "index.html") ||
          (file === "index.html" && name === "index.html");
        return `<a href="${link.href}"${active ? ' aria-current="page"' : ""}>${link.label}</a>`;
      })
      .join("");
  });
})();
