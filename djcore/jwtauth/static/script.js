const API_URL = "http://127.0.0.1:8000/api";  // URL вашего Django API

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API_URL}/token/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);

        const userInfo = await fetchUserInfo(data.access);
        if (userInfo) {
            redirectToRolePage(userInfo);
        }
    } else {
        alert("Ошибка входа: " + data.detail);
    }
}

async function fetchUserInfo(token) {
    const response = await fetch(`${API_URL}/me/`, {
        method: "GET",
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.ok) {
        return await response.json();
    } else {
        alert("Ошибка получения данных пользователя");
        return null;
    }
}

function redirectToRolePage(userInfo) {
    // Перенаправление в зависимости от роли
    if (userInfo.is_staff) {
        window.location.href = "/admin-content/";
    } else {
        window.location.href = "/user-content/";
    }
}

// Функции для загрузки контента остаются как есть, используя access_token в заголовке
async function getCommonContent() {
    let token = localStorage.getItem("access_token");

    const response = await fetch(`${API_URL}/common-content/`, {
        method: "GET",
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.status === 401) {
        token = await refreshAccessToken();
        if (!token) return;
        return getCommonContent();
    }

    const data = await response.json();
    document.getElementById("common-content").innerText = JSON.stringify(data, null, 2);
}

async function getRoleSpecificContent() {
    let token = localStorage.getItem("access_token");

    const response = await fetch(`${API_URL}/role-content/`, {
        method: "GET",
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.status === 401) {
        token = await refreshAccessToken();
        if (!token) return;
        return getRoleSpecificContent();
    }

    const data = await response.json();
    document.getElementById("role-content").innerText = JSON.stringify(data, null, 2);
}

async function refreshAccessToken() {
    const refresh_token = localStorage.getItem("refresh_token");

    const response = await fetch(`${API_URL}/token/refresh/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: refresh_token })
    });

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem("access_token", data.access);
        return data.access;
    } else {
        alert("Сессия истекла, войдите заново");
        logout();
        return null;
    }
}

async function logout() {
    const refresh_token = localStorage.getItem("refresh_token");

    await fetch(`${API_URL}/logout/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token })
    });

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    window.location.href = "/";
}