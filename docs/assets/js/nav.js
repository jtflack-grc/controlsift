/** Shared primary nav for ControlSift static pages (header only). */
(function () {
  const WELCOME_KEY = "controlsift_welcome_seen";

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
      <div class="welcome-modal__card" role="document" style="font-family:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'SF Pro Text','Helvetica Neue',Arial,sans-serif !important;background:#0a1510;border:2px solid #7fffb2;padding:1.5rem 1.45rem;color:#e8f4ec;">
        <p class="welcome-modal__brand" style="font-family:'IBM Plex Mono',monospace !important;color:#7fffb2;margin:0 0 0.55rem;font-size:clamp(1.85rem,5vw,2.35rem);font-weight:600;">ControlSift</p>
        <h2 id="welcome-modal-title" style="font-family:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'SF Pro Text','Helvetica Neue',Arial,sans-serif !important;color:#fff;margin:0 0 0.75rem;font-size:clamp(1.2rem,3vw,1.45rem);font-weight:500;">Proof from paperwork — research, not a live auditor.</h2>
        <p style="font-family:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'SF Pro Text','Helvetica Neue',Arial,sans-serif !important;color:#c8e6d2;line-height:1.55;margin:0 0 0.85rem;">
          ControlSift studies whether a small AI can tell real security proof from paperwork
          on a sealed synthetic benchmark. Open research with published metrics — not production GRC software.
        </p>
        <p class="welcome-modal__note" style="font-family:'IBM Plex Mono',monospace !important;color:#38e881;font-size:0.72rem;letter-spacing:0.04em;text-transform:uppercase;margin:0 0 1rem;">UN SDG 10 · Reduced Inequalities · metrics published</p>
        <div class="cta-row" style="display:flex;flex-wrap:wrap;gap:0.65rem;">
          <button type="button" class="btn btn-primary" id="welcome-modal-continue" data-welcome-dismiss style="font-family:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'SF Pro Text','Helvetica Neue',Arial,sans-serif !important;background:#7fffb2;color:#021008;border:1px solid #7fffb2;padding:0.75rem 1.15rem;font-weight:600;cursor:pointer;">Continue to site</button>
          <a class="btn btn-secondary" href="${p}capstone/index.html" data-welcome-capstone style="font-family:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'SF Pro Text','Helvetica Neue',Arial,sans-serif !important;border:1px solid #2a2e2a;color:#e8f4ec;padding:0.75rem 1.15rem;font-weight:600;text-decoration:none;">Enter Capstone</a>
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
      if (lastFocus && typeof lastFocus.focus === "function") {
        lastFocus.focus();
      }
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

    const capstone = modal.querySelector("[data-welcome-capstone]");
    if (capstone) {
      capstone.addEventListener("click", () => {
        markSeen();
      });
    }

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
