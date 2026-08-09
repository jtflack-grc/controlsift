async function loadResults() {
  try {
    const res = await fetch("data/results.json", { cache: "no-store" });
    if (!res.ok) throw new Error("missing results");
    return await res.json();
  } catch (err) {
    console.warn("results.json unavailable", err);
    return null;
  }
}

function fmt(value) {
  if (value === null || value === undefined) return "pending";
  if (typeof value === "number") return value.toFixed(3);
  return String(value);
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

document.addEventListener("DOMContentLoaded", async () => {
  const data = await loadResults();
  fillMetrics(data);
  fillResultsTable(data);
  fillMacroBars(data);
  const status = document.querySelector("[data-results-status]");
  if (status) status.textContent = data ? data.status : "pending";
});
