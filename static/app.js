var tasks = [];
var activeFilter = "todas";
var overdueOnly = false;
var searchText = "";
var editingId = null;

var PRIORITY_ORDER = { "altisima": 0, "alta": 1, "media": 2, "baja": 3 };
var CAT_LABELS = { "personal": "Personal", "domestico": "Doméstico", "laboral": "Laboral", "otro": "Otro" };
var PRI_LABELS = { "altisima": "altísima", "alta": "alta", "media": "media", "baja": "baja" };
var STATUS_LABELS = { "pendiente": "Pendiente", "critico": "Crítico", "hoy": "Hoy", "progreso": "En progreso", "hecho": "Completado" };

function todayStr() {
  var d = new Date();
  var mm = String(d.getMonth() + 1).padStart(2, "0");
  var dd = String(d.getDate()).padStart(2, "0");
  return d.getFullYear() + "-" + mm + "-" + dd;
}

function api(path, options) {
  options = options || {};
  options.headers = Object.assign({ "Content-Type": "application/json" }, options.headers || {});
  return fetch("/api" + path, options).then(function(res) {
    if (!res.ok) {
      return res.text().then(function(txt) {
        throw new Error("API " + res.status + ": " + txt);
      });
    }
    if (res.status === 204) return null;
    return res.json();
  });
}

function loadTasks() {
  return api("/tasks").then(function(data) {
    tasks = data;
    render();
  }).catch(function(err) {
    console.error(err);
    alert("Error al cargar tareas: " + err.message);
  });
}

function isOverdue(t) {
  return !!t.due && t.due < todayStr() && t.status !== "hecho";
}

function matchesFilters(t) {
  if (activeFilter !== "todas" && t.category !== activeFilter) return false;
  if (overdueOnly && !isOverdue(t)) return false;
  if (searchText) {
    var hay = ((t.title || "") + " " + (t.notes || "")).toLowerCase();
    if (hay.indexOf(searchText) === -1) return false;
  }
  return true;
}

function compareTasks(a, b) {
  var pa = PRIORITY_ORDER[a.priority] != null ? PRIORITY_ORDER[a.priority] : 99;
  var pb = PRIORITY_ORDER[b.priority] != null ? PRIORITY_ORDER[b.priority] : 99;
  if (pa !== pb) return pa - pb;
  // created_at ascending (oldest first); empty values go last
  var ca = a.created_at || "9999-99-99";
  var cb = b.created_at || "9999-99-99";
  if (ca !== cb) return ca < cb ? -1 : 1;
  return (a.id || 0) - (b.id || 0);
}

function render() {
  var filtered = tasks.filter(matchesFilters);
  var colKeys = ["pendiente", "critico", "progreso", "hoy", "hecho"];
  colKeys.forEach(function(key) {
    var area = document.getElementById("col-" + key);
    var colTasks = filtered.filter(function(t){ return t.status === key; }).sort(compareTasks);
    document.getElementById("cnt-" + key).textContent = colTasks.length;
    if (colTasks.length === 0) {
      area.innerHTML = "<div class=\"empty-state\"><div class=\"icon\">&#x1F5C2;</div>Sin tareas aquí</div>";
      return;
    }
    area.innerHTML = colTasks.map(cardHTML).join("");
  });
  renderStats();
}

