// ===== Settings =====
const TOTAL_PCS = 30;              // number of computers in the laboratory
const ADMIN_PASSWORD = "admin123"; // demo only: change it, and see the note in the README below
const STORAGE_KEY = "labSessions";

// ===== Data (saved in the browser with localStorage) =====
function loadSessions() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; }
  catch (e) { return []; }
}
function saveSessions(list) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(list)); } catch (e) {}
}
let sessions = loadSessions();
let selectedPc = null;
let isAdmin = false;

// ===== Helpers =====
const $ = (id) => document.getElementById(id);
const pcName = (n) => "PC-" + String(n).padStart(2, "0");
const activeSessions = () => sessions.filter((s) => !s.timeOut);
const dateStr = (iso) => new Date(iso).toLocaleDateString("en-CA"); // YYYY-MM-DD
const timeStr = (iso) => new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

function duration(s) {
  const end = s.timeOut ? new Date(s.timeOut) : new Date();
  const mins = Math.max(0, Math.round((end - new Date(s.timeIn)) / 60000));
  const h = Math.floor(mins / 60), m = mins % 60;
  return h ? h + " h " + m + " min" : m + " min";
}
function say(el, text, ok) {
  el.textContent = text;
  el.className = "msg " + (ok ? "ok" : "err");
}
function clean(text) { return text.trim().replace(/\s+/g, " "); }

// ===== Laboratory map =====
function renderMap() {
  const map = $("map");
  map.innerHTML = "";
  for (let n = 1; n <= TOTAL_PCS; n++) {
    const name = pcName(n);
    const user = activeSessions().find((s) => s.pc === name);
    const b = document.createElement("button");
    b.type = "button";
    b.className = "pc" + (user ? " used" : "") + (selectedPc === name ? " pick" : "");
    b.innerHTML = "<b>" + name + "</b><small>" + (user ? user.name.split(",")[0] : "Free") + "</small>";
    if (user) {
      b.disabled = true;
      b.title = "In use";
    } else {
      b.onclick = () => {
        selectedPc = name;
        $("spc").value = name;
        renderMap();
      };
    }
    map.appendChild(b);
  }
}

// ===== Student: time in =====
$("timeInForm").addEventListener("submit", (e) => {
  e.preventDefault();
  const id = clean($("sid").value);
  const name = clean($("sname").value);
  const section = clean($("ssection").value);
  const pc = $("spc").value;
  const msg = $("inMsg");

  if (!pc) return say(msg, "Select a free computer on the map first.", false);
  if (activeSessions().some((s) => s.studentId.toLowerCase() === id.toLowerCase()))
    return say(msg, "This student ID already has an active session. Time out first.", false);
  if (activeSessions().some((s) => s.pc === pc)) {
    selectedPc = null; $("spc").value = ""; renderMap();
    return say(msg, pc + " was just taken. Choose another computer.", false);
  }

  sessions.push({
    id: Date.now(),
    studentId: id, name: name, section: section, pc: pc,
    timeIn: new Date().toISOString(), timeOut: null
  });
  saveSessions(sessions);
  say(msg, "Session started on " + pc + " at " + timeStr(new Date().toISOString()) + ".", true);
  e.target.reset();
  selectedPc = null;
  refresh();
});

// ===== Student: time out =====
$("timeOutForm").addEventListener("submit", (e) => {
  e.preventDefault();
  const id = clean($("outId").value).toLowerCase();
  const s = activeSessions().find((x) => x.studentId.toLowerCase() === id);
  if (!s) return say($("outMsg"), "No active session found for that student ID.", false);
  s.timeOut = new Date().toISOString();
  saveSessions(sessions);
  say($("outMsg"), s.pc + " is free again. Time used: " + duration(s) + ".", true);
  e.target.reset();
  refresh();
});

