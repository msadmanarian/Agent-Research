/**
 * CogniMesh Visual Research Laboratory Client
 * Interactive canvas visualizations, REST API connectors, and real-time telemetry.
 */

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initCognitiveControls();
  initKnowledgeGraph();
  initDebateArena();
  initBenchmarks();
  initBibtexCopy();

  // Load initial system status
  fetchStatus();
});

// ==========================================
// 1. Tab Navigation
// ==========================================
function initTabs() {
  const tabs = document.querySelectorAll(".nav-tab");
  const panels = document.querySelectorAll(".panel");

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("active"));
      panels.forEach((p) => p.classList.remove("active"));

      tab.classList.add("active");
      const targetId = tab.getAttribute("data-target");
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) {
        targetPanel.classList.add("active");
      }

      if (targetId === "panel-graph") {
        renderGraph();
      }
    });
  });
}

// ==========================================
// 2. Cognitive Cycle Runner & Telemetry
// ==========================================
function initCognitiveControls() {
  const btnRun = document.getElementById("btn-run-step");
  if (!btnRun) return;

  btnRun.addEventListener("click", async () => {
    const perception = document.getElementById("input-perception").value.trim();
    const goal = document.getElementById("input-goal").value.trim();
    const feedback = document.getElementById("input-feedback").value;

    btnRun.disabled = true;
    btnRun.innerHTML = `<span class="btn-icon">⏳</span> Deliberating...`;

    try {
      const res = await fetch("/api/run-cycle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ perception, goal, feedback }),
      });
      const data = await res.json();
      renderCycleResults(data);
    } catch (err) {
      console.error("Cycle execution error:", err);
    } finally {
      btnRun.disabled = false;
      btnRun.innerHTML = `<span class="btn-icon">⚡</span> Execute Cycle`;
    }
  });
}

function renderCycleResults(data) {
  // 1. Working Memory
  const wmList = document.getElementById("working-memory-list");
  const wmBadge = document.getElementById("wm-count-badge");
  wmList.innerHTML = "";

  const items = data.working_memory || [];
  wmBadge.textContent = `${items.length} / 7`;

  if (items.length === 0) {
    wmList.innerHTML = `<li class="empty-state">No items in working buffer.</li>`;
  } else {
    items.forEach((it) => {
      const li = document.createElement("li");
      li.className = "memory-item";
      li.innerHTML = `
        <span>${escapeHtml(it.content)}</span>
        <span class="salience-tag">s:${it.salience.toFixed(2)}</span>
      `;
      wmList.appendChild(li);
    });
  }

  // 2. Arbitration & Mode
  const modeBadge = document.getElementById("mode-badge");
  modeBadge.textContent = data.selected_mode.replace("_", " ").toUpperCase();
  modeBadge.className = data.selected_mode.includes("system_2") ? "badge badge-accent" : "badge badge-mode";

  const conf = data.confidence || {};
  document.getElementById("metric-s1").textContent = `${((conf.heuristic_score || 0) * 100).toFixed(0)}%`;
  document.getElementById("bar-s1").style.width = `${(conf.heuristic_score || 0) * 100}%`;

  document.getElementById("metric-uncertainty").textContent = `${((conf.epistemic_uncertainty || 0) * 100).toFixed(0)}%`;
  document.getElementById("bar-uncertainty").style.width = `${(conf.epistemic_uncertainty || 0) * 100}%`;

  document.getElementById("arbitration-reason").textContent = conf.reason || "Arbitration completed.";

  // 3. Reflection
  const reflBox = document.getElementById("reflection-box");
  const reflStatus = document.getElementById("reflection-status");
  const refl = data.reflection || {};

  if (refl.successful) {
    reflStatus.textContent = "Aligned";
    reflStatus.className = "badge";
    reflStatus.style.background = "rgba(16, 185, 129, 0.15)";
    reflStatus.style.color = "#10b981";
  } else {
    reflStatus.textContent = "Drift Detected";
    reflStatus.className = "badge";
    reflStatus.style.background = "rgba(244, 63, 94, 0.15)";
    reflStatus.style.color = "#f43f5e";
  }

  let reflHtml = `<p class="reflection-critique">${escapeHtml(refl.critique || "Nominal")}</p>`;
  if (refl.heuristic_rule_learned) {
    reflHtml += `<div class="reflection-rule"><strong>Consolidated Rule:</strong> ${escapeHtml(refl.heuristic_rule_learned)}</div>`;
  }
  reflBox.innerHTML = reflHtml;

  // 4. Action Trace
  const traceBox = document.getElementById("action-trace-content");
  document.getElementById("cycle-latency").textContent = `Latency: ${data.duration_ms}ms`;

  const act = data.action || {};
  traceBox.textContent = `[Cycle ${data.cycle_index}] Action Type: ${act.action_type}\nRationale: ${act.rationale}\nPayload: ${JSON.stringify(act.payload, null, 2)}`;
}

