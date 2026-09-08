/** Shared primary nav and first-visit orientation for ControlSift static pages. */
(function () {
  const WELCOME_KEY = "controlsift_welcome_seen_v3";
  const links = [
    { href: "index.html", label: "Home" },
    { href: "results.html", label: "Results" },
    { href: "methods.html", label: "Methods" },
    { href: "failure-lab.html", label: "Failure Lab" },
    { href: "assurance.html", label: "Assurance" },
    { href: "reproduce.html", label: "Reproduce" },
    { href: "capstone/index.html", label: "Capstone" },
  ];

  function pathNormalized() { return window.location.pathname.replace(/\\/g, "/"); }
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

  function renderChrome() {
    const p = prefix();
    const path = pathNormalized();
    const file = currentFile();
    const inCapstone = path.includes("/capstone/");
    const inAssurance = file === "assurance.html" || path.includes("/assurance/");

    const brand = document.querySelector(".nav > .brand, .site-header .brand");
    if (brand) {
      brand.href = p + "index.html";
      brand.setAttribute("aria-label", "ControlSift home");
      brand.textContent = "ControlSift";
    }

    const host = document.querySelector("[data-site-nav]");
    if (host) {
      host.innerHTML = links.map((link) => {
        let active = file === link.href;
        if (link.href === "index.html" && file === "index.html" && !inCapstone && !inAssurance) active = true;
        if (link.href === "assurance.html" && inAssurance) active = true;
        if (link.href === "capstone/index.html" && inCapstone) active = true;
        if (link.href === "index.html" && (inCapstone || inAssurance)) active = false;
        return `<li><a href="${p + link.href}"${active ? ' aria-current="page"' : ""}>${link.label}</a></li>`;
      }).join("");
    }
  }

  function buildModal() {
    let modal = document.getElementById("welcome-modal");
    if (modal) return modal;
    const p = prefix();
    modal = document.createElement("div");
    modal.id = "welcome-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-labelledby", "welcome-modal-title");
    modal.hidden = true;
    modal.innerHTML = `
      <div class="welcome-modal__backdrop" data-welcome-dismiss tabindex="-1" aria-hidden="true"></div>
      <div class="welcome-modal__card" role="document" style="max-height:90vh;overflow:auto;">
        <p class="welcome-modal__brand">ControlSift</p>
        <h2 id="welcome-modal-title">Start here - no AI background required.</h2>
        <p>ControlSift asks a simple security question: when a reviewer receives a document, does it actually prove the control worked, or is it only relevant-looking paperwork?</p>
        <div style="border-left:2px solid #38e881;padding-left:0.9rem;margin:0 0 1rem;line-height:1.5;">
          <p style="margin:0 0 0.45rem;"><strong>Benchmark</strong> = a fixed exam for a model.</p>
          <p style="margin:0 0 0.45rem;"><strong>Gemma</strong> = the small language model being tested.</p>
          <p style="margin:0;"><strong>Macro F1</strong> = a 0-to-1 score that gives all five labels equal weight; higher is better.</p>
        </div>
        <p><strong>What happened:</strong> the hardened classical experiments and the Gemma experiments were completed on different dataset versions. Within Gemma v1.0, few-shot beat QLoRA. Cross-version classical-vs-Gemma scores are shown only as descriptive context, not as a controlled same-benchmark contest.</p>
        <p class="welcome-modal__note">Synthetic research benchmark / human judgment stays authoritative</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="${p}index.html#plain-english" data-welcome-route>Plain-English tour</a>
          <a class="btn btn-secondary" href="${p}capstone/index.html" data-welcome-route>Capstone hub</a>
          <button type="button" class="btn btn-secondary" id="welcome-modal-continue" data-welcome-dismiss>Skip intro</button>
        </div>
      </div>`;
    document.body.appendChild(modal);
    return modal;
  }

  function bootModal() {
    let seen = false;
    try { seen = localStorage.getItem(WELCOME_KEY) === "1"; } catch (_) {}
    if (seen) return;
    const modal = buildModal();
    function markSeen() { try { localStorage.setItem(WELCOME_KEY, "1"); } catch (_) {} }
    function close() { markSeen(); modal.hidden = true; document.body.classList.remove("welcome-modal-open"); }
    modal.querySelectorAll("[data-welcome-dismiss]").forEach((el) => el.addEventListener("click", (e) => { e.preventDefault(); close(); }));
    modal.querySelectorAll("[data-welcome-route]").forEach((el) => el.addEventListener("click", markSeen));
    modal.hidden = false;
    document.body.classList.add("welcome-modal-open");
    const btn = modal.querySelector("#welcome-modal-continue");
    if (btn) btn.focus();
    document.addEventListener("keydown", (e) => { if (!modal.hidden && e.key === "Escape") close(); }, { once: false });
  }

  document.addEventListener("DOMContentLoaded", function () {
    renderChrome();
    bootModal();
  });
})();
