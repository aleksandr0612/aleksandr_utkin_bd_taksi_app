const API = "http://127.0.0.1:8000";

let currentUser = null;
let companiesCache = [];

/* EKRANŲ VALDYMAS */

function showScreen(name) {
    document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
    const screen = document.querySelector(`.screen[data-screen="${name}"]`);
    if (screen) screen.classList.add("active");

    document.querySelectorAll(".bottom-nav button").forEach(btn => {
        btn.classList.remove("active");
        if (btn.dataset.target === name) btn.classList.add("active");
    });
}

/* AUTO LOGIN */

async function autoLogin() {
    try {
        const formData = new FormData();
        formData.append("username", "user1@test.lt");
        formData.append("password", "password"); // pagal seed

        const res = await fetch(`${API}/auth/login`, {
            method: "POST",
            body: formData
        });

        if (!res.ok) throw new Error("Auto login failed");

        const data = await res.json();
        currentUser = data.user;

        loadCompanies();
        loadProfile();
        loadHistory();
        loadReviewsOverview();

        showScreen("companies");
    } catch (err) {
        console.error("Auto login error:", err);
        showScreen("login");
    }
}

/* ĮMONĖS */

async function loadCompanies() {
    const list = document.getElementById("company-list");
    list.innerHTML = "Kraunama...";

    const res = await fetch(`${API}/companies`);
    const companies = await res.json();
    companiesCache = companies;

    // užpildom miestų filtrą
    const citySelect = document.getElementById("filter-city");
    const allCities = new Set();
    companies.forEach(c => c.cities.forEach(city => allCities.add(city)));
    citySelect.innerHTML = `<option value="">Miestas</option>`;
    [...allCities].forEach(city => {
        citySelect.innerHTML += `<option value="${city}">${city}</option>`;
    });

    renderCompanies(companies);
}