async function fetchStatus() {
  try {
    const res = await fetch("/api/status");
    const data = await res.json();
    if (data.status === "online") {
      document.getElementById("system-status-indicator").querySelector(".status-label").textContent =
        `Sim Engine: Online (Cycle ${data.engine_state.cycle_index})`;
    }
  } catch (err) {
    console.warn("Status fetch warning:", err);
  }
}

// ==========================================
// 3. Knowledge Graph Canvas Renderer
// ==========================================
let graphNodes = [];
let graphEdges = [];
let graphAnimationId = null;

function initKnowledgeGraph() {
  const canvas = document.getElementById("knowledgeGraphCanvas");
  if (!canvas) return;

  document.getElementById("btn-refresh-graph")?.addEventListener("click", loadGraphData);
  document.getElementById("btn-activate-nodes")?.addEventListener("click", () => {
    graphNodes.forEach((n) => {
      n.activation = Math.min(1.0, n.activation + Math.random() * 0.4);
    });
  });

  loadGraphData();
}

async function loadGraphData() {
  try {
    const res = await fetch("/api/graph");
    const data = await res.json();

    const canvas = document.getElementById("knowledgeGraphCanvas");
    const width = canvas.width;
    const height = canvas.height;

    // Position nodes radially / force-like
    const rawNodes = data.nodes || [];
    const count = rawNodes.length;
    graphNodes = rawNodes.map((n, i) => {
      const angle = (i / count) * 2 * Math.PI;
      const radius = 170 + (i % 2) * 50;
      return {
        ...n,
        x: width / 2 + Math.cos(angle) * radius,
        y: height / 2 + Math.sin(angle) * radius,
        vx: 0,
        vy: 0,
      };
    });

    graphEdges = data.edges || [];
    renderGraph();
  } catch (err) {
    console.error("Failed to load graph:", err);
  }
}

function renderGraph() {
  const canvas = document.getElementById("knowledgeGraphCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw edges
    graphEdges.forEach((edge) => {
      const src = graphNodes.find((n) => n.id === edge.source);
      const tgt = graphNodes.find((n) => n.id === edge.target);
      if (src && tgt) {
        ctx.beginPath();
        ctx.moveTo(src.x, src.y);
        ctx.lineTo(tgt.x, tgt.y);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.12)";
        ctx.lineWidth = Math.max(1, edge.weight * 2);
        ctx.stroke();

        // Draw relation label
        const midX = (src.x + tgt.x) / 2;
        const midY = (src.y + tgt.y) / 2;
        ctx.fillStyle = "rgba(148, 163, 184, 0.6)";
        ctx.font = "9px JetBrains Mono";
        ctx.fillText(edge.relation.replace("_", " "), midX - 20, midY - 4);
      }
    });

    // Draw nodes
    graphNodes.forEach((node) => {
      // Glow circle
      ctx.beginPath();
      const nodeRadius = 16 + (node.activation || 0) * 10;
      ctx.arc(node.x, node.y, nodeRadius, 0, 2 * Math.PI);

      let color = "#00f2fe";
      if (node.category.includes("memory")) color = "#10b981";
      if (node.category.includes("reasoning")) color = "#8a2be2";
      if (node.category.includes("multiagent")) color = "#f59e0b";

      ctx.fillStyle = color;
      ctx.shadowColor = color;
      ctx.shadowBlur = 12 + (node.activation || 0) * 15;
      ctx.fill();
      ctx.shadowBlur = 0;

      // Inner ring
      ctx.beginPath();
      ctx.arc(node.x, node.y, nodeRadius - 3, 0, 2 * Math.PI);
      ctx.fillStyle = "#07090e";
      ctx.fill();

      // Node Name Label
      ctx.fillStyle = "#ffffff";
      ctx.font = "11px Inter, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(node.name, node.x, node.y + nodeRadius + 14);

      // Activation decay
      if (node.activation > 0.05) {
        node.activation *= 0.995;
      }
    });

    graphAnimationId = requestAnimationFrame(animate);
  }

  if (graphAnimationId) cancelAnimationFrame(graphAnimationId);
  animate();
}