function cardHTML(t) {
  var overdue = isOverdue(t);
  var isDone = t.status === "hecho";
  var dueStr = t.due ? "<span class=\"card-due" + (overdue ? " overdue" : "") + "\">" + (overdue ? "&#9888; " : "&#128197; ") + fmtDate(t.due) + "</span>" : "";
  var createdStr = t.created_at ? "<span class=\"card-created\" title=\"Fecha de creación\">&#43; " + fmtDate(t.created_at) + "</span>" : "";

  // Advance button (next state in workflow).
  var nextSt  = { pendiente: "hoy", critico: "hoy", hoy: "progreso", progreso: "hecho", hecho: "pendiente" };
  var nextLbl = { pendiente: "&#9728; Hoy", critico: "&#9728; Hoy", hoy: "&#9654; Iniciar", progreso: "&#10003; Completar", hecho: "&#8617; Reabrir" };
  var advanceBtn = "<button class=\"action-btn\" onclick=\"moveTask(" + t.id + ",'" + nextSt[t.status] + "')\">" + nextLbl[t.status] + "</button>";

  // Extra "Completar" shortcut for critico and hoy (progreso already completes via advance).
  var completeBtn = "";
  if (t.status === "critico" || t.status === "hoy") {
    completeBtn = "<button class=\"action-btn complete\" title=\"Completar\" onclick=\"moveTask(" + t.id + ",'hecho')\">&#10003;</button>";
  }

  var notesHTML = t.notes ? "<p style=\"margin-top:3px;font-size:0.7rem;color:#aaa;line-height:1.3\">" + esc(t.notes) + "</p>" : "";

  return "<div class=\"card priority-" + t.priority + "\" id=\"card-" + t.id + "\">" +
    "<div class=\"card-top\">" +
      "<span class=\"card-id\">#" + t.id + "</span>" +
      "<span class=\"card-title" + (isDone ? " done" : "") + "\">" + esc(t.title) + "</span>" +
    "</div>" +
    "<div class=\"card-meta\">" +
      "<div class=\"card-tags\">" +
        "<span class=\"tag tag-" + t.category + "\">" + (CAT_LABELS[t.category]||t.category) + "</span>" +
        "<span style=\"display:flex;align-items:center;gap:2px\">" +
          "<span class=\"priority-dot p-" + t.priority + "\"></span>" +
          "<span style=\"font-size:0.63rem;color:#999\">" + (PRI_LABELS[t.priority]||t.priority) + "</span>" +
        "</span>" +
        dueStr +
        createdStr +
      "</div>" +
      "<div class=\"card-actions\">" +
        advanceBtn +
        completeBtn +
        "<button class=\"action-btn\" onclick=\"editTask(" + t.id + ")\">&#9999;</button>" +
        "<button class=\"action-btn danger\" onclick=\"deleteTask(" + t.id + ")\">&#128465;</button>" +
      "</div>" +
    "</div>" +
    notesHTML +
    "</div>";
}

function renderStats() {
  var total = tasks.length;
  var done = tasks.filter(function(t){ return t.status === "hecho"; }).length;
  var altisimas = tasks.filter(function(t){ return t.priority === "altisima" && t.status !== "hecho"; }).length;
  var pct = total ? Math.round(done / total * 100) : 0;
  var overdue = tasks.filter(isOverdue).length;
  var html = "<span class=\"stat-chip\"><b>" + total + "</b> tareas</span>" +
             "<span class=\"stat-chip\"><b>" + done + "</b> completadas</span>" +
             "<span class=\"stat-chip\"><b>" + pct + "%</b> progreso</span>";
  if (altisimas) html += "<span class=\"stat-chip\" style=\"background:rgba(123,13,30,0.35)\"><b>" + altisimas + "</b> altísima prio</span>";
  if (overdue)   html += "<span class=\"stat-chip\" style=\"background:rgba(233,69,96,0.3)\"><b>" + overdue + "</b> vencidas</span>";
  document.getElementById("stats").innerHTML = html;
}

function moveTask(id, newStatus) {
  api("/tasks/" + id, { method: "PATCH", body: JSON.stringify({ status: newStatus }) })
    .then(function(updated) {
      var idx = tasks.findIndex(function(t){ return t.id === id; });
      if (idx >= 0 && updated) tasks[idx] = updated;
      render();
    })
    .catch(function(err) { alert("Error al mover tarea: " + err.message); });
}

function deleteTask(id) {
  if (!confirm("¿Eliminar esta tarea?")) return;
  api("/tasks/" + id, { method: "DELETE" })
    .then(function() {
      tasks = tasks.filter(function(t){ return t.id !== id; });
      render();
    })
    .catch(function(err) { alert("Error al eliminar tarea: " + err.message); });
}

