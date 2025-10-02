// API Configuration
const API_BASE_URL = 'https://psychic-fishstick-75uo.onrender.com';

// Global state
let authToken = localStorage.getItem('authToken');
let isAuthenticated = false;

// DOM Elements
const loginForm = document.getElementById('login-form');
const userInfo = document.getElementById('user-info');
const apiKeyInput = document.getElementById('api-key');
const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');

const authStartBtn = document.getElementById('auth-start-btn');
const authSaveBtn = document.getElementById('auth-save-btn');
const authStatus = document.getElementById('auth-status');
const phoneInput = document.getElementById('phone-input');

const parsingSection = document.getElementById('parsing-section');
const downloadSection = document.getElementById('download-section');
const parseButtons = document.querySelectorAll('.parse-btn');
const parsingStatus = document.getElementById('parsing-status');

// Progress elements
const progressSection = document.getElementById('progress-section');
const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');
const progressPercent = document.getElementById('progress-percent');
const progressSteps = document.querySelectorAll('.step');
const parsingLogs = document.getElementById('parsing-logs');

const checkStatusBtn = document.getElementById('check-status-btn');
const downloadBtn = document.getElementById('download-btn');
const downloadStatus = document.getElementById('download-status');

const loadingOverlay = document.getElementById('loading-overlay');

// Initialize app
document.addEventListener('DOMContentLoaded', function () {
    console.log('Initial token:', authToken);
    checkAuthStatus();
    setupEventListeners();
});

// Check authentication status
function checkAuthStatus() {
    if (authToken) {
        showAuthenticatedState();
        loadSections();
    } else {
        showLoginState();
        // Ensure buttons are disabled when not authenticated
        authStartBtn.disabled = true;
        authSaveBtn.disabled = true;
    }
}

// Show login state
function showLoginState() {
    loginForm.style.display = 'flex';
    userInfo.style.display = 'none';
    parsingSection.style.display = 'none';
    downloadSection.style.display = 'none';
}

// Show authenticated state
function showAuthenticatedState() {
    loginForm.style.display = 'none';
    userInfo.style.display = 'flex';
    isAuthenticated = true;

    // Enable auth buttons and phone input after successful login
    authStartBtn.disabled = false;
    authSaveBtn.disabled = false;
    phoneInput.disabled = false;

    // Update button text to show they're enabled
    authStartBtn.innerHTML = '<i class="fas fa-external-link-alt"></i> Отправить номер';
    authSaveBtn.innerHTML = '<i class="fas fa-save"></i> Сохранить куки';
}

// Load sections after authentication
function loadSections() {
    parsingSection.style.display = 'block';
    downloadSection.style.display = 'block';
}

// Setup event listeners
function setupEventListeners() {
    // Login
    loginBtn.addEventListener('click', handleLogin);
    logoutBtn.addEventListener('click', handleLogout);

    // Auth
    authStartBtn.addEventListener('click', handleAuthStart);
    authSaveBtn.addEventListener('click', handleAuthSave);

    // Parsing
    parseButtons.forEach(btn => {
        btn.addEventListener('click', handleParse);
    });

    // Download
    checkStatusBtn.addEventListener('click', checkFileStatus);
    downloadBtn.addEventListener('click', downloadFile);
}

// API Helper Functions
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;

    // Debug: log token status
    console.log('API Request:', endpoint, 'Token:', authToken ? 'Present' : 'Missing');

    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...(authToken && { 'Authorization': `Bearer ${authToken}` })
        }
    };

    const response = await fetch(url, { ...defaultOptions, ...options });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Network error' }));
        console.error('API Error:', error);
        throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response;
}

// Show loading overlay
function showLoading() {
    loadingOverlay.style.display = 'flex';
}

// Hide loading overlay
function hideLoading() {
    loadingOverlay.style.display = 'none';
}

// Show status message
function showStatus(element, message, type = 'info') {
    element.textContent = message;
    element.className = `status-message ${type}`;
    element.style.display = 'block';

    // Auto-hide after 5 seconds
    setTimeout(() => {
        element.style.display = 'none';
    }, 5000);
}