// ==========================================
// 4. Dialectical Multi-Agent Arena
// ==========================================
function initDebateArena() {
  const btnStart = document.getElementById("btn-start-debate");
  if (!btnStart) return;

  btnStart.addEventListener("click", async () => {
    const topic = document.getElementById("input-debate-topic").value.trim();
    const rounds = document.getElementById("input-debate-rounds").value;

    btnStart.disabled = true;
    btnStart.innerHTML = `<span class="btn-icon">⏳</span> Convening...`;

    try {
      const res = await fetch("/api/run-debate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, rounds }),
      });
      const data = await res.json();
      renderDebateResults(data);
    } catch (err) {
      console.error("Debate error:", err);
    } finally {
      btnStart.disabled = false;
      btnStart.innerHTML = `<span class="btn-icon">⚔️</span> Convene Arena`;
    }
  });
}

function renderDebateResults(data) {
  const container = document.getElementById("debate-messages-container");
  container.innerHTML = "";

  const messages = data.messages || [];
  document.getElementById("debate-turn-badge").textContent = `${messages.length} Statements`;

  messages.forEach((msg) => {
    const div = document.createElement("div");
    div.className = "debate-msg";

    let roleClass = "speaker-proposer";
    if (msg.role.includes("Adversary")) roleClass = "speaker-adversary";
    if (msg.role.includes("FactChecker")) roleClass = "speaker-factchecker";
    if (msg.role.includes("Synthesizer")) roleClass = "speaker-synthesizer";

    div.innerHTML = `
      <div class="debate-msg-header">
        <span class="${roleClass}">[Round ${msg.round}] ${escapeHtml(msg.speaker)} &bull; ${escapeHtml(msg.role)}</span>
        <span class="badge">Stance: ${msg.stance > 0 ? "+" : ""}${msg.stance.toFixed(2)}</span>
      </div>
      <div class="debate-msg-content">${escapeHtml(msg.content)}</div>
    `;
    container.appendChild(div);
  });

  // Metrics
  document.getElementById("metric-sycophancy").textContent = `${((data.sycophancy_resistance_score || 0) * 100).toFixed(1)}%`;
  document.getElementById("synthesis-box").textContent = data.synthesis || "Synthesis complete.";
}

// ==========================================
// 5. Diagnostic Benchmarks & Radar Chart
// ==========================================
function initBenchmarks() {
  const btnRun = document.getElementById("btn-run-benchmarks");
  if (!btnRun) return;

  btnRun.addEventListener("click", async () => {
    btnRun.disabled = true;
    btnRun.innerHTML = `<span class="btn-icon">⏳</span> Benchmarking...`;

    try {
      const res = await fetch("/api/run-benchmark", { method: "POST" });
      const data = await res.json();
      renderBenchmarkResults(data);
    } catch (err) {
      console.error("Benchmark error:", err);
    } finally {
      btnRun.disabled = false;
      btnRun.innerHTML = `<span class="btn-icon">🚀</span> Run All Benchmarks`;
    }
  });
}

