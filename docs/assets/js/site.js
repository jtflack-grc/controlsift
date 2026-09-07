async function loadResults() {
  const url = resolveResultsUrl();
  try {
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("missing results");
    return await res.json();
  } catch (err) {
    console.warn("results.json unavailable", err);
    return null;
  }
}

function resolveResultsUrl() {
  if (document.body && document.body.dataset.resultsUrl) {
    return document.body.dataset.resultsUrl;
  }
  const meta = document.querySelector('meta[name="results-url"]');
  if (meta && meta.content) return meta.content;
  const script = document.querySelector('script[src*="assets/js/site.js"]');
  if (script) {
    const src = script.getAttribute("src") || "";
    const base = src.replace(/assets\/js\/site\.js(\?.*)?$/, "");
    return `${base}data/results.json`;
  }
  return "data/results.json";
}

function fmt(value) {
  if (value === null || value === undefined) return "pending";
  if (typeof value === "number") return value.toFixed(3);
  return String(value);
}

function gemmaTestReady(data) {
  if (!data || !data.experiments) return false;
  return ["gemma_zero_shot", "gemma_few_shot", "gemma_qlora"].every(
    (key) => data.experiments[key] && data.experiments[key].macro_f1 != null
  );
}

function fillMetrics(data) {
  const nodes = document.querySelectorAll("[data-metric]");
  if (!nodes.length) return;
  nodes.forEach((el) => {
    const key = el.getAttribute("data-metric");
    const exp = el.getAttribute("data-experiment");
    let value = null;
    if (data && exp && data.experiments && data.experiments[exp]) {
      value = data.experiments[exp][key];
    } else if (data && key in data) {
      value = data[key];
    }
    el.textContent = fmt(value);
    el.classList.toggle("pending", value === null || value === undefined);
  });
}

function fillPendingUntilGemma(data) {
  const ready = gemmaTestReady(data);
  document.querySelectorAll("[data-pending-until-gemma]").forEach((el) => {
    el.hidden = ready;
    el.classList.toggle("pending", !ready);
  });
  document.querySelectorAll("[data-ready-when-gemma]").forEach((el) => {
    el.hidden = !ready;
  });
}

function fillResultsTable(data) {
  const body = document.querySelector("#results-body");
  if (!body || !data || !data.experiments) return;
  body.innerHTML = "";
  Object.values(data.experiments).forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.experiment}</td>
      <td>${row.model || "—"}</td>
      <td class="${row.macro_f1 == null ? "pending" : ""}">${fmt(row.macro_f1)}</td>
      <td class="${row.accuracy == null ? "pending" : ""}">${fmt(row.accuracy)}</td>
      <td class="${row.challenge_macro_f1 == null ? "pending" : ""}">${fmt(row.challenge_macro_f1)}</td>
    `;
    body.appendChild(tr);
  });
}

function fillMacroBars(data) {
  const root = document.querySelector("#macro-bars");
  if (!root || !data || !data.experiments) return;
  const order = [
    "majority",
    "tfidf",
    "gemma_zero_shot",
    "gemma_few_shot",
    "gemma_qlora",
  ];
  root.innerHTML = "";
  order.forEach((key) => {
    const row = data.experiments[key];
    if (!row) return;
    const value = row.macro_f1;
    const pending = value === null || value === undefined;
    const scale = pending ? 0 : Math.max(0, Math.min(1, value));
    const el = document.createElement("div");
    el.className = "bar-row";
    el.innerHTML = `
      <span class="name">${row.experiment}</span>
      <div class="bar-track"><div class="bar-fill${pending ? " is-pending" : ""}" style="transform:scaleX(${pending ? 1 : scale})"></div></div>
      <span class="val ${pending ? "pending" : ""}">${fmt(value)}</span>
    `;
    root.appendChild(el);
  });
}

function fillHubGemmaStatus(data) {
  const ready = gemmaTestReady(data);
  document.querySelectorAll("[data-hub-gemma-status]").forEach((el) => {
    const pendingLabel = el.getAttribute("data-pending-label") || "pending GPU";
    const readyLabel = el.getAttribute("data-ready-label") || "meets";
    el.textContent = ready ? readyLabel : pendingLabel;
    el.classList.toggle("pending-gpu", !ready);
  });
}

document.addEventListener("DOMContentLoaded", async () => {
  const data = await loadResults();
  fillMetrics(data);
  fillPendingUntilGemma(data);
  fillHubGemmaStatus(data);
  fillResultsTable(data);
  fillMacroBars(data);
  const status = document.querySelector("[data-results-status]");
  if (status) status.textContent = data ? data.status : "pending";
});
