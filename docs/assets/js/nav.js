/** Shared primary nav for ControlSift static pages. */
(function () {
  const links = [
    { href: "index.html", label: "Home" },
    { href: "failure-lab.html", label: "Failure Lab" },
    { href: "results.html", label: "Results" },
    { href: "methods.html", label: "Methods" },
    { href: "assurance.html", label: "Assurance" },
    { href: "reproduce.html", label: "Reproduce" },
  ];

  function prefix() {
    const path = window.location.pathname.replace(/\\/g, "/");
    if (path.includes("/capstone/") || path.includes("/assurance/")) return "../";
    return "";
  }

  function currentFile() {
    const path = window.location.pathname.replace(/\\/g, "/");
    const parts = path.split("/");
    return parts[parts.length - 1] || "index.html";
  }

  function render() {
    const host = document.querySelector("[data-site-nav]");
    if (!host) return;
    const p = prefix();
    const file = currentFile();
    const inAssurance =
      file === "assurance.html" || pathIncludes("/assurance/");
    host.innerHTML = links
      .map((link) => {
        const href = p + link.href;
        let active = file === link.href;
        if (link.href === "assurance.html" && inAssurance) active = true;
        return `<li><a href="${href}"${active ? ' aria-current="page"' : ""}>${link.label}</a></li>`;
      })
      .join("");
  }

  function pathIncludes(seg) {
    return window.location.pathname.replace(/\\/g, "/").includes(seg);
  }

  document.addEventListener("DOMContentLoaded", render);
})();