function renderCompanies(companies) {
    const list = document.getElementById("company-list");
    list.innerHTML = "";

    if (!companies.length) {
        list.innerHTML = "<p>Nerasta įmonių pagal pasirinktus filtrus.</p>";
        return;
    }

    companies.forEach(c => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
            <h3>${c.name}</h3>
            <p>Kodas: ${c.juridinis_kodas}</p>
            <p>Miestai: ${c.cities.join(", ")}</p>
            <p>Kaina: ${c.base_price} €</p>
            <p>Butkevičiaus balas: ${c.butkevicius_score.toFixed(2)}</p>
            <p style="font-size:12px;color:#9ca3af;">Spustelk, kad pamatytum atsiliepimus ir paliktum savo.</p>
        `;
        card.onclick = () => openCompanyModal(c);
        list.appendChild(card);
    });
}

/* FILTRAI */

document.getElementById("search-btn").onclick = applyFilters;

function applyFilters() {
    const code = document.getElementById("search-code").value.trim();
    const name = document.getElementById("search-name").value.trim().toLowerCase();
    const city = document.getElementById("filter-city").value;
    const eco = document.getElementById("filter-eco").value;
    const price = document.getElementById("filter-price").value;
    const score = document.getElementById("filter-score").value;

    let filtered = [...companiesCache];

    if (code) filtered = filtered.filter(c => c.juridinis_kodas == code);
    if (name) filtered = filtered.filter(c => c.name.toLowerCase().includes(name));
    if (city) filtered = filtered.filter(c => c.cities.includes(city));
    if (eco) filtered = filtered.filter(c => String(c.is_eco) === eco);

    if (price === "low") filtered.sort((a,b)=>a.base_price - b.base_price);
    if (price === "high") filtered.sort((a,b)=>b.base_price - a.base_price);

    if (score === "high") filtered.sort((a,b)=>b.butkevicius_score - a.butkevicius_score);
    if (score === "low") filtered.sort((a,b)=>a.butkevicius_score - b.butkevicius_score);

    renderCompanies(filtered);
}

/* MODALAS: ĮMONĖ + ATSILIEPIMAI */

const modalBackdrop = document.getElementById("company-modal-backdrop");
const modalCloseBtn = document.getElementById("modal-close");
const reviewForm = document.getElementById("review-form");

let currentModalCompany = null;

function openCompanyModal(company) {
    currentModalCompany = company;

    document.getElementById("modal-company-name").innerText = company.name;
    document.getElementById("modal-company-code").innerText = company.juridinis_kodas;
    document.getElementById("modal-company-cities").innerText = company.cities.join(", ");
    document.getElementById("modal-company-price").innerText = company.base_price;
    document.getElementById("modal-company-score").innerText = company.butkevicius_score.toFixed(2);

    document.getElementById("review-comment").value = "";
    document.querySelectorAll('.stars input[name="rating"]').forEach(i => i.checked = false);

    loadCompanyReviews(company.id);

    modalBackdrop.classList.remove("hidden");
}

modalCloseBtn.onclick = () => {
    modalBackdrop.classList.add("hidden");
};

modalBackdrop.addEventListener("click", (e) => {
    if (e.target === modalBackdrop) {
        modalBackdrop.classList.add("hidden");
    }
});

async function loadCompanyReviews(companyId) {
    const container = document.getElementById("modal-reviews-list");
    container.innerHTML = "Kraunama...";

    try {
        const res = await fetch(`${API}/reviews/company/${companyId}`);
        const reviews = await res.json();

        if (!reviews.length) {
            container.innerHTML = "<p>Dar nėra atsiliepimų. Būk pirmas!</p>";
            return;
        }

        container.innerHTML = "";
        reviews.forEach(r => {
            const div = document.createElement("div");
            div.className = "review-item";
            const stars = "★".repeat(r.rating) + "☆".repeat(5 - r.rating);
            div.innerHTML = `
                <div class="stars-inline">${stars}</div>
                <div>${r.comment || "Be komentaro"}</div>
            `;
            container.appendChild(div);
        });
    } catch (err) {
        console.error(err);
        container.innerHTML = "<p>Klaida kraunant atsiliepimus.</p>";
    }
}

/* ATSILIEPIMO SIUNTIMAS */

reviewForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!currentModalCompany) return;

    const ratingInput = document.querySelector('.stars input[name="rating"]:checked');
    if (!ratingInput) {
        alert("Pasirink žvaigždučių skaičių.");
        return;
    }

    const rating = Number(ratingInput.value);
    const comment = document.getElementById("review-comment").value.trim();

    const payload = {
        company_id: currentModalCompany.id,
        rating: rating,
        comment: comment
    };

    try {
        await fetch(`${API}/reviews`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        document.getElementById("review-comment").value = "";
        document.querySelectorAll('.stars input[name="rating"]').forEach(i => i.checked = false);

        loadCompanyReviews(currentModalCompany.id);
        loadReviewsOverview();
        loadHistory();
        alert("Atsiliepimas išsaugotas!");
    } catch (err) {
        console.error(err);
        alert("Nepavyko išsaugoti atsiliepimo.");
    }
});

/* BENDRA ATSILIEPIMŲ APŽVALGA */

async function loadReviewsOverview() {
    const list = document.getElementById("reviews-list");
    if (!list) return;
    list.innerHTML = "Kraunama...";

    try {
        const res = await fetch(`${API}/ratings`);
        const data = await res.json();

        list.innerHTML = "";
        data.forEach(r => {
            const avg = (r.speed + r.transparency + r.behavior + r.condition) / 4;
            const div = document.createElement("div");
            div.className = "card";
            div.innerHTML = `
                <h3>${r.company_name}</h3>
                <p>⭐ ${avg.toFixed(1)}</p>
                <p>${r.comment || "Be komentaro"}</p>
            `;
            list.appendChild(div);
        });
    } catch (err) {
        console.error(err);
        list.innerHTML = "<p>Klaida kraunant atsiliepimus.</p>";
    }
}

/* ISTORIJA */

async function loadHistory() {
    const list = document.getElementById("history-list");
    if (!list) return;
    list.innerHTML = "Kraunama...";

    try {
        const res = await fetch(`${API}/ratings`);
        const history = await res.json();

        list.innerHTML = "";
        history.forEach(h => {
            const avg = (h.speed + h.transparency + h.behavior + h.condition) / 4;
            const card = document.createElement("div");
            card.className = "card";
            card.innerHTML = `
                <h3>${h.company_name}</h3>
                <p>⭐ ${avg.toFixed(1)}</p>
                <p>${h.comment || "Be komentaro"}</p>
            `;
            list.appendChild(card);
        });
    } catch (err) {
        console.error(err);
        list.innerHTML = "<p>Klaida kraunant istoriją.</p>";
    }
}

/* PROFILIS */

function loadProfile() {
    if (!currentUser) return;
    document.getElementById("profile-name").innerText = currentUser.name;
    document.getElementById("profile-email").innerText = currentUser.email;
}

/* NAVIGACIJA */

document.querySelectorAll(".bottom-nav button").forEach(btn => {
    btn.onclick = () => showScreen(btn.dataset.target);
});

/* LOGOUT */

document.getElementById("logout-btn").onclick = () => {
    currentUser = null;
    showScreen("login");
};

/* STARTAS */

autoLogin();
