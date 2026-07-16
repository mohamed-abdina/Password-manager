/* ---------------------------------------------------------------------------
   Password Manager - Frontend Logic
   --------------------------------------------------------------------------- */

const API = "/api";
let editingName = null;

const searchInput   = document.getElementById("searchInput");
const addBtn        = document.getElementById("addBtn");
const passwordList  = document.getElementById("passwordList");
const stats         = document.getElementById("stats");
const modal         = document.getElementById("modal");
const modalTitle    = document.getElementById("modalTitle");
const modalClose    = document.getElementById("modalClose");
const passwordForm  = document.getElementById("passwordForm");
const formName      = document.getElementById("formName");
const formUsername   = document.getElementById("formUsername");
const formPassword  = document.getElementById("formPassword");
const togglePassword = document.getElementById("togglePassword");
const generateBtn   = document.getElementById("generateBtn");
const cancelBtn     = document.getElementById("cancelBtn");
const strengthEl    = document.getElementById("strengthIndicator");

document.addEventListener("DOMContentLoaded", loadPasswords);

async function api(method, path, body) {
    const opts = { method, headers: { "Content-Type": "application/json" } };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(`${API}${path}`, opts);
    const json = await res.json();
    if (!res.ok) throw new Error(json.error || "Request failed");
    return json;
}

async function loadPasswords() {
    try {
        const entries = await api("GET", "/passwords");
        render(entries);
    } catch (err) {
        passwordList.innerHTML = `<p class="empty-state">Error loading passwords: ${err.message}</p>`;
    }
}

function render(entries) {
    const query = searchInput.value.toLowerCase();
    const filtered = entries.filter(e =>
        e.name.toLowerCase().includes(query) ||
        e.username.toLowerCase().includes(query)
    );

    if (filtered.length === 0) {
        passwordList.innerHTML = `<p class="empty-state">${entries.length === 0
            ? 'No passwords saved yet. Click "+ Add Password" to get started.'
            : "No results match your search."}</p>`;
        stats.textContent = "";
        return;
    }

    passwordList.innerHTML = filtered.map(e => `
        <div class="password-card" data-name="${escapeHtml(e.name)}">
            <div class="card-icon">${escapeHtml(e.name.charAt(0))}</div>
            <div class="card-info">
                <div class="card-name">${escapeHtml(e.name)}</div>
                <div class="card-username">${escapeHtml(e.username)}</div>
            </div>
            <div class="card-info">
                <div class="card-password" data-password="${escapeAttr(e.password)}">
                    &bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;
                </div>
                <span class="strength-badge strength-${e.strength}">${e.strength}</span>
            </div>
            <div class="card-actions">
                <button class="btn-icon" title="Copy password" onclick="copyPassword(this)">&#128203;</button>
                <button class="btn-icon" title="Show/Hide" onclick="toggleCardPassword(this)">&#128065;</button>
                <button class="btn-icon" title="Edit" onclick="openEdit('${escapeAttr(e.name)}','${escapeAttr(e.username)}')">&#9998;</button>
                <button class="btn-icon btn-danger" title="Delete" onclick="deleteEntry('${escapeAttr(e.name)}')">&#128465;</button>
            </div>
        </div>
    `).join("");

    stats.textContent = `Showing ${filtered.length} of ${entries.length} entries`;
}

addBtn.addEventListener("click", () => {
    editingName = null;
    modalTitle.textContent = "Add Password";
    passwordForm.reset();
    strengthEl.textContent = "";
    formName.disabled = false;
    modal.classList.remove("hidden");
});

function openEdit(name, username) {
    editingName = name;
    modalTitle.textContent = "Edit Password";
    formName.value = name;
    formName.disabled = true;
    formUsername.value = username;
    formPassword.value = "";
    formPassword.placeholder = "Enter new password";
    strengthEl.textContent = "";
    modal.classList.remove("hidden");
}

modalClose.addEventListener("click", closeModal);
cancelBtn.addEventListener("click", closeModal);
document.querySelector(".modal-overlay").addEventListener("click", closeModal);

function closeModal() {
    modal.classList.add("hidden");
    editingName = null;
    formPassword.placeholder = "Enter password";
}

passwordForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = formName.value.trim();
    const username = formUsername.value.trim();
    const password = formPassword.value.trim();

    if (!name || !username || !password) return;

    try {
        if (editingName) {
            await api("PUT", `/passwords/${encodeURIComponent(editingName)}`, { password });
        } else {
            await api("POST", "/passwords", { name, username, password });
        }
        closeModal();
        await loadPasswords();
    } catch (err) {
        alert(err.message);
    }
});

async function deleteEntry(name) {
    if (!confirm(`Delete "${name}"?`)) return;
    try {
        await api("DELETE", `/passwords/${encodeURIComponent(name)}`);
        await loadPasswords();
    } catch (err) {
        alert(err.message);
    }
}

function toggleCardPassword(btn) {
    const card = btn.closest(".password-card");
    const el = card.querySelector(".card-password");
    const pw = el.dataset.password;
    if (el.textContent.trim() === "\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022") {
        el.textContent = pw;
    } else {
        el.textContent = "\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022";
    }
}

function copyPassword(btn) {
    const card = btn.closest(".password-card");
    const el = card.querySelector(".card-password");
    const pw = el.dataset.password;
    navigator.clipboard.writeText(pw).then(() => {
        btn.innerHTML = "&#10003;";
        setTimeout(() => { btn.innerHTML = "&#128203;"; }, 1200);
    });
}

togglePassword.addEventListener("click", () => {
    const isPassword = formPassword.type === "password";
    formPassword.type = isPassword ? "text" : "password";
    togglePassword.innerHTML = isPassword ? "&#128064;" : "&#128065;";
});

generateBtn.addEventListener("click", async () => {
    try {
        const data = await api("POST", "/generate", { length: 16 });
        formPassword.value = data.password;
        formPassword.type = "text";
        togglePassword.innerHTML = "&#128064;";
        updateStrength(data.password);
    } catch (err) {
        alert("Failed to generate password: " + err.message);
    }
});

const SYMBOLS = "!@#$%^&*()-_=+";

formPassword.addEventListener("input", () => updateStrength(formPassword.value));

function updateStrength(pw) {
    if (!pw) { strengthEl.textContent = ""; return; }
    let score = 0;
    if (pw.length >= 8) score++;
    if (/[a-z]/.test(pw)) score++;
    if (/[A-Z]/.test(pw)) score++;
    if (/\d/.test(pw)) score++;
    if (pw.split("").some(c => SYMBOLS.includes(c))) score++;

    let label, cls;
    if (score >= 5)      { label = "Strong"; cls = "strength-Strong"; }
    else if (score >= 3) { label = "Medium"; cls = "strength-Medium"; }
    else                 { label = "Weak";   cls = "strength-Weak"; }

    strengthEl.innerHTML = `<span class="strength-badge ${cls}">${label}</span>`;
}

let searchTimeout;
searchInput.addEventListener("input", () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(loadPasswords, 200);
});

function escapeHtml(str) {
    const d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
}

function escapeAttr(str) {
    return str.replace(/&/g, "&amp;").replace(/'/g, "&#39;").replace(/"/g, "&quot;");
}