// ===== Admin: sign in / out =====
$("loginForm").addEventListener("submit", (e) => {
  e.preventDefault();
  if ($("adminPass").value === ADMIN_PASSWORD) {
    isAdmin = true;
    $("adminPass").value = "";
    $("loginMsg").textContent = "";
    showAdmin();
  } else {
    say($("loginMsg"), "Wrong password. Try again.", false);
  }
});
$("logoutBtn").onclick = () => { isAdmin = false; showAdmin(); };

function showAdmin() {
  $("loginForm").hidden = isAdmin;
  $("dashboard").hidden = !isAdmin;
  if (isAdmin) renderAdmin();
}

// ===== Admin: dashboard =====
function renderAdmin() {
  const today = dateStr(new Date().toISOString());
  const active = activeSessions().length;
  $("statActive").textContent = active;
  $("statFree").textContent = TOTAL_PCS - active;
  $("statToday").textContent = sessions.filter((s) => dateStr(s.timeIn) === today).length;

  const q = $("search").value.toLowerCase();
  const d = $("dateFilter").value;
  const rows = sessions
    .filter((s) => !d || dateStr(s.timeIn) === d)
    .filter((s) => (s.name + s.studentId + s.section + s.pc).toLowerCase().includes(q))
    .sort((a, b) => new Date(b.timeIn) - new Date(a.timeIn));

  const body = $("logBody");
  body.innerHTML = "";
  rows.forEach((s) => {
    const tr = document.createElement("tr");
    const cells = [s.pc, s.studentId, s.name, s.section, dateStr(s.timeIn), timeStr(s.timeIn)];
    cells.forEach((c) => { const td = document.createElement("td"); td.textContent = c; tr.appendChild(td); });

    const out = document.createElement("td");
    if (s.timeOut) out.textContent = timeStr(s.timeOut);
    else out.innerHTML = '<span class="badge">In use</span>';
    tr.appendChild(out);

    const dur = document.createElement("td");
    dur.textContent = duration(s);
    tr.appendChild(dur);

    const act = document.createElement("td");
    if (!s.timeOut) {
      const b = document.createElement("button");
      b.className = "link";
      b.textContent = "End session";
      b.onclick = () => { s.timeOut = new Date().toISOString(); saveSessions(sessions); refresh(); };
      act.appendChild(b);
    }
    tr.appendChild(act);
    body.appendChild(tr);
  });
  $("emptyMsg").hidden = rows.length > 0;
}
$("search").addEventListener("input", renderAdmin);
$("dateFilter").addEventListener("change", renderAdmin);

// ===== Admin: export and clear =====
$("exportBtn").onclick = () => {
  const head = ["Computer", "Student ID", "Name", "Section", "Date", "Time in", "Time out", "Duration"];
  const lines = [head].concat(sessions.map((s) => [
    s.pc, s.studentId, s.name, s.section, dateStr(s.timeIn), timeStr(s.timeIn),
    s.timeOut ? timeStr(s.timeOut) : "In use", duration(s)
  ]));
  const csv = lines.map((r) => r.map((c) => '"' + String(c).replace(/"/g, '""') + '"').join(",")).join("\n");
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
  a.download = "lab-usage-" + dateStr(new Date().toISOString()) + ".csv";
  a.click();
  URL.revokeObjectURL(a.href);
};
$("clearBtn").onclick = () => {
  if (confirm("Delete all usage records? This cannot be undone.")) {
    sessions = [];
    saveSessions(sessions);
    selectedPc = null;
    refresh();
  }
};

// ===== Tabs =====
document.querySelectorAll(".tab").forEach((t) => {
  t.onclick = () => {
    document.querySelectorAll(".tab").forEach((x) => x.classList.toggle("active", x === t));
    $("student").hidden = t.dataset.tab !== "student";
    $("admin").hidden = t.dataset.tab !== "admin";
    refresh();
  };
});

function refresh() {
  renderMap();
  if (isAdmin) renderAdmin();
}

// Keep several open tabs in sync, and refresh durations every minute
window.addEventListener("storage", () => { sessions = loadSessions(); refresh(); });
setInterval(() => { if (isAdmin) renderAdmin(); }, 60000);

showAdmin();
refresh();
