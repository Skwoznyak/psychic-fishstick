// API Configuration
const API_BASE_URL = 'http://localhost:8000';

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

    // Enable auth buttons after successful login
    authStartBtn.disabled = false;
    authSaveBtn.disabled = false;

    // Update button text to show they're enabled
    authStartBtn.innerHTML = '<i class="fas fa-external-link-alt"></i> Открыть страницу входа';
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
    showLoading();

    try {
        const response = await apiRequest('/auth/start', {
            method: 'POST'
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

// Parsing Functions
async function handleParse(event) {
    const button = event.target;
    const card = button.closest('.parsing-card');
    const account = card.dataset.account;

    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Запуск...';

    showProgress();
    updateProgress(1, 'Запуск парсинга...', 10);

    try {
        const endpoint = account === 'elama-856489 nudnoi.ru'
            ? '/elama-856489%20nudnoi.ru'
            : `/${account}`;

        // Simulate progress steps
        setTimeout(() => updateProgress(2, 'Авторизация в системе...', 25), 1000);
        setTimeout(() => updateProgress(3, 'Поиск кнопки аккаунта...', 50), 2000);
        setTimeout(() => updateProgress(4, 'Парсинг данных...', 75), 3000);

        const response = await apiRequest(endpoint, {
            method: 'POST'
        });

        const data = await response.json();
        showStatus(parsingStatus, data.message, 'success');

        // Complete progress
        setTimeout(() => {
            updateProgress(5, 'Сохранение файла...', 90);
            setTimeout(() => completeProgress(), 1000);
        }, 4000);

    } catch (error) {
        hideProgress();
        showStatus(parsingStatus, `Ошибка парсинга: ${error.message}`, 'error');
    } finally {
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-play"></i> Запустить';
    }
}

// Download Functions
async function checkFileStatus() {
    showLoading();

    try {
        const response = await apiRequest('/status');
        const data = await response.json();

        if (data.ready_to_download) {
            downloadBtn.disabled = false;
            showStatus(downloadStatus, `Файл готов: ${data.last_file}`, 'success');
        } else {
            downloadBtn.disabled = true;
            showStatus(downloadStatus, data.message, 'info');
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
        } else {
            throw new Error('Неверный формат файла');
        }

    } catch (error) {
        showStatus(downloadStatus, `Ошибка скачивания: ${error.message}`, 'error');
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
