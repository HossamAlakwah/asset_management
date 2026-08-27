(() => {
  const csrf = document.querySelector('meta[name="csrf-token"]').content;
  const viewEl = document.getElementById("view");
  const navEl = document.getElementById("nav");
  const drawer = document.getElementById("drawer");
  const drawerBody = document.getElementById("drawer-body");
  const drawerTitle = document.getElementById("drawer-title");
  const drawerTabs = document.getElementById("drawer-tabs");
  const drawerFoot = document.getElementById("drawer-foot");
  const toastEl = document.getElementById("toast");
  const searchEl = document.getElementById("global-search");
  const userChip = document.getElementById("user-chip");
  const overlay = document.getElementById("sidebar-overlay");
  const sidebar = document.getElementById("sidebar");

  const state = {
    schema: null,
    stats: null,
    resource: null,
    page: 1,
    search: "",
    filters: {},
    rows: [],
    count: 0,
    relationCache: {},
  };

  const ICONS = {
    dashboard: '<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>',
    laptop: '<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M2 19h20"/>',
    desktop: '<rect x="4" y="3" width="16" height="12" rx="2"/><path d="M8 21h8M12 15v6"/>',
    phone: '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
    camera: '<path d="M4 8h4l2-3h4l2 3h4v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    server: '<rect x="3" y="4" width="18" height="6" rx="1.5"/><rect x="3" y="14" width="18" height="6" rx="1.5"/><path d="M7 7h.01M7 17h.01"/>',
    cube: '<path d="M12 3l9 5v8l-9 5-9-5V8z"/><path d="M12 13l9-5M12 13L3 8M12 13v9"/>',
    cloud: '<path d="M7 18h11a4 4 0 0 0 0-8 6 6 0 0 0-11-1.5A3.5 3.5 0 0 0 7 18z"/>',
    wifi: '<path d="M5 12a9 9 0 0 1 14 0M8.5 15.5a5 5 0 0 1 7 0M12 19h.01"/>',
    network: '<rect x="9" y="3" width="6" height="6" rx="1"/><rect x="3" y="15" width="6" height="6" rx="1"/><rect x="15" y="15" width="6" height="6" rx="1"/><path d="M12 9v3m0 0H6m6 0h6M6 15v-3m12 3v-3"/>',
    shield: '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>',
    lock: '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    battery: '<rect x="2" y="7" width="18" height="10" rx="2"/><path d="M22 11v2M6 11h6"/>',
    building: '<path d="M4 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16M4 21h16M9 8h.01M9 12h.01M9 16h.01M15 8h.01M15 12h.01M15 16h.01"/>',
    users: '<circle cx="9" cy="8" r="3"/><path d="M3 19a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.4"/><path d="M16 19a5 5 0 0 0 5-5"/>',
    bell: '<path d="M6 9a6 6 0 1 1 12 0c0 7 2 7 2 9H4c0-2 2-2 2-9"/><path d="M10 21h4"/>',
    mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 7 9-7"/>',
    history: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    box: '<path d="M3 8l9-5 9 5-9 5z"/><path d="M3 8v8l9 5 9-5V8M12 13v8"/>',
    chevron: '<path d="M6 9l6 6 6-6"/>',
    open: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    edit: '<path d="M4 20h4L19 9l-4-4L4 16z"/>',
    trash: '<path d="M4 7h16M9 7V5h6v2M8 7l1 13h6l1-13"/>',
    undo: '<path d="M9 14l-4-4 4-4"/><path d="M5 10h9a5 5 0 0 1 0 10H8"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
  };

  function icon(name) {
    return `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[name] || ICONS.box}</svg>`;
  }

  function initials(name) {
    return String(name || "?")
      .split(/\s+/)
      .slice(0, 2)
      .map((part) => part[0])
      .join("")
      .toUpperCase();
  }

  function statusClass(value) {
    return `status-${String(value || "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "")}`;
  }

  function collapsedGroups() {
    try {
      return new Set(JSON.parse(localStorage.getItem("ac-nav-collapsed") || "[]"));
    } catch (_error) {
      return new Set();
    }
  }

  function toggleGroup(group) {
    const groups = collapsedGroups();
    if (groups.has(group)) groups.delete(group);
    else groups.add(group);
    localStorage.setItem("ac-nav-collapsed", JSON.stringify([...groups]));
    renderNav();
  }

  function closeSidebar() {
    sidebar.classList.remove("open");
    overlay.hidden = true;
  }

  function showSkeleton(kind) {
    if (kind === "dashboard") {
      viewEl.innerHTML = `<div class="skeleton-page"><div class="summary">${"<div class='skeleton skeleton-card'></div>".repeat(4)}</div><div class="cards">${"<div class='skeleton skeleton-card'></div>".repeat(8)}</div></div>`;
      return;
    }
    viewEl.innerHTML = `<div class="skeleton-page"><div class="skeleton" style="height:48px;width:46%"></div><div class="skeleton skeleton-card" style="height:360px"></div></div>`;
  }

  async function loadStats(force = false) {
    if (!force && state.stats) return state.stats;
    state.stats = await api("/api/v1/stats/");
    return state.stats;
  }

  function invalidateStats() {
    state.stats = null;
  }

  const headers = () => ({
    "X-CSRFToken": csrf,
    Accept: "application/json",
  });

  async function api(url, options = {}) {
    const opts = {
      credentials: "same-origin",
      ...options,
      headers: { ...headers(), ...(options.headers || {}) },
    };
    const response = await fetch(url, opts);
    const contentType = response.headers.get("content-type") || "";
    const isJson = contentType.includes("application/json");
    const payload = isJson ? await response.json() : await response.blob();
    if (!response.ok) {
      const message = isJson
        ? formatErrors(payload)
        : `Request failed (${response.status})`;
      throw new Error(message);
    }
    return payload;
  }

  function formatErrors(payload) {
    if (!payload) return "Request failed.";
    if (typeof payload.detail === "string") return payload.detail;
    if (Array.isArray(payload.errors)) {
      return payload.errors
        .map((row) => `Row ${row.row}: ${formatErrors(row.errors)}`)
        .join("\n");
    }
    if (typeof payload === "object") {
      return Object.entries(payload)
        .map(([key, value]) => `${key}: ${[].concat(value).join(", ")}`)
        .join("\n");
    }
    return String(payload);
  }

  function toast(message, kind = "ok") {
    toastEl.hidden = false;
    toastEl.className = `toast ${kind}`;
    toastEl.textContent = message;
    clearTimeout(toastEl._t);
    toastEl._t = setTimeout(() => {
      toastEl.hidden = true;
    }, 4200);
  }

  function resourceByKey(key) {
    return state.schema.resources.find((item) => item.key === key);
  }

  function parseHash() {
    const raw = (location.hash || "#/dashboard").replace(/^#/, "");
    const parts = raw.split("/").filter(Boolean);
    return { page: parts[0] || "dashboard", id: parts[1] || null };
  }

  function go(hash) {
    location.hash = hash;
  }

  function renderNav() {
    const groups = {};
    for (const resource of state.schema.resources) {
      groups[resource.group] = groups[resource.group] || [];
      groups[resource.group].push(resource);
    }
    const current = parseHash();
    const collapsed = collapsedGroups();
    const counts = Object.fromEntries((state.stats?.cards || []).map((card) => [card.key, card.total]));
    navEl.innerHTML = `
      <a href="#/dashboard" class="nav-dashboard ${current.page === "dashboard" ? "active" : ""}">${icon("dashboard")}<span>Dashboard</span></a>
      <a href="#/notifications" class="nav-link ${current.page === "notifications" ? "active" : ""}">${icon("bell")}<span>Notifications</span></a>
      <a href="#/security" class="nav-link ${current.page === "security" ? "active" : ""}">${icon("lock")}<span>Security</span></a>
      ${Object.entries(groups)
        .map(([group, items]) => {
          const isCollapsed = collapsed.has(group);
          return `
        <button type="button" class="nav-group ${isCollapsed ? "collapsed" : ""}" data-group="${group}">
          <span>${group}</span>${icon("chevron")}
        </button>
        <div class="nav-items ${isCollapsed ? "collapsed" : ""}">
          ${items
            .map(
              (item) => `
            <a href="#/${item.key}" class="nav-link ${current.page === item.key ? "active" : ""}">
              ${icon(item.icon)}
              <span>${item.title}</span>
              ${counts[item.key] != null ? `<span class="nav-count">${counts[item.key]}</span>` : ""}
            </a>
          `
            )
            .join("")}
        </div>`;
        })
        .join("")}
    `;
    navEl.querySelectorAll("[data-group]").forEach((button) => {
      button.addEventListener("click", () => toggleGroup(button.dataset.group));
    });
    navEl.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", closeSidebar);
    });
  }

  async function loadRelation(key) {
    if (!key) return [];
    if (state.relationCache[key]) return state.relationCache[key];
    const data = await api(`/api/v1/${key}/?page_size=500`);
    const rows = data.results || data;
    state.relationCache[key] = rows;
    return rows;
  }

  function fieldValue(row, name) {
    const value = row[name];
    if (value === null || value === undefined || value === "") return "—";
    if (typeof value === "boolean") return value ? "Yes" : "No";
    if (Array.isArray(value)) {
      if (!value.length) return "—";
      if (name === "storage_devices") {
        return value
          .map((item) => [item.size, item.type].filter(Boolean).join(" "))
          .join(", ");
      }
      return value
        .map((item) => (typeof item === "object" ? JSON.stringify(item) : item))
        .join(", ");
    }
    return value;
  }

  function singularTitle(title) {
    if (title.endsWith("ies")) return `${title.slice(0, -3)}y`;
    if (title.endsWith("s") && !title.endsWith("ss")) return title.slice(0, -1);
    return title;
  }

  function inputValue(field, value) {
    if (value === null || value === undefined || value === "") return "";
    const text = String(value);
    if (field.type === "date") return text.slice(0, 10);
    if (field.type === "datetime") return text.length >= 16 ? text.slice(0, 16) : text;
    return text;
  }

  async function prefetchRelations(fields) {
    const keys = [
      ...new Set(
        fields
          .filter((field) => field.type === "relation" && field.resource)
          .map((field) => field.resource)
      ),
    ];
    await Promise.all(keys.map(loadRelation));
  }

  function formatWhen(value) {
    if (!value) return "";
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleString();
  }

  function changeLine(label, from, to) {
    const start = from || "—";
    const end = to || "—";
    if (start === end) return "";
    return `${label}: ${start} → ${end}`;
  }

  function logLines(log) {
    const lines = [
      changeLine("Status", log.old_status, log.new_status),
      changeLine(
        "Employee",
        log.old_employee_name || log.old_employee,
        log.new_employee_name || log.new_employee
      ),
      log.old_branch_name || log.new_branch_name
        ? changeLine("Branch", log.old_branch_name, log.new_branch_name)
        : log.branch_name
          ? `Branch: ${log.branch_name}`
          : "",
      changeLine("Location", log.old_location, log.new_location),
      changeLine("IP", log.old_ip_address, log.new_ip_address),
      log.on_hand_date ? `On hand: ${log.on_hand_date}` : "",
      log.return_date ? `Returned: ${log.return_date}` : "",
      log.comment || "",
    ].filter(Boolean);
    if (!lines.length) lines.push("Change recorded");
    return lines;
  }

  function renderLogs(logs) {
    if (!logs || !logs.length) {
      return `<p class="muted">No log entries yet for this device.</p>`;
    }
    return `<div class="logs">${logs
      .map(
        (log) => `<article class="log">
          <div>${escapeHtml(log.new_status || log.comment || "Change")}</div>
          <div class="muted">${escapeHtml(formatWhen(log.change_time))} · ${escapeHtml(
            log.changed_by_username || "system"
          )}</div>
          <ul>${logLines(log)
            .map((line) => `<li>${escapeHtml(line)}</li>`)
            .join("")}</ul>
        </article>`
      )
      .join("")}</div>`;
  }

  function showTabs(tabs, active) {
    if (!tabs.length) {
      drawerTabs.hidden = true;
      drawerTabs.innerHTML = "";
      return;
    }
    drawerTabs.hidden = false;
    drawerTabs.innerHTML = tabs
      .map(
        (tab) =>
          `<button type="button" data-tab="${tab.id}" class="${
            tab.id === active ? "active" : ""
          }">${tab.label}</button>`
      )
      .join("");
    drawerTabs.querySelectorAll("[data-tab]").forEach((button) => {
      button.addEventListener("click", () => selectTab(button.dataset.tab));
    });
    selectTab(active || tabs[0].id);
  }

  function selectTab(id) {
    drawerTabs.querySelectorAll("[data-tab]").forEach((button) => {
      button.classList.toggle("active", button.dataset.tab === id);
    });
    drawerBody.querySelectorAll("[data-pane]").forEach((pane) => {
      pane.hidden = pane.dataset.pane !== id;
    });
  }

  function setFooter(html) {
    if (!html) {
      drawerFoot.hidden = true;
      drawerFoot.innerHTML = "";
      return;
    }
    drawerFoot.hidden = false;
    drawerFoot.innerHTML = html;
  }

  function writableFields(resource, { creating } = {}) {
    return resource.fields.filter((field) => {
      if (field.read_only) return false;
      if (creating && field.omit_on_create) return false;
      return true;
    });
  }

  function cellHtml(resource, name, row) {
    const field = resource.fields.find((item) => item.name === name);
    const raw = row[name];
    if (name === "status" || name === "environment" || name === "role") {
      return `<span class="pill ${statusClass(raw)}">${escapeHtml(fieldValue(row, name))}</span>`;
    }
    if (field?.type === "boolean") {
      return `<span class="pill ${raw ? "status-yes" : "status-stock"}">${raw ? "Yes" : "No"}</span>`;
    }
    return escapeHtml(fieldValue(row, name));
  }

  async function renderDashboard() {
    const stats = await loadStats();
    const total = stats.cards.reduce((sum, card) => sum + card.total, 0);
    const stock = stats.cards.reduce((sum, card) => sum + (card.in_stock || 0), 0);
    const inUse = stats.cards.reduce((sum, card) => sum + (card.by_status["In Use"] || 0), 0);
    const groups = {};
    for (const card of stats.cards) {
      groups[card.group] = groups[card.group] || [];
      groups[card.group].push(card);
    }
    const groupOrder = [
      "Organisation",
      "Endpoints",
      "Infrastructure",
      "Compute",
      "Notifications",
      "Administration",
    ];
    const groupLabels = { Endpoints: "Assets" };
    const orderedGroups = [
      ...groupOrder.filter((name) => groups[name]),
      ...Object.keys(groups).filter((name) => !groupOrder.includes(name)),
    ];
    const alertStats = stats.alerts || { total: 0, active: 0 };
    viewEl.innerHTML = `
      <div class="page-head">
        <div>
          <div class="kicker">Overview</div>
          <h1>Dashboard</h1>
          <p class="muted">Inventory grouped by section.</p>
        </div>
      </div>
      <div class="summary">
        <article class="summary-card"><div class="label">Total records</div><div class="value">${total}</div></article>
        <article class="summary-card"><div class="label">In use</div><div class="value">${inUse}</div></article>
        <article class="summary-card"><div class="label">In stock</div><div class="value">${stock}</div></article>
        <article class="summary-card"><div class="label">Sections</div><div class="value">${orderedGroups.length}</div></article>
      </div>
      <div class="dash-sections">
        ${orderedGroups
          .map((group) => {
            const cards = groups[group];
            const sectionTotal = cards.reduce((sum, card) => sum + card.total, 0);
            return `
        <section class="dash-section">
          <header class="section-head">
            <h2>${groupLabels[group] || group}</h2>
            <span class="muted">${cards.length} type${cards.length === 1 ? "" : "s"} · ${sectionTotal}</span>
          </header>
          <div class="cards">
            ${cards
              .map((card) => {
                const statuses = Object.entries(card.by_status).slice(0, 2);
                return `
              <a class="card" href="#/${card.key}">
                <div class="card-top">
                  <div class="card-icon">${icon(card.icon)}</div>
                </div>
                <h3>${card.title}</h3>
                <div class="total">${card.total}</div>
                ${
                  statuses.length
                    ? `<div class="status-pills">${statuses
                        .map(([name, count]) => `<span class="pill ${statusClass(name)}">${name}: ${count}</span>`)
                        .join("")}</div>`
                    : ""
                }
              </a>`;
              })
              .join("")}
          </div>
        </section>`;
          })
          .join("")}
      </div>
      <section class="dash-section">
        <header class="section-head">
          <h2>Notifications</h2>
          <span class="muted">${alertStats.active} active</span>
        </header>
        <div class="cards">
          <a class="card" href="#/notifications">
            <div class="card-top"><div class="card-icon">${icon("bell")}</div></div>
            <h3>Stock alerts</h3>
            <div class="total">${alertStats.total}</div>
            <div class="status-pills">
              <span class="pill status-in-use">Active: ${alertStats.active}</span>
            </div>
          </a>
        </div>
      </section>
    `;
    renderNav();
  }

  async function renderList(resource) {
    const params = new URLSearchParams({ page: String(state.page) });
    if (state.search) params.set("search", state.search);
    for (const [key, value] of Object.entries(state.filters)) {
      if (value) params.set(key, value);
    }
    const data = await api(`${resource.endpoint}?${params.toString()}`);
    state.rows = data.results || data;
    state.count = data.count ?? state.rows.length;
    const columns = resource.list_fields;
    const canWrite = state.schema.user.is_admin && !resource.read_only;

    const filterControls = resource.filter_fields
      .map((name) => {
        const field = resource.fields.find((item) => item.name === name);
        if (!field || field.type === "relation") {
          return `<input class="grow" data-filter="${name}" placeholder="Filter ${name}" value="${state.filters[name] || ""}">`;
        }
        if (field.type === "choice") {
          return `<select data-filter="${name}">
            <option value="">All ${field.label}</option>
            ${field.choices
              .map(
                (choice) =>
                  `<option value="${choice.value}" ${
                    state.filters[name] === String(choice.value) ? "selected" : ""
                  }>${choice.label}</option>`
              )
              .join("")}
          </select>`;
        }
        return "";
      })
      .join("");

    viewEl.innerHTML = `
      <div class="page-head">
        <div>
          <div class="kicker">${resource.group}</div>
          <h1>${resource.title}</h1>
          <p class="muted">${state.count} record${state.count === 1 ? "" : "s"}</p>
        </div>
        <div class="actions">
          ${
            resource.supports_excel
              ? `
            <button class="ghost" data-act="template">Template</button>
            <button class="ghost" data-act="export">Export</button>
            <label class="ghost" style="display:inline-flex;align-items:center;gap:.4rem;">
              Import
              <input type="file" accept=".xlsx,.xlsm" data-act="import" hidden>
            </label>
          `
              : ""
          }
          ${canWrite ? `<button class="primary" data-act="create">${icon("plus")}New</button>` : ""}
        </div>
      </div>
      <div class="toolbar">${filterControls || `<span class="muted">No extra filters for this list.</span>`}</div>
      <div class="table-wrap">
        ${
          state.rows.length
            ? `<table>
          <thead><tr>${columns
            .map((col) => `<th>${labelFor(resource, col)}</th>`)
            .join("")}<th></th></tr></thead>
          <tbody>
            ${state.rows
              .map(
                (row) => `<tr data-id="${row.id}">
                  ${columns.map((col) => `<td>${cellHtml(resource, col, row)}</td>`).join("")}
                  <td>
                    <div class="row-actions">
                      <button class="icon-btn" data-act="view" data-id="${row.id}" title="Open">${icon("open")}</button>
                      ${
                        resource.log_field
                          ? `<button class="icon-btn" data-act="history" data-id="${row.id}" title="History">${icon("history")}</button>`
                          : ""
                      }
                      ${
                        canWrite
                          ? `<button class="icon-btn" data-act="edit" data-id="${row.id}" title="Edit">${icon("edit")}</button>`
                          : ""
                      }
                      ${
                        canWrite && resource.actions.includes("unassign") && row.employee
                          ? `<button class="icon-btn" data-act="unassign" data-id="${row.id}" title="Unassign">${icon("undo")}</button>`
                          : ""
                      }
                      ${
                        canWrite
                          ? `<button class="icon-btn" data-act="delete" data-id="${row.id}" title="Delete">${icon("trash")}</button>`
                          : ""
                      }
                    </div>
                  </td>
                </tr>`
              )
              .join("")}
          </tbody>
        </table>`
            : `<div class="empty"><strong>No records yet</strong>Try another filter, or create a new ${singularTitle(resource.title).toLowerCase()}.</div>`
        }
      </div>
      <div class="pager">
        <button class="ghost" data-act="prev" ${state.page <= 1 ? "disabled" : ""}>Previous</button>
        <span>Page ${state.page}</span>
        <button class="ghost" data-act="next" ${
          !data.next ? "disabled" : ""
        }>Next</button>
      </div>
    `;

    viewEl.querySelectorAll("[data-filter]").forEach((el) => {
      el.addEventListener("change", () => {
        state.filters[el.dataset.filter] = el.value;
        state.page = 1;
        render();
      });
    });
    viewEl.querySelector("[data-act='create']")?.addEventListener("click", () => openForm(resource));
    viewEl.querySelector("[data-act='template']")?.addEventListener("click", () => downloadFile(`${resource.endpoint}excel-template/`, `${resource.key}_template.xlsx`));
    viewEl.querySelector("[data-act='export']")?.addEventListener("click", () => {
      const exportParams = new URLSearchParams(params);
      downloadFile(`${resource.endpoint}export/?${exportParams}`, `${resource.key}.xlsx`);
    });
    viewEl.querySelector("[data-act='import']")?.addEventListener("change", async (event) => {
      const file = event.target.files[0];
      if (!file) return;
      const body = new FormData();
      body.append("file", file);
      try {
        const result = await api(`${resource.endpoint}import/`, { method: "POST", body });
        toast(`Imported ${result.created} row(s). ${result.failed || 0} failed.`, result.failed ? "err" : "ok");
        invalidateStats();
        render();
      } catch (error) {
        toast(error.message, "err");
      }
    });
    viewEl.querySelector("[data-act='prev']")?.addEventListener("click", () => {
      state.page = Math.max(1, state.page - 1);
      render();
    });
    viewEl.querySelector("[data-act='next']")?.addEventListener("click", () => {
      state.page += 1;
      render();
    });
    viewEl.querySelectorAll("[data-act='view']").forEach((btn) =>
      btn.addEventListener("click", (event) => {
        event.stopPropagation();
        openDetail(resource, btn.dataset.id);
      })
    );
    viewEl.querySelectorAll("[data-act='history']").forEach((btn) =>
      btn.addEventListener("click", (event) => {
        event.stopPropagation();
        openDetail(resource, btn.dataset.id, "history");
      })
    );
    viewEl.querySelectorAll("[data-act='edit']").forEach((btn) =>
      btn.addEventListener("click", (event) => {
        event.stopPropagation();
        openForm(resource, btn.dataset.id);
      })
    );
    viewEl.querySelectorAll("[data-act='unassign']").forEach((btn) =>
      btn.addEventListener("click", (event) => {
        event.stopPropagation();
        unassign(resource, btn.dataset.id);
      })
    );
    viewEl.querySelectorAll("[data-act='delete']").forEach((btn) =>
      btn.addEventListener("click", (event) => {
        event.stopPropagation();
        destroy(resource, btn.dataset.id);
      })
    );
    viewEl.querySelectorAll("tbody tr").forEach((row) => {
      row.addEventListener("click", (event) => {
        if (event.target.closest("button, a, label, input")) return;
        openDetail(resource, row.dataset.id);
      });
    });
  }

  function labelFor(resource, name) {
    return resource.fields.find((field) => field.name === name)?.label || name;
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  async function downloadFile(url, filename) {
    const response = await fetch(url, { credentials: "same-origin", headers: headers() });
    if (!response.ok) {
      toast("Download failed.", "err");
      return;
    }
    const blob = await response.blob();
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    URL.revokeObjectURL(link.href);
  }

  async function openDetail(resource, id, tab = "details") {
    const row = await api(`${resource.endpoint}${id}/`);
    const label = row.serial || row.serial_number || row.hostname || row.name || `#${id}`;
    drawerTitle.textContent = `${singularTitle(resource.title)} · ${label}`;
    const canWrite = state.schema.user.is_admin && !resource.read_only;
    const details = `<div class="detail-grid">${resource.fields
      .map((field) => {
        const wide = field.type === "nested" || field.type === "text" ? "span-2" : "";
        return `<div class="field ${wide}"><span>${field.label}</span><strong>${escapeHtml(
          fieldValue(row, field.name)
        )}</strong></div>`;
      })
      .join("")}</div>`;
    const hasLogs = Boolean(resource.log_field);
    drawerBody.innerHTML = `
      <div data-pane="details">${details}</div>
      ${hasLogs ? `<div data-pane="history">${renderLogs(row[resource.log_field])}</div>` : ""}
    `;
    showTabs(
      hasLogs
        ? [
            { id: "details", label: "Details" },
            { id: "history", label: "History" },
          ]
        : [],
      tab
    );
    setFooter(
      canWrite
        ? `
          <button class="primary" type="button" data-detail="edit">Edit</button>
          ${
            resource.actions.includes("unassign") && row.employee
              ? `<button class="ghost" type="button" data-detail="unassign">Unassign</button>`
              : ""
          }
          <button class="danger" type="button" data-detail="delete">Delete</button>
        `
        : ""
    );
    drawer.hidden = false;
    drawerFoot.querySelector("[data-detail='edit']")?.addEventListener("click", () =>
      openForm(resource, id)
    );
    drawerFoot.querySelector("[data-detail='unassign']")?.addEventListener("click", async () => {
      await unassign(resource, id);
      closeDrawer();
    });
    drawerFoot.querySelector("[data-detail='delete']")?.addEventListener("click", async () => {
      await destroy(resource, id);
      closeDrawer();
    });
  }

  async function openForm(resource, id = null, tab = "details") {
    const row = id ? await api(`${resource.endpoint}${id}/`) : {};
    const itemName = singularTitle(resource.title);
    drawerTitle.textContent = id
      ? `Edit ${itemName}`
      : `New ${itemName}`;
    const fields = writableFields(resource, { creating: !id });
    await prefetchRelations(fields);
    const html = [];
    for (const field of fields) {
      html.push(await renderField(field, row[field.name], row));
    }
    const hasLogs = Boolean(id && resource.log_field);
    drawerBody.innerHTML = `
      <div data-pane="details">
        <form id="record-form" class="form-grid">${html.join("")}</form>
      </div>
      ${hasLogs ? `<div data-pane="history">${renderLogs(row[resource.log_field])}</div>` : ""}
    `;
    showTabs(
      hasLogs
        ? [
            { id: "details", label: "Details" },
            { id: "history", label: "History" },
          ]
        : [],
      tab
    );
    setFooter(`
      <button class="ghost" type="button" id="form-cancel">Cancel</button>
      <button class="primary" type="submit" form="record-form">Save</button>
      <div class="error" id="form-error"></div>
    `);
    drawer.hidden = false;
    document.getElementById("form-cancel").addEventListener("click", closeDrawer);
    drawerBody.querySelector("#record-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = {};
      for (const field of fields) {
        if (field.type === "nested") {
          payload[field.name] = collectNested(field, event.target);
          continue;
        }
        const input = event.target.elements[field.name];
        if (!input) continue;
        if (field.type === "relation" && field.many) {
          payload[field.name] = [...input.selectedOptions].map((option) => Number(option.value));
          continue;
        }
        payload[field.name] = coerce(field, input.value, input.type === "checkbox" ? input.checked : undefined);
      }
      try {
        await api(id ? `${resource.endpoint}${id}/` : resource.endpoint, {
          method: id ? "PUT" : "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        toast("Saved.");
        closeDrawer();
        invalidateStats();
        render();
      } catch (error) {
        document.getElementById("form-error").textContent = error.message;
      }
    });
  }

  async function renderField(field, value, row) {
    const required = field.required ? "required" : "";
    const wide =
      field.type === "nested" || field.type === "text" || field.type === "boolean"
        ? "span-2"
        : "";
    if (field.type === "boolean") {
      return `<label class="field ${wide}"><span>${field.label}</span><input type="checkbox" name="${field.name}" ${value ? "checked" : ""}></label>`;
    }
    if (field.type === "choice") {
      return `<label class="field ${wide}"><span>${field.label}</span>
        <select name="${field.name}" ${required}>
          <option value="">Select…</option>
          ${field.choices
            .map(
              (choice) =>
                `<option value="${choice.value}" ${
                  String(value) === String(choice.value) ? "selected" : ""
                }>${choice.label}</option>`
            )
            .join("")}
        </select></label>`;
    }
    if (field.type === "relation") {
      const options = field.resource ? await loadRelation(field.resource) : [];
      const related = resourceByKey(field.resource);
      const labelKeys = related?.option_fields || ["name", "username", "serial"];
      const many = field.many;
      const selected = many ? (value || []).map(String) : [String(value ?? "")];
      return `<label class="field ${wide}"><span>${field.label}</span>
        <select name="${field.name}" ${many ? "multiple" : ""} ${required}>
          ${many ? "" : `<option value="">None</option>`}
          ${options
            .map((option) => {
              const label = labelKeys.map((key) => option[key]).filter(Boolean).join(" · ") || option.id;
              const isSelected = selected.includes(String(option.id)) ? "selected" : "";
              return `<option value="${option.id}" ${isSelected}>${escapeHtml(label)}</option>`;
            })
            .join("")}
        </select></label>`;
    }
    if (field.type === "nested") {
      const rows = Array.isArray(value) && value.length ? value : [{}];
      return `<div class="field ${wide}"><span>${field.label}</span>
        <div id="nested-${field.name}">
          ${rows.map((item, index) => nestedRow(field, item, index)).join("")}
        </div>
        <button class="ghost" type="button" data-add-nested="${field.name}">Add row</button>
      </div>`;
    }
    if (field.type === "text") {
      return `<label class="field ${wide}"><span>${field.label}</span><textarea name="${field.name}" rows="3">${escapeHtml(value || "")}</textarea></label>`;
    }
    const type =
      field.type === "date" ? "date" :
      field.type === "datetime" ? "datetime-local" :
      field.type === "integer" || field.type === "float" ? "number" :
      field.type === "email" ? "email" : "text";
    const step = field.type === "float" ? "any" : undefined;
    const display = inputValue(field, value);
    return `<label class="field ${wide}"><span>${field.label}</span><input type="${type}" name="${field.name}" value="${escapeHtml(display)}" ${required} ${step ? `step="${step}"` : ""}></label>`;
  }

  function nestedRow(field, item, index) {
    return `<div class="nested" data-nested="${field.name}">
      ${field.fields
        .map((child) => {
          if (child.read_only) return "";
          if (child.type === "choice") {
            return `<label class="field"><span>${child.label}</span>
              <select name="${field.name}.${index}.${child.name}">
                <option value="">Select…</option>
                ${child.choices
                  .map(
                    (choice) =>
                      `<option value="${choice.value}" ${
                        item[child.name] === choice.value ? "selected" : ""
                      }>${choice.label}</option>`
                  )
                  .join("")}
              </select></label>`;
          }
          return `<label class="field"><span>${child.label}</span>
            <input name="${field.name}.${index}.${child.name}" value="${escapeHtml(item[child.name] ?? "")}">
          </label>`;
        })
        .join("")}
    </div>`;
  }

  function collectNested(field, form) {
    const blocks = [...form.querySelectorAll(`[data-nested="${field.name}"]`)];
    return blocks
      .map((block, index) => {
        const row = {};
        for (const child of field.fields) {
          if (child.read_only) continue;
          const input = block.querySelector(`[name="${field.name}.${index}.${child.name}"]`);
          if (!input || input.value === "") continue;
          row[child.name] = input.value;
        }
        return row;
      })
      .filter((row) => Object.keys(row).length);
  }

  function coerce(field, value, checked) {
    if (field.type === "boolean") return Boolean(checked);
    if (value === "") return field.required ? value : null;
    if (field.type === "integer") return Number(value);
    if (field.type === "float") return Number(value);
    if (field.type === "relation") return value ? Number(value) : null;
    return value;
  }

  async function unassign(resource, id) {
    try {
      await api(`${resource.endpoint}${id}/unassign/`, { method: "POST" });
      toast("Device returned to stock.");
      invalidateStats();
      render();
    } catch (error) {
      toast(error.message, "err");
    }
  }

  async function destroy(resource, id) {
    if (!confirm("Delete this record?")) return;
    try {
      await api(`${resource.endpoint}${id}/`, { method: "DELETE" });
      toast("Deleted.");
      invalidateStats();
      render();
    } catch (error) {
      toast(error.message, "err");
    }
  }

  function closeDrawer() {
    drawer.hidden = true;
    drawerBody.innerHTML = "";
    drawerTabs.hidden = true;
    drawerTabs.innerHTML = "";
    setFooter("");
    drawerTitle.textContent = "Record";
  }

  function modelLabel(value) {
    return (state.schema.alerts?.models || []).find((item) => item.value === value)?.label || value;
  }

  async function renderNotifications() {
    const endpoint = state.schema.alerts?.endpoint || "/api/v1/notification-configs/";
    const sentEndpoint = state.schema.alerts?.sent_endpoint || "/api/v1/sent-notifications/";
    const models = state.schema.alerts?.models || [];
    const canWrite = state.schema.user.is_admin;
    const [rulesData, sentData] = await Promise.all([
      api(`${endpoint}?page_size=100`),
      api(`${sentEndpoint}?page_size=25`),
    ]);
    const rules = rulesData.results || rulesData;
    const sent = sentData.results || sentData;

    viewEl.innerHTML = `
      <div class="page-head">
        <div>
          <div class="kicker">Alerts</div>
          <h1>Notifications</h1>
          <p class="muted">Create a stock alert, choose what it should do, and pick who receives it — all on this screen.</p>
        </div>
      </div>
      <div class="alert-layout">
        <form id="alert-form" class="alert-composer" ${canWrite ? "" : "hidden"}>
          <input type="hidden" name="rule_id" value="">
          <h2>Create alert</h2>
          <label class="field">
            <span>Watch this inventory</span>
            <select name="model_name" required>
              <option value="">Select an asset type…</option>
              ${models.map((item) => `<option value="${item.value}">${item.label}</option>`).join("")}
            </select>
          </label>
          <label class="field">
            <span>When stock is at or below</span>
            <input type="number" name="condition_value" min="0" step="1" required placeholder="e.g. 2">
          </label>
          <label class="field">
            <span>Then send this email</span>
            <textarea name="notification_message" rows="4" placeholder="Low stock: {model} is at {count} (threshold {threshold})."></textarea>
            <small class="muted">Placeholders: {model}, {count}, {threshold}</small>
          </label>
          <div class="field">
            <span>Recipients</span>
            <div class="chip-row">
              <input type="email" id="alert-email" placeholder="name@company.com">
              <button class="ghost" type="button" id="alert-add-email">Add</button>
            </div>
            <div id="alert-chips" class="chips"></div>
          </div>
          <label class="field check">
            <input type="checkbox" name="is_active" checked>
            <span>Active — send mail when the threshold is hit</span>
          </label>
          <div class="actions">
            <button class="primary" type="submit">Save alert</button>
            <button class="ghost" type="button" id="alert-reset">Clear</button>
          </div>
          <div class="error" id="alert-error"></div>
        </form>
        <div class="alert-side">
          <h2>Saved alerts</h2>
          ${
            rules.length
              ? rules
                  .map(
                    (rule) => `
            <article class="alert-rule ${rule.is_active ? "" : "inactive"}" data-id="${rule.id}">
              <div>
                <strong>${escapeHtml(modelLabel(rule.model_name))}</strong>
                <div class="muted">Email when stock ≤ ${escapeHtml(rule.condition_value)}</div>
                <div class="chips">
                  ${(rule.recipients || [])
                    .map((email) => `<span class="chip">${escapeHtml(email)}</span>`)
                    .join("") || `<span class="muted">No recipients yet</span>`}
                </div>
              </div>
              <div class="row-actions">
                ${canWrite ? `<button class="icon-btn" data-alert="edit" data-id="${rule.id}" title="Edit">${icon("edit")}</button>` : ""}
                ${canWrite ? `<button class="icon-btn" data-alert="run" data-id="${rule.id}" title="Run now">${icon("bell")}</button>` : ""}
                ${canWrite ? `<button class="icon-btn" data-alert="delete" data-id="${rule.id}" title="Delete">${icon("trash")}</button>` : ""}
              </div>
            </article>`
                  )
                  .join("")
              : `<div class="empty"><strong>No alerts yet</strong>Use the form to watch an asset type and email people when stock is low.</div>`
          }
        </div>
      </div>
      <section class="dash-section" style="margin-top:1rem;">
        <header class="section-head">
          <h2>Delivery log</h2>
          <span class="muted">${sent.length} recent</span>
        </header>
        ${
          sent.length
            ? `<div class="table-wrap"><table>
                <thead><tr><th>When</th><th>Alert</th><th>Recipient</th><th>Message</th></tr></thead>
                <tbody>
                  ${sent
                    .map(
                      (row) => `<tr>
                        <td>${escapeHtml(formatWhen(row.sent_at))}</td>
                        <td>${escapeHtml(row.config_label || row.triggered_by || "—")}</td>
                        <td>${escapeHtml(row.recipient_email || "—")}</td>
                        <td>${escapeHtml((row.message || "").slice(0, 120))}</td>
                      </tr>`
                    )
                    .join("")}
                </tbody>
              </table></div>`
            : `<p class="muted">Nothing has been sent yet. Save an alert with recipients, then click Run now or wait for the stock check.</p>`
        }
      </section>
    `;

    const form = document.getElementById("alert-form");
    if (!form) return;
    const chipsEl = document.getElementById("alert-chips");
    let emails = [];

    function renderChips() {
      chipsEl.innerHTML = emails
        .map(
          (email) =>
            `<button type="button" class="chip" data-remove="${escapeHtml(email)}">${escapeHtml(email)} ×</button>`
        )
        .join("");
      chipsEl.querySelectorAll("[data-remove]").forEach((button) => {
        button.addEventListener("click", () => {
          emails = emails.filter((item) => item !== button.dataset.remove);
          renderChips();
        });
      });
    }

    function addEmail() {
      const input = document.getElementById("alert-email");
      const value = (input.value || "").trim().toLowerCase();
      if (!value || !value.includes("@")) {
        toast("Enter a valid email address.", "err");
        return;
      }
      if (!emails.includes(value)) emails.push(value);
      input.value = "";
      renderChips();
    }

    function fillForm(rule) {
      form.elements.rule_id.value = rule?.id || "";
      form.elements.model_name.value = rule?.model_name || "";
      form.elements.condition_value.value = rule?.condition_value || "";
      form.elements.notification_message.value = rule?.notification_message || "";
      form.elements.is_active.checked = rule ? Boolean(rule.is_active) : true;
      emails = [...(rule?.recipients || [])];
      form.querySelector("h2").textContent = rule ? "Edit alert" : "Create alert";
      document.getElementById("alert-error").textContent = "";
      renderChips();
    }

    document.getElementById("alert-add-email").addEventListener("click", addEmail);
    document.getElementById("alert-email").addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        addEmail();
      }
    });
    document.getElementById("alert-reset").addEventListener("click", () => fillForm(null));

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = {
        model_name: form.elements.model_name.value,
        condition_type: "stock_count",
        condition_value: String(form.elements.condition_value.value),
        notification_message: form.elements.notification_message.value,
        is_active: form.elements.is_active.checked,
        recipients: emails,
      };
      const id = form.elements.rule_id.value;
      try {
        await api(id ? `${endpoint}${id}/` : endpoint, {
          method: id ? "PUT" : "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        toast(id ? "Alert updated." : "Alert created.");
        invalidateStats();
        render();
      } catch (error) {
        document.getElementById("alert-error").textContent = error.message;
      }
    });

    viewEl.querySelectorAll("[data-alert='edit']").forEach((button) => {
      button.addEventListener("click", () => {
        const rule = rules.find((item) => String(item.id) === button.dataset.id);
        fillForm(rule);
        form.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
    viewEl.querySelectorAll("[data-alert='run']").forEach((button) => {
      button.addEventListener("click", async () => {
        try {
          const result = await api(`${endpoint}${button.dataset.id}/run/`, { method: "POST" });
          if (result.triggered) {
            toast(`Threshold hit (stock ${result.stock}). Emailed ${result.emailed} recipient(s).`);
          } else {
            toast(`Stock is OK (${result.stock} above ${result.threshold}). No email sent.`);
          }
          render();
        } catch (error) {
          toast(error.message, "err");
        }
      });
    });
    viewEl.querySelectorAll("[data-alert='delete']").forEach((button) => {
      button.addEventListener("click", async () => {
        if (!confirm("Delete this alert?")) return;
        try {
          await api(`${endpoint}${button.dataset.id}/`, { method: "DELETE" });
          toast("Alert deleted.");
          invalidateStats();
          render();
        } catch (error) {
          toast(error.message, "err");
        }
      });
    });
  }

  async function renderSecurity() {
    viewEl.innerHTML = `
      <div class="security-hero">
        <div>
          <div class="kicker">Account</div>
          <h1>Security</h1>
          <p class="muted">Every account must sign in with a password and an authenticator. This cannot be turned off in the console.</p>
        </div>
        <span class="badge-on">2FA required</span>
      </div>
      <div class="security-grid">
        <section class="security-card">
          <h3>Authenticator app</h3>
          <p>You enrolled at first sign-in. Later visits need the 6-digit code or a leftover backup code. If the device is lost, an operator runs <code>python manage.py disable_2fa ${escapeHtml(state.schema.user.username)}</code> and you enroll again at login.</p>
        </section>
        <section class="security-card">
          <h3>Sign-in protection</h3>
          <p>Five failed passwords from the same username or IP lock that sign-in for 15 minutes. Django Admin uses this same login page.</p>
          <p>Password reset and stock alerts go out through SMTP once <code>EMAIL_HOST</code> is set. Until then, local debug prints mail in the server terminal.</p>
        </section>
      </div>
    `;
  }

  async function render() {
    const route = parseHash();
    const switching = state.resource !== route.page;
    if (switching) showSkeleton(route.page === "dashboard" ? "dashboard" : "list");
    try {
      await loadStats();
    } catch (_error) {
      /* Nav counts are optional. */
    }
    renderNav();
    if (route.page === "dashboard") {
      searchEl.value = "";
      searchEl.placeholder = "Search a list after you open one…";
      state.resource = "dashboard";
      await renderDashboard();
      return;
    }
    if (route.page === "notifications") {
      searchEl.value = "";
      searchEl.placeholder = "Search is on each list page…";
      state.resource = "notifications";
      await renderNotifications();
      return;
    }
    if (route.page === "security") {
      searchEl.value = "";
      searchEl.placeholder = "Search is on each list page…";
      state.resource = "security";
      await renderSecurity();
      return;
    }
    searchEl.placeholder = "Search this list…";
    const resource = resourceByKey(route.page);
    if (!resource) {
      viewEl.innerHTML = `<div class="empty"><strong>Unknown page</strong>That section is not in the schema.</div>`;
      return;
    }
    if (state.resource !== resource.key) {
      state.resource = resource.key;
      state.page = 1;
      state.filters = {};
      state.search = "";
      searchEl.value = "";
    }
    await renderList(resource);
    if (route.id) await openDetail(resource, route.id);
  }

  document.getElementById("drawer-close").addEventListener("click", closeDrawer);
  drawer.addEventListener("click", (event) => {
    if (event.target === drawer) closeDrawer();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !drawer.hidden) closeDrawer();
  });
  document.getElementById("menu-toggle").addEventListener("click", () => {
    sidebar.classList.toggle("open");
    overlay.hidden = !sidebar.classList.contains("open");
  });
  overlay.addEventListener("click", closeSidebar);
  let searchTimer = null;
  searchEl.addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      if (parseHash().page === "dashboard") return;
      state.search = searchEl.value.trim();
      state.page = 1;
      render();
    }, 280);
  });
  searchEl.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      clearTimeout(searchTimer);
      state.search = searchEl.value.trim();
      state.page = 1;
      render();
    }
  });
  drawerBody.addEventListener("click", (event) => {
    const button = event.target.closest("[data-add-nested]");
    if (!button) return;
    const name = button.dataset.addNested;
    const resource = resourceByKey(state.resource);
    const field = resource.fields.find((item) => item.name === name);
    const holder = document.getElementById(`nested-${name}`);
    const index = holder.children.length;
    holder.insertAdjacentHTML("beforeend", nestedRow(field, {}, index));
  });
  window.addEventListener("hashchange", render);

  api("/api/v1/schema/")
    .then((schema) => {
      state.schema = schema;
      const name = schema.user.full_name || schema.user.username;
      userChip.innerHTML = `<span class="user-avatar">${escapeHtml(initials(name))}</span>${escapeHtml(name)} · ${escapeHtml(schema.user.role)}`;
      userChip.href = "#/security";
      render();
    })
    .catch((error) => {
      viewEl.innerHTML = `<div class="empty">${escapeHtml(error.message)}</div>`;
    });
})();