function clearCompleted(ev) {
  if (ev) ev.stopPropagation();
  var n = tasks.filter(function(t){ return t.status === "hecho"; }).length;
  if (n === 0) { alert("No hay tareas completadas para limpiar."); return; }
  if (!confirm("¿Eliminar las " + n + " tareas completadas? Esta acción no se puede deshacer.")) return;
  api("/tasks/completed", { method: "DELETE" })
    .then(function() {
      tasks = tasks.filter(function(t){ return t.status !== "hecho"; });
      render();
    })
    .catch(function(err) { alert("Error al limpiar finalizadas: " + err.message); });
}

function editTask(id) {
  var t = tasks.find(function(t){ return t.id === id; });
  if (!t) return;
  editingId = id;
  document.getElementById("modalTitle").textContent = "Editar tarea";
  document.getElementById("fTitle").value = t.title;
  document.getElementById("fNotes").value = t.notes;
  document.getElementById("fCat").value = t.category;
  document.getElementById("fPriority").value = t.priority;
  document.getElementById("fStatus").value = t.status;
  document.getElementById("fDue").value = t.due;
  var hint = document.getElementById("formCreatedHint");
  if (t.created_at) {
    hint.textContent = "Creada el " + fmtDate(t.created_at) + " (no editable)";
    hint.style.display = "block";
  } else {
    hint.style.display = "none";
  }
  document.getElementById("modalOverlay").classList.remove("hidden");
}

function setFilter(cat) {
  activeFilter = cat;
  document.querySelectorAll(".filter-btn[data-cat]").forEach(function(b){
    b.classList.toggle("active", b.dataset.cat === cat);
  });
  render();
}

function toggleOverdue() {
  overdueOnly = !overdueOnly;
  document.getElementById("overdueToggle").classList.toggle("active", overdueOnly);
  render();
}

function onSearchInput(value) {
  searchText = (value || "").trim().toLowerCase();
  render();
}

function openModal() {
  editingId = null;
  document.getElementById("modalTitle").textContent = "Nueva tarea";
  document.getElementById("fTitle").value = "";
  document.getElementById("fNotes").value = "";
  document.getElementById("fCat").value = "personal";
  document.getElementById("fPriority").value = "media";
  document.getElementById("fStatus").value = "pendiente";
  document.getElementById("fDue").value = "";
  document.getElementById("formCreatedHint").style.display = "none";
  document.getElementById("modalOverlay").classList.remove("hidden");
  setTimeout(function(){ document.getElementById("fTitle").focus(); }, 100);
}

function closeModal() {
  document.getElementById("modalOverlay").classList.add("hidden");
}

function saveTask() {
  var title = document.getElementById("fTitle").value.trim();
  if (!title) { alert("El título es obligatorio."); return; }
  var data = {
    title: title,
    notes: document.getElementById("fNotes").value.trim(),
    category: document.getElementById("fCat").value,
    priority: document.getElementById("fPriority").value,
    status: document.getElementById("fStatus").value,
    due: document.getElementById("fDue").value
  };
  var req = editingId
    ? api("/tasks/" + editingId, { method: "PATCH", body: JSON.stringify(data) })
    : api("/tasks", { method: "POST", body: JSON.stringify(data) });
  req.then(function(saved) {
      if (editingId) {
        var idx = tasks.findIndex(function(t){ return t.id === editingId; });
        if (idx >= 0) tasks[idx] = saved;
      } else {
        tasks.push(saved);
      }
      closeModal();
      render();
    })
    .catch(function(err) { alert("Error al guardar tarea: " + err.message); });
}

function toggleDone() {
  var col = document.getElementById("col-hecho-wrap");
  var btn = document.getElementById("collapse-btn");
  var collapsed = col.classList.toggle("collapsed");
  btn.innerHTML = collapsed ? "&#x25BC;" : "&#x25B2;";
  btn.title = collapsed ? "Expandir" : "Colapsar";
}

function esc(s) {
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

function fmtDate(d) {
  if (!d) return "";
  var p = d.split("-");
  return p[2] + "/" + p[1] + "/" + p[0];
}

document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("modalOverlay").addEventListener("click", function(e){
    if (e.target === this) closeModal();
  });
  loadTasks();
});