// Authentication Functions
async function handleLogin() {
    const apiKey = apiKeyInput.value.trim();

    if (!apiKey) {
        showStatus(authStatus, 'Введите API ключ', 'error');
        return;
    }

    showLoading();

    try {
        const response = await apiRequest('/login', {
            method: 'POST',
            body: JSON.stringify({ Api_key: apiKey })
        });

        const data = await response.json();
        console.log('Login response:', data);

        authToken = data.access_token;
        localStorage.setItem('authToken', authToken);

        console.log('Token saved:', authToken);

        showAuthenticatedState();
        loadSections();
        showStatus(authStatus, 'Успешная авторизация! Кнопки авторизации разблокированы.', 'success');

    } catch (error) {
        showStatus(authStatus, `Ошибка авторизации: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

function handleLogout() {
    authToken = null;
    localStorage.removeItem('authToken');
    showLoginState();
    showStatus(authStatus, 'Вы вышли из системы', 'info');
}

// Auth Functions
async function handleAuthStart() {
    const phone = phoneInput.value.trim();

    if (!phone) {
        showStatus(authStatus, 'Введите номер телефона', 'error');
        return;
    }

    showLoading();

    try {
        const response = await apiRequest('/auth/start', {
            method: 'POST',
            body: JSON.stringify({ phone: phone })
        });

        const data = await response.json();
        showStatus(authStatus, data.message, 'success');
        authSaveBtn.disabled = false;

    } catch (error) {
        showStatus(authStatus, `Ошибка: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

async function handleAuthSave() {
    showLoading();

    try {
        const response = await apiRequest('/auth/save', {
            method: 'POST'
        });

        const data = await response.json();
        showStatus(authStatus, data.message, 'success');

    } catch (error) {
        showStatus(authStatus, `Ошибка: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Progress Functions
function showProgress() {
    progressSection.style.display = 'block';
    resetProgress();
}

function hideProgress() {
    progressSection.style.display = 'none';
}

function resetProgress() {
    progressFill.style.width = '0%';
    progressPercent.textContent = '0%';
    progressText.textContent = 'Инициализация...';

    progressSteps.forEach((step, index) => {
        step.classList.remove('active', 'completed');
        if (index === 0) {
            step.classList.add('active');
        }
    });

    // Clear logs
    parsingLogs.innerHTML = '<div class="log-entry">Ожидание начала парсинга...</div>';
}

function updateProgress(step, text, percent) {
    // Update progress bar
    progressFill.style.width = `${percent}%`;
    progressPercent.textContent = `${percent}%`;
    progressText.textContent = text;

    // Update steps
    progressSteps.forEach((stepElement, index) => {
        stepElement.classList.remove('active', 'completed');

        if (index < step) {
            stepElement.classList.add('completed');
            stepElement.querySelector('i').className = 'fas fa-check-circle';
        } else if (index === step) {
            stepElement.classList.add('active');
            stepElement.querySelector('i').className = 'fas fa-spinner fa-spin';
        } else {
            stepElement.querySelector('i').className = 'fas fa-circle';
        }
    });
}

function completeProgress() {
    updateProgress(5, 'Парсинг завершен! Файл готов к скачиванию.', 100);

    // Enable download section
    downloadSection.style.display = 'block';
    checkFileStatus();

    // Stop automatic status checking
    stopStatusCheck();

    // Hide progress after 3 seconds
    setTimeout(() => {
        hideProgress();
    }, 3000);
}

// Log Functions
function addLogEntry(message, type = 'info') {
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${type}`;
    logEntry.textContent = message;
    parsingLogs.appendChild(logEntry);

    // Auto-scroll to bottom
    parsingLogs.scrollTop = parsingLogs.scrollHeight;

    // Keep only last 50 entries
    const entries = parsingLogs.querySelectorAll('.log-entry');
    if (entries.length > 50) {
        entries[0].remove();
    }
}

// Parsing Functions
async function handleParse(event) {
    const button = event.target;
    const card = button.closest('.parsing-card');
    const account = card.dataset.account;

    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Запуск...';

    showProgress();
    updateProgress(1, 'Запуск парсинга...', 10);
    addLogEntry(`🚀 Начало парсинга ${account}`, 'status');

    try {
        // Автоматически кодируем endpoint (учёт пробелов и спецсимволов)
        const safeAccount = encodeURIComponent(account);
        const endpoint = `/parsing/${safeAccount}`;

        const response = await apiRequest(endpoint, {
            method: 'POST'
        });

        const data = await response.json();
        showStatus(parsingStatus, data.message, 'success');
        addLogEntry(`✅ Парсинг запущен: ${data.message}`, 'success');

        // Start monitoring status
        startStatusMonitoring();

    } catch (error) {
        hideProgress();
        showStatus(parsingStatus, `Ошибка парсинга: ${error.message}`, 'error');
        addLogEntry(`❌ Ошибка парсинга: ${error.message}`, 'error');
    } finally {
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-play"></i> Запустить';
    }
}

// Status Monitoring
let statusMonitoringInterval;

function startStatusMonitoring() {
    if (statusMonitoringInterval) clearInterval(statusMonitoringInterval);

    statusMonitoringInterval = setInterval(async () => {
        try {
            const response = await apiRequest('/parsing/status');
            const data = await response.json();

            // Update progress based on status
            if (data.is_running) {
                updateProgressFromStatus(data.progress);
                addLogEntry(`📊 [СТАТУС] ${data.progress}`, 'info');
            } else if (data.ready_to_download) {
                completeProgress();
                addLogEntry(`✅ Парсинг завершён! Файл готов к скачиванию.`, 'success');
                stopStatusMonitoring();
            }
        } catch (error) {
            addLogEntry(`❌ Ошибка проверки статуса: ${error.message}`, 'error');
        }
    }, 2000); // Check every 2 seconds
}

function stopStatusMonitoring() {
    if (statusMonitoringInterval) {
        clearInterval(statusMonitoringInterval);
        statusMonitoringInterval = null;
    }
}

function updateProgressFromStatus(statusText) {
    // Map status text to progress steps
    if (statusText.includes('Начало парсинга')) {
        updateProgress(1, statusText, 10);
    } else if (statusText.includes('Загружаю куки') || statusText.includes('Авторизация')) {
        updateProgress(2, statusText, 25);
    } else if (statusText.includes('Получаю драйвер') || statusText.includes('Перехожу на страницу')) {
        updateProgress(2, statusText, 35);
    } else if (statusText.includes('Ищу кнопку') || statusText.includes('Кнопка найдена')) {
        updateProgress(3, statusText, 50);
    } else if (statusText.includes('Проверяю время жизни') || statusText.includes('Токен действителен')) {
        updateProgress(3, statusText, 60);
    } else if (statusText.includes('Начинаю парсинг') || statusText.includes('Парсинг данных')) {
        updateProgress(4, statusText, 75);
    } else if (statusText.includes('Сохраняю файл') || statusText.includes('Файл готов')) {
        updateProgress(5, statusText, 90);
    }
}

// Download Functions
async function checkFileStatus() {
    showLoading();

    try {
        const response = await apiRequest('/parsing/status');
        const data = await response.json();

        if (data.ready_to_download) {
            downloadBtn.disabled = false;
            showStatus(downloadStatus, `Файл готов к скачиванию`, 'success');
        } else {
            downloadBtn.disabled = true;
            showStatus(downloadStatus, data.progress || 'Парсинг в процессе...', 'info');
        }

    } catch (error) {
        showStatus(downloadStatus, `Ошибка проверки статуса: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

async function downloadFile() {
    showLoading();

    try {
        const response = await apiRequest('/download');

        if (response.headers.get('content-type')?.includes('application/vnd.openxmlformats')) {
            // Handle file download
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'export.xlsx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            showStatus(downloadStatus, 'Файл успешно скачан!', 'success');
            addLogEntry(`📁 Файл успешно скачан!`, 'success');
        } else {
            throw new Error('Неверный формат файла');
        }

    } catch (error) {
        showStatus(downloadStatus, `Ошибка скачивания: ${error.message}`, 'error');
        addLogEntry(`❌ Ошибка скачивания: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Auto-check status every 10 seconds when authenticated and progress is visible
let statusCheckInterval;

function startStatusCheck() {
    if (statusCheckInterval) clearInterval(statusCheckInterval);

    statusCheckInterval = setInterval(() => {
        if (isAuthenticated && progressSection.style.display !== 'none') {
            checkFileStatus();
        }
    }, 10000);
}

function stopStatusCheck() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
        statusCheckInterval = null;
    }
}

// Start status check when authenticated
if (authToken) {
    startStatusCheck();
}

// Keyboard shortcuts
document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
            case 'Enter':
                if (loginForm.style.display !== 'none') {
                    handleLogin();
                }
                break;
        }
    }
});

// Handle API key input
apiKeyInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        handleLogin();
    }
});

// Show welcome message
if (authToken) {
    showStatus(authStatus, 'Добро пожаловать! Вы авторизованы.', 'success');
}