function renderBenchmarkResults(data) {
  // Badges
  document.getElementById("composite-score-badge").textContent = `Index: ${data.composite_index}%`;
  document.getElementById("tasks-passed-badge").textContent = `Passed: ${data.tasks_passed}`;

  // Table
  const tbody = document.getElementById("benchmark-table-body");
  tbody.innerHTML = "";

  const tasks = data.tasks || [];
  tasks.forEach((t) => {
    const tr = document.createElement("tr");
    const statusClass = t.passed ? "status-pass" : "status-fail";
    const statusText = t.passed ? "PASS" : "FAIL";

    tr.innerHTML = `
      <td><strong>${escapeHtml(t.task_name)}</strong><br><small style="color:var(--text-muted)">${escapeHtml(t.details)}</small></td>
      <td>${escapeHtml(t.category)}</td>
      <td><strong>${(t.score * 100).toFixed(1)}%</strong></td>
      <td class="${statusClass}">[${statusText}]</td>
    `;
    tbody.appendChild(tr);
  });

  // Radar Chart Canvas
  drawRadarChart(data.radar_metrics || []);
}

function drawRadarChart(metrics) {
  const canvas = document.getElementById("radarChartCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;
  const cx = w / 2;
  const cy = h / 2;
  const radius = 120;

  ctx.clearRect(0, 0, w, h);

  const numAxes = metrics.length || 5;
  const angleStep = (2 * Math.PI) / numAxes;

  // Concentric polygon grids (20%, 40%, 60%, 80%, 100%)
  const levels = [0.2, 0.4, 0.6, 0.8, 1.0];
  ctx.strokeStyle = "rgba(255, 255, 255, 0.1)";
  ctx.lineWidth = 1;

  levels.forEach((lvl) => {
    ctx.beginPath();
    for (let i = 0; i < numAxes; i++) {
      const angle = i * angleStep - Math.PI / 2;
      const x = cx + Math.cos(angle) * (radius * lvl);
      const y = cy + Math.sin(angle) * (radius * lvl);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.stroke();
  });

  // Axis spokes & labels
  ctx.fillStyle = "rgba(148, 163, 184, 0.8)";
  ctx.font = "11px Inter, sans-serif";
  ctx.textAlign = "center";

  for (let i = 0; i < numAxes; i++) {
    const angle = i * angleStep - Math.PI / 2;
    const x = cx + Math.cos(angle) * radius;
    const y = cy + Math.sin(angle) * radius;

    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(x, y);
    ctx.stroke();

    const labelX = cx + Math.cos(angle) * (radius + 24);
    const labelY = cy + Math.sin(angle) * (radius + 18);
    const dimName = metrics[i] ? metrics[i].dimension : `Dim ${i + 1}`;
    ctx.fillText(dimName, labelX, labelY);
  }

  // Data polygon
  ctx.beginPath();
  ctx.fillStyle = "rgba(0, 242, 254, 0.25)";
  ctx.strokeStyle = "#00f2fe";
  ctx.lineWidth = 2.5;

  for (let i = 0; i < numAxes; i++) {
    const scoreFrac = metrics[i] ? metrics[i].score / 100 : 0.5;
    const angle = i * angleStep - Math.PI / 2;
    const x = cx + Math.cos(angle) * (radius * scoreFrac);
    const y = cy + Math.sin(angle) * (radius * scoreFrac);

    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // Data point dots
  for (let i = 0; i < numAxes; i++) {
    const scoreFrac = metrics[i] ? metrics[i].score / 100 : 0.5;
    const angle = i * angleStep - Math.PI / 2;
    const x = cx + Math.cos(angle) * (radius * scoreFrac);
    const y = cy + Math.sin(angle) * (radius * scoreFrac);

    ctx.beginPath();
    ctx.arc(x, y, 4, 0, 2 * Math.PI);
    ctx.fillStyle = "#ffffff";
    ctx.shadowColor = "#00f2fe";
    ctx.shadowBlur = 8;
    ctx.fill();
    ctx.shadowBlur = 0;
  }
}

// ==========================================
// 6. BibTeX Copy
// ==========================================
function initBibtexCopy() {
  const btn = document.getElementById("btn-copy-bibtex");
  if (!btn) return;

  btn.addEventListener("click", () => {
    const bibtex = document.getElementById("bibtex-block").textContent;
    navigator.clipboard.writeText(bibtex).then(() => {
      btn.textContent = "✅ Copied!";
      setTimeout(() => {
        btn.textContent = "📋 Copy BibTeX";
      }, 2000);
    });
  });
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
