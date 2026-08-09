/** Secondary nav for assurance / responsible-AI cluster. */
(function () {
  const links = [
    { href: "../assurance.html", label: "Overview" },
    { href: "protocol.html", label: "Protocol" },
    { href: "data-card.html", label: "Data Card" },
    { href: "model-card.html", label: "Model Card" },
    { href: "risk-register.html", label: "Risk Register" },
    { href: "limitations.html", label: "Limitations" },
    { href: "intended-use.html", label: "Intended Use" },
    { href: "human-review.html", label: "Human Review" },
  ];

  document.addEventListener("DOMContentLoaded", () => {
    const host = document.querySelector("[data-assurance-nav]");
    if (!host) return;
    const file = (window.location.pathname.split("/").pop() || "").toLowerCase();
    const isHub = file === "assurance.html";
    const items = isHub
      ? [
          { href: "assurance.html", label: "Overview" },
          { href: "assurance/protocol.html", label: "Protocol" },
          { href: "assurance/data-card.html", label: "Data Card" },
          { href: "assurance/model-card.html", label: "Model Card" },
          { href: "assurance/risk-register.html", label: "Risk Register" },
          { href: "assurance/limitations.html", label: "Limitations" },
          { href: "assurance/intended-use.html", label: "Intended Use" },
          { href: "assurance/human-review.html", label: "Human Review" },
        ]
      : links;
    host.innerHTML = items
      .map((link) => {
        const name = link.href.split("/").pop();
        const active =
          (isHub && link.label === "Overview") ||
          (!isHub && file === name);
        return `<a href="${link.href}"${active ? ' aria-current="page"' : ""}>${link.label}</a>`;
      })
      .join("");
  });
})();
