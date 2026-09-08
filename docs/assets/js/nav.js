/** Shared primary nav and first-visit orientation for ControlSift static pages. */
(function () {
  const WELCOME_KEY = "controlsift_welcome_seen_v2";

  const links = [
    { href: "index.html", label: "Home" },
    { href: "results.html", label: "Results" },
    { href: "methods.html", label: "Methods" },
    { href: "failure-lab.html", label: "Failure Lab" },
    { href: "assurance.html", label: "Assurance" },
    { href: "reproduce.html", label: "Reproduce" },
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
    brand.setAttribute("href", prefix() + "index.html");
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
      let active = file === link.href;
      if (link.href === "index.html" && file === "index.html" && !inCapstone && !inAssurance) active = true;
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
    const linksHost = wrap.querySelector(".footer-links");
    if (linksHost) linksHost.remove();
    Array.from(wrap.querySelectorAll(":scope > a")).forEach((a) => a.remove());
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

  function ensureWelcomeModal() {
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
      <div class="welcome-modal__card" role="document" style="font-family:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'SF Pro Text','Helvetica Neue',Arial,sans-serif !important;background:#0a1510;border:2px solid #7fffb2;padding:1.5rem 1.45rem;color:#e8f4ec;max-height:90vh;overflow:auto;">
        <p class="welcome-modal__brand" style="font-family:'IBM Plex Mono',monospace !important;color:#7fffb2;margin:0 0 0.55rem;font-size:clamp(1.85rem,5vw,2.35rem);font-weight:600;">ControlSift</p>
        <h2 id="welcome-modal-title" style="font-family:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'SF Pro Text','Helvetica Neue',Arial,sans-serif !important;color:#fff;margin:0 0 0.75rem;font-size:clamp(1.2rem,3vw,1.45rem);font-weight:500;">Start here — no AI background required.</h2>
        <p style="font-family:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'SF Pro Text','Helvetica Neue',Arial,sans-serif !important;color:#c8e6d2;line-height:1.55;margin:0 0 0.85rem;">
          ControlSift asks a simple security question: when someone hands a reviewer a document, does it actually prove the control worked — or is it only paperwork that sounds relevant?
        </p>
        <div style="border-left:2px solid #38e881;padding-left:0.9rem;margin:0 0 1rem;color:#c8e6d2;line-height:1.5;font-size:0.94rem;">
          <p style="margin:0 0 0.45rem;"><strong style="color:#fff;">Benchmark</strong> = a fixed exam for the models.</p>
          <p style="margin:0 0 0.45rem;"><strong style="color:#fff;">Gemma</strong> = the small language model being tested.</p>
          <p style="margin:0;"><strong style="color:#fff;">Macro F1</strong> = a 0–1 score that gives all five evidence labels equal weight; higher is better.</p>
        </div>
        <p style="font-family:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'SF Pro Text','Helvetica Neue',Arial,sans-serif !important;color:#e8f4ec;line-height:1.55;margin:0 0 0.85rem;">
          <strong>Headline:</strong> the classic word-based baseline beat the small language-model approaches. ControlSift keeps that negative result instead of manufacturing an AI win.
        </p>
        <p class="welcome-modal__note" style="font-family:'IBM Plex Mono',monospace !important;color:#38e881;font-size:0.72rem;letter-spacing:0.04em;text-transform:uppercase;margin:0 0 1rem;">Synthetic research benchmark · human judgment stays authoritative</p>
        <div class="cta-row" style="display:flex;flex-wrap:wrap;gap:0.65rem;">
          <a class="btn btn-primary" href="${p}index.html#plain-english" data-welcome-route style="font-family:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'SF Pro Text','Helvetica Neue',Arial,sans-serif !important;background:#7fffb2;color:#021008;border:1px solid #7fffb2;padding:0.75rem 1.15rem;font-weight:600;text-decoration:none;">Plain-English tour</a>
          <a class="btn btn-secondary" href="${p}capstone/index.html" data-welcome-route style="font-family:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'SF Pro Text','Helvetica Neue',Arial,sans-serif !important;border:1px solid #2a2e2a;color:#e8f4ec;padding:0.75rem 1.15rem;font-weight:600;text-decoration:none;">Capstone hub</a>
          <button type="button" class="btn btn-secondary" id="welcome-modal-continue" data-welcome-dismiss style="font-family:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'SF Pro Text','Helvetica Neue',Arial,sans-serif !important;background:transparent;border:1px solid #2a2e2a;color:#e8f4ec;padding:0.75rem 1.15rem;font-weight:600;cursor:pointer;">Skip intro</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
    return modal;
  }

  function focusableIn(root) {
    return Array.from(
      root.querySelectorAll(
        'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'
      )
    ).filter((el) => !el.hasAttribute("disabled") && el.offsetParent !== null);
  }

  function bootWelcomeModal() {
    let seen = false;
    try {
      seen = localStorage.getItem(WELCOME_KEY) === "1";
    } catch (_) {
      seen = false;
    }
    if (seen) return;

    const modal = ensureWelcomeModal();
    const card = modal.querySelector(".welcome-modal__card");
    const continueBtn = modal.querySelector("#welcome-modal-continue");
    let lastFocus = null;

    function markSeen() {
      try {
        localStorage.setItem(WELCOME_KEY, "1");
      } catch (_) {
        /* private mode / blocked storage — still dismiss for this session */
      }
    }

    function closeModal() {
      markSeen();
      modal.hidden = true;
      document.body.classList.remove("welcome-modal-open");
      document.removeEventListener("keydown", onKeydown, true);
      if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
    }

    function onKeydown(e) {
      if (modal.hidden) return;
      if (e.key === "Escape") {
        e.preventDefault();
        closeModal();
        return;
      }
      if (e.key !== "Tab" || !card) return;
      const nodes = focusableIn(card);
      if (!nodes.length) return;
      const first = nodes[0];
      const last = nodes[nodes.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }

    modal.querySelectorAll("[data-welcome-dismiss]").forEach((el) => {
      el.addEventListener("click", (e) => {
        e.preventDefault();
        closeModal();
      });
    });

    modal.querySelectorAll("[data-welcome-route]").forEach((el) => {
      el.addEventListener("click", () => markSeen());
    });

    lastFocus = document.activeElement;
    modal.hidden = false;
    document.body.classList.add("welcome-modal-open");
    document.addEventListener("keydown", onKeydown, true);
    if (continueBtn) continueBtn.focus();
  }

  function boot() {
    enhanceBrand();
    renderNav();
    enhanceFooter();
    bootWelcomeModal();
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
