async function loadCases() {
  const res = await fetch("data/failure_lab.json", { cache: "no-store" });
  if (!res.ok) throw new Error("failure_lab.json missing");
  return res.json();
}

function renderCase(caseData) {
  const root = document.querySelector("#case-view");
  if (!root || !caseData) return;
  const tags = (caseData.failure_tags || []).join(", ") || "none";
  root.innerHTML = `
    <article class="panel" style="border:0;border-radius:0;min-height:100%;">
      <div class="meta-strip" style="margin-top:0;">
        <span>Case <strong>${caseData.id}</strong></span>
        <span>Expected <strong>${caseData.label}</strong></span>
        <span>Tags <strong>${tags}</strong></span>
      </div>
      <h2>Control</h2>
      <div class="control-block" style="margin-top:0.5rem;">
        <span class="label">Requirement</span>
        ${caseData.control_statement}
      </div>
      <h2>Evidence</h2>
      <p><em>${caseData.evidence_type}</em> · ${caseData.environment}</p>
      <p style="color:var(--fg)">${caseData.evidence_text}</p>
      <h2>Why this is hard</h2>
      <p>${caseData.why_hard || "Boundary case selected for Failure Lab."}</p>
      <h2>Model outcomes</h2>
      <table>
        <thead><tr><th>Model</th><th>Prediction</th><th>Notes</th></tr></thead>
        <tbody>
          ${(caseData.predictions || []).map((p) => `
            <tr>
              <td>${p.model}</td>
              <td class="${p.pred_label == null ? "pending" : ""}">${p.pred_label ?? "pending"}</td>
              <td>${p.note || ""}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    </article>
  `;
}

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const payload = await loadCases();
    const list = document.querySelector("#case-list");
    const cases = payload.cases || [];
    cases.forEach((c, idx) => {
      const li = document.createElement("li");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = `${c.id} · ${c.label}`;
      btn.addEventListener("click", () => {
        list.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        renderCase(c);
      });
      li.appendChild(btn);
      list.appendChild(li);
      if (idx === 0) {
        btn.classList.add("active");
        renderCase(c);
      }
    });
  } catch (err) {
    document.querySelector("#case-view").innerHTML =
      `<div class="panel pending">Failure Lab cases will appear after error analysis (Gate 4).</div>`;
  }
});
