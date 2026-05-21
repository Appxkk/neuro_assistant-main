const commandsToday = document.getElementById("commandsToday");
const successCommands = document.getElementById("successCommands");
const activeTasksCount = document.getElementById("activeTasksCount");
const reportsCount = document.getElementById("reportsCount");

const totalSales = document.getElementById("totalSales");
const ordersCount = document.getElementById("ordersCount");
const averageCheck = document.getElementById("averageCheck");

const historyList = document.getElementById("historyList");
const tasksList = document.getElementById("tasksList");

const recordBtn = document.getElementById("recordBtn");
const voiceTitle = document.getElementById("voiceTitle");
const recognizedText = document.getElementById("recognizedText");
const systemStatusText = document.getElementById("systemStatusText");

const ollamaModeBtn = document.getElementById("ollamaModeBtn");
const localModeBtn = document.getElementById("localModeBtn");

const settingsOllamaModeBtn = document.getElementById("settingsOllamaModeBtn");
const settingsLocalModeBtn = document.getElementById("settingsLocalModeBtn");

const ollamaModelInput = document.getElementById("ollamaModelInput");
const saveOllamaModelBtn = document.getElementById("saveOllamaModelBtn");

const fallbackToggle = document.getElementById("fallbackToggle");
const whisperModelSelect = document.getElementById("whisperModelSelect");
const speechLanguageSelect = document.getElementById("speechLanguageSelect");

const voiceActivationModeSelect = document.getElementById("voiceActivationModeSelect");
const wakeWordInput = document.getElementById("wakeWordInput");
const wakeWordStatusDot = document.getElementById("wakeWordStatusDot");
const wakeWordStatusText = document.getElementById("wakeWordStatusText");

const siteLanguageSelect = document.getElementById("siteLanguageSelect");
const siteThemeSelect = document.getElementById("siteThemeSelect");
const detailedOutputToggle = document.getElementById("detailedOutputToggle");
const techInfoToggle = document.getElementById("techInfoToggle");

const autoRefreshToggle = document.getElementById("autoRefreshToggle");
const refreshIntervalInput = document.getElementById("refreshIntervalInput");

const saveHistoryToggle = document.getElementById("saveHistoryToggle");
const confirmActionsToggle = document.getElementById("confirmActionsToggle");

const defaultReportPeriodSelect = document.getElementById("defaultReportPeriodSelect");
const exportFormatSelect = document.getElementById("exportFormatSelect");

const currentNlpModeText = document.getElementById("currentNlpModeText");
const currentLanguageText = document.getElementById("currentLanguageText");
const currentThemeText = document.getElementById("currentThemeText");

const intentBadge = document.getElementById("intentBadge");
const sourceBadge = document.getElementById("sourceBadge");
const resultTextBlock = document.getElementById("resultTextBlock");
const paramsBlock = document.getElementById("paramsBlock");

const commandDataBlock = document.getElementById("commandDataBlock");
const commandOutputSubtitle = document.getElementById("commandOutputSubtitle");

const downloadPdfBtn = document.getElementById("downloadPdfBtn");
const buildChartBtn = document.getElementById("buildChartBtn");
const chartBox = document.getElementById("chartBox");
const clearHistoryBtn = document.getElementById("clearHistoryBtn");
const manualCreateOrderBtn = document.getElementById("manualCreateOrderBtn");
const manualCreateEmployeeBtn = document.getElementById("manualCreateEmployeeBtn");
const manualCreateSaleBtn = document.getElementById("manualCreateSaleBtn");
const manualCreateTaskBtn = document.getElementById("manualCreateTaskBtn");
const manualSendMailingBtn = document.getElementById("manualSendMailingBtn");
const manualBuildChartBtn = document.getElementById("manualBuildChartBtn");
const manualDownloadPdfBtn = document.getElementById("manualDownloadPdfBtn");
const manualClearHistoryBtn = document.getElementById("manualClearHistoryBtn");
const manualOpenHelpBtn = document.getElementById("manualOpenHelpBtn");

const confirmActionOverlay = document.getElementById("confirmActionOverlay");
const confirmActionBody = document.getElementById("confirmActionBody");
const confirmActionApplyBtn = document.getElementById("confirmActionApplyBtn");
const confirmActionCancelBtn = document.getElementById("confirmActionCancelBtn");

const pageSections = {
  dashboard: document.getElementById("pageDashboard"),
  voice: document.getElementById("pageVoice"),
  actions: document.getElementById("pageActions"),
  orders: document.getElementById("pageOrders"),
  tasks: document.getElementById("pageTasks"),
  reports: document.getElementById("pageReports"),
  history: document.getElementById("pageHistory"),
  settings: document.getElementById("pageSettings"),
};

const ordersPageContent = document.getElementById("ordersPageContent");
const tasksPageContent = document.getElementById("tasksPageContent");
const reportsPageSummary = document.getElementById("reportsPageSummary");
const reportsPageContent = document.getElementById("reportsPageContent");
const historyPageContent = document.getElementById("historyPageContent");

const helpChatToggleBtn = document.getElementById("helpChatToggleBtn");
const helpChatPanel = document.getElementById("helpChatPanel");
const helpChatCloseBtn = document.getElementById("helpChatCloseBtn");
const helpChatMessages = document.getElementById("helpChatMessages");
const helpChatInput = document.getElementById("helpChatInput");
const helpChatSendBtn = document.getElementById("helpChatSendBtn");

let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;
let autoRefreshTimer = null;
let lastCommandResultForPdf = null;

let wakeRecognition = null;
let wakeRecognitionActive = false;
let wakeCommandProcessing = false;

let pendingAction = null;
let orderManagers = [];
let actionEmployees = [];
let actionOrders = [];

const defaultUiSettings = {
  ollamaModel: "qwen2.5:1.5b",
  fallbackEnabled: true,
  whisperModel: "base",
  speechLanguage: "ru",
  voiceActivationMode: "button",
  wakeWord: "помощник",
  siteLanguage: "ru",
  theme: "light",
  detailedOutput: false,
  showTechInfo: true,
  autoRefresh: false,
  refreshInterval: 30,
  saveHistory: true,
  confirmActions: true,
  defaultReportPeriod: "month",
  fontSize: "normal",
  compactMode: false,
  animations: true,
  exportFormat: "pdf",
};

let uiSettings = { ...defaultUiSettings };

const translations = {
  ru: {
    projectSubtitle: "Дипломный проект",
    projectTitle: "Нейропомощник для автоматизации бизнес-процессов",
    navDashboard: "Главная",
    navVoice: "Голосовые команды",
    navActions: "Действия",
    navOrders: "Заказы",
    navTasks: "Задачи",
    navReports: "Отчёты",
    navHistory: "История",
    navSettings: "Настройки",
    systemStatusLabel: "Статус системы",
    onlineStatusText: "● Онлайн",
    dashboardTitle: "Панель управления",
    dashboardSubtitle: "Голосовое управление заказами, задачами и отчётами",
    headerNlpModeLabel: "Режим NLP:",
    historyButton: "История команд",
    statCommandsLabel: "Команд сегодня",
    statSuccessLabel: "Успешно обработано",
    statTasksLabel: "Активных задач",
    statReportsLabel: "Отчётов сформировано",
    voiceInputTitle: "Голосовой ввод",
    voiceInputSubtitle: "Нажмите кнопку и произнесите команду",
    microphoneStatus: "Микрофон готов",
    voiceTitleDefault: "Скажите команду",
    voiceExampleText: "Например: «Покажи продажи за март», «Найди заказ 152», «Создай задачу менеджеру Иванову»",
    recognizedTextLabel: "Распознанный текст",
    interpretationLabel: "Интерпретация команды",
    resultLabel: "Результат",
    paramsLabel: "Параметры",
    latestCommandsTitle: "Последние команды",
    executionResultTitle: "Результат выполнения",
    commandOutputSubtitle: "Здесь появятся данные после голосового запроса",
    downloadPdfBtn: "Скачать PDF",
    buildChartBtn: "Построить график",
    totalSalesLabel: "Общие продажи",
    totalSalesHint: "По данным таблицы sales",
    ordersLabel: "Заказы",
    ordersHint: "Всего заказов в системе",
    averageCheckLabel: "Средний чек",
    averageCheckHint: "Среднее значение заказа",
    activeTasksTitle: "Активные задачи",
    emptyCommandResultText: "Выполните голосовую команду, чтобы увидеть результат",
    voicePageTitle: "Голосовые команды",
    voicePageDescription: "В этом разделе представлены примеры голосовых запросов, которые может обработать нейропомощник.",
    voiceOrdersTitle: "Работа с заказами",
    voiceOrdersExample1: "«Покажи заказ 1»",
    voiceOrdersExample2: "«Найди заказ 152»",
    voiceOrdersExample3: "«Покажи заказ клиента Альфа»",
    voiceSalesTitle: "Работа с продажами",
    voiceSalesExample1: "«Покажи продажи за март»",
    voiceSalesExample2: "«Сколько продаж было за апрель»",
    voiceSalesExample3: "«Покажи выручку за месяц»",
    voiceTasksTitle: "Работа с задачами",
    voiceTasksExample1: "«Покажи активные задачи»",
    voiceTasksExample2: "«Покажи просроченные задачи»",
    voiceTasksExample3: "«Создай задачу Иванову позвонить клиенту»",
    voiceReportsTitle: "Отчёты",
    voiceReportsExample1: "«Сформируй складской отчёт»",
    voiceReportsExample2: "«Покажи остатки на складе»",
    voiceReportsExample3: "«Покажи отчёт по продажам»",
    actionsPageTitle: "Действия",
    actionsPageDescription: "Быстрый запуск операций без голосовой команды.",
    manualCreateOrderTitle: "Добавить заказ",
    manualCreateOrderDescription: "Открыть окно подтверждения для создания заказа",
    manualCreateEmployeeTitle: "Добавить сотрудника",
    manualCreateEmployeeDescription: "Создать сотрудника или менеджера через форму подтверждения",
    manualCreateSaleTitle: "Добавить продажу",
    manualCreateSaleDescription: "Выбрать заказ, товар, количество, сумму и дату продажи",
    manualCreateTaskTitle: "Создать задачу",
    manualCreateTaskDescription: "Назначить задачу сотруднику со сроком и приоритетом",
    manualSendMailingTitle: "Сделать рассылку",
    manualSendMailingDescription: "Отправить текст, картинки или файлы в Telegram",
    manualBuildChartTitle: "Построить график",
    manualBuildChartDescription: "Сформировать график продаж по данным таблицы sales",
    manualDownloadPdfTitle: "Скачать PDF",
    manualDownloadPdfDescription: "Скачать PDF по последнему результату команды",
    manualClearHistoryTitle: "Очистить историю",
    manualClearHistoryDescription: "Удалить историю команд на сайте и в базе данных",
    manualOpenHelpTitle: "Открыть справку",
    manualOpenHelpDescription: "Открыть справочный чат с подсказками по командам",
    ordersPageTitle: "Заказы",
    ordersPageDescription: "Список заказов, загруженный из таблицы orders.",
    tasksPageTitle: "Задачи",
    tasksPageDescription: "Список задач сотрудников из таблицы tasks.",
    reportsPageTitle: "Отчёты",
    reportsPageDescription: "Сводная аналитика по продажам, заказам и задачам.",
    salesSubtitle: "Продажи",
    historyPageTitle: "История команд",
    historyPageDescription: "Последние голосовые команды, обработанные системой.",
    settingsTitle: "Настройки",
    settingsDescription: "Управление режимами работы нейропомощника, интерфейсом и параметрами обработки команд.",
    nlpSettingsTitle: "Режим NLP",
    nlpSettingsDescription: "Выберите способ интерпретации голосовых команд.",
    nlpModeLabel: "Режим:",
    fallbackTitle: "Fallback-режим",
    fallbackDescription: "Если Ollama недоступна, автоматически использовать Local parser.",
    ollamaModelTitle: "Модель Ollama",
    ollamaModelDescription: "Модель, которая используется для обработки команд в режиме Ollama.",
    ollamaModelLabel: "Название модели",
    saveOllamaModelBtn: "Сохранить модель",
    whisperSettingsTitle: "Распознавание речи",
    whisperSettingsDescription: "Настройки модуля распознавания речи и голосовой активации.",
    whisperModelLabel: "Модель Whisper",
    speechLanguageLabel: "Язык распознавания",
    voiceActivationModeLabel: "Режим голосового управления",
    wakeWordLabel: "Ключевое слово",
    interfaceSettingsTitle: "Интерфейс",
    interfaceSettingsDescription: "Настройки отображения dashboard и результатов команд.",
    siteLanguageLabel: "Язык интерфейса",
    siteThemeLabel: "Тема интерфейса",
    detailedOutputTitle: "Подробный вывод",
    detailedOutputDescription: "Показывать больше полей в карточках результата.",
    techInfoTitle: "Техническая информация",
    techInfoDescription: "Показывать источник обработки, fallback и параметры.",
    dashboardSettingsTitle: "Обновление dashboard",
    dashboardSettingsDescription: "Настройки автоматического обновления главной панели.",
    autoRefreshTitle: "Автообновление",
    autoRefreshDescription: "Периодически обновлять статистику без перезагрузки страницы.",
    refreshIntervalLabel: "Интервал, секунд",
    businessSettingsTitle: "Бизнес-логика",
    businessSettingsDescription: "Параметры выполнения команд, влияющих на данные системы.",
    saveHistoryTitle: "Сохранять историю",
    saveHistoryDescription: "Записывать распознанные команды и результаты выполнения.",
    confirmActionsTitle: "Подтверждать действия",
    confirmActionsDescription: "Запрашивать подтверждение перед созданием задач и изменением данных.",
    reportsSettingsTitle: "Отчёты",
    reportsSettingsDescription: "Настройки периода и формата отчётности.",
    defaultReportPeriodLabel: "Период отчёта по умолчанию",
    exportFormatLabel: "Формат экспорта",
    systemStateTitle: "Состояние системы",
    systemStateDescription: "Текущие параметры работы приложения.",
    databaseLabel: "База данных",
    speechModuleLabel: "Распознавание речи",
    nlpModuleLabel: "NLP-модуль",
    interfaceLanguageStateLabel: "Язык интерфейса",
    interfaceThemeStateLabel: "Тема интерфейса",
    languageName: "Русский",
    lightThemeName: "Светлая",
    darkThemeName: "Тёмная",
    emptyHistory: "История команд пока пуста",
    emptyTasks: "Активных задач нет",
    loadingOrders: "Загрузка заказов...",
    emptyOrders: "Заказов нет",
    loadingTasks: "Загрузка задач...",
    emptyTasksPage: "Задач нет",
    loadingReports: "Загрузка отчётов...",
    emptySales: "Продаж нет",
    loadingHistory: "Загрузка истории...",
    emptyHistoryPage: "История пуста",
    noData: "Нет данных для отображения",
    noParams: "Параметров нет",
    wakeDisabled: "Режим ожидания выключен",
    wakeWaiting: "Ожидание ключевого слова",
    wakeUnsupported: "Режим ожидания не поддерживается этим браузером",
    wakeDenied: "Доступ к микрофону запрещён",
    wakeError: "Ошибка режима ожидания",
  },
  en: {
    projectSubtitle: "Graduation project",
    projectTitle: "AI assistant for business process automation",
    navDashboard: "Dashboard",
    navVoice: "Voice commands",
    navActions: "Actions",
    navOrders: "Orders",
    navTasks: "Tasks",
    navReports: "Reports",
    navHistory: "History",
    navSettings: "Settings",
    systemStatusLabel: "System status",
    onlineStatusText: "● Online",
    dashboardTitle: "Dashboard",
    dashboardSubtitle: "Voice control for orders, tasks, and reports",
    headerNlpModeLabel: "NLP mode:",
    historyButton: "Command history",
    statCommandsLabel: "Commands today",
    statSuccessLabel: "Successfully processed",
    statTasksLabel: "Active tasks",
    statReportsLabel: "Reports generated",
    voiceInputTitle: "Voice input",
    voiceInputSubtitle: "Press the button and say a command",
    microphoneStatus: "Microphone ready",
    voiceTitleDefault: "Say a command",
    voiceExampleText: "For example: “Show sales for March”, “Find order 152”, “Create a task for Ivanov”",
    recognizedTextLabel: "Recognized text",
    interpretationLabel: "Command interpretation",
    resultLabel: "Result",
    paramsLabel: "Parameters",
    latestCommandsTitle: "Latest commands",
    executionResultTitle: "Execution result",
    commandOutputSubtitle: "Data will appear here after a voice request",
    downloadPdfBtn: "Download PDF",
    buildChartBtn: "Build chart",
    totalSalesLabel: "Total sales",
    totalSalesHint: "Based on the sales table",
    ordersLabel: "Orders",
    ordersHint: "Total orders in the system",
    averageCheckLabel: "Average order value",
    averageCheckHint: "Average order amount",
    activeTasksTitle: "Active tasks",
    emptyCommandResultText: "Run a voice command to see the result",
    actionsPageTitle: "Actions",
    actionsPageDescription: "Quickly start operations without a voice command.",
    manualCreateOrderTitle: "Add order",
    manualCreateOrderDescription: "Open confirmation window for creating an order",
    manualCreateEmployeeTitle: "Add employee",
    manualCreateEmployeeDescription: "Create an employee or manager through confirmation form",
    manualCreateSaleTitle: "Add sale",
    manualCreateSaleDescription: "Choose order, product, quantity, amount, and sale date",
    manualCreateTaskTitle: "Create task",
    manualCreateTaskDescription: "Assign a task to an employee with deadline and priority",
    manualSendMailingTitle: "Send mailing",
    manualSendMailingDescription: "Send text, images, or files to Telegram",
    manualBuildChartTitle: "Build chart",
    manualBuildChartDescription: "Build a sales chart from the sales table",
    manualDownloadPdfTitle: "Download PDF",
    manualDownloadPdfDescription: "Download PDF for the latest command result",
    manualClearHistoryTitle: "Clear history",
    manualClearHistoryDescription: "Delete command history from the site and database",
    manualOpenHelpTitle: "Open help",
    manualOpenHelpDescription: "Open the help chat with command hints",
    languageName: "English",
    lightThemeName: "Light",
    darkThemeName: "Dark",
    emptyHistory: "Command history is empty",
    emptyTasks: "No active tasks",
    loadingOrders: "Loading orders...",
    emptyOrders: "No orders",
    loadingTasks: "Loading tasks...",
    emptyTasksPage: "No tasks",
    loadingReports: "Loading reports...",
    emptySales: "No sales",
    loadingHistory: "Loading history...",
    emptyHistoryPage: "History is empty",
    noData: "No data to display",
    noParams: "No parameters",
    wakeDisabled: "Wake word mode disabled",
    wakeWaiting: "Waiting for wake word",
    wakeUnsupported: "Wake word mode is not supported in this browser",
    wakeDenied: "Microphone access denied",
    wakeError: "Wake word recognition error",
  },
};

function getT(key) {
  const lang = uiSettings.siteLanguage || "ru";
  return translations[lang]?.[key] || translations.ru[key] || key;
}

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = value;
}

function applyLocalization() {
  const lang = uiSettings.siteLanguage || "ru";
  const dictionary = translations[lang] || translations.ru;

  Object.entries(dictionary).forEach(([id, value]) => {
    if (
      id !== "languageName" &&
      id !== "lightThemeName" &&
      id !== "darkThemeName" &&
      !id.startsWith("empty") &&
      !id.startsWith("loading") &&
      !id.startsWith("wake") &&
      id !== "noData" &&
      id !== "noParams"
    ) {
      setText(id, value);
    }
  });

  if (currentLanguageText) currentLanguageText.textContent = getT("languageName");

  if (currentThemeText) {
    currentThemeText.textContent =
      uiSettings.theme === "dark" ? getT("darkThemeName") : getT("lightThemeName");
  }

  if (voiceTitle && !isRecording) voiceTitle.textContent = getT("voiceTitleDefault");

  updateWakeWordStatus(
    uiSettings.voiceActivationMode === "wake_word" && wakeRecognitionActive ? "active" : "inactive",
    uiSettings.voiceActivationMode === "wake_word" && wakeRecognitionActive
      ? `${getT("wakeWaiting")}: ${uiSettings.wakeWord}`
      : getT("wakeDisabled")
  );
}

function applyTheme() {
  if (uiSettings.theme === "dark") {
    document.body.classList.add("dark-theme");
  } else {
    document.body.classList.remove("dark-theme");
  }

  if (currentThemeText) {
    currentThemeText.textContent =
      uiSettings.theme === "dark" ? getT("darkThemeName") : getT("lightThemeName");
  }
}

function applyVisualSettings() {
  document.body.classList.remove("font-small", "font-normal", "font-large");
  document.body.classList.remove("compact-mode", "no-animations");

  const fontSize = uiSettings.fontSize || "normal";

  if (["small", "normal", "large"].includes(fontSize)) {
    document.body.classList.add(`font-${fontSize}`);
  } else {
    document.body.classList.add("font-normal");
  }

  if (uiSettings.compactMode) document.body.classList.add("compact-mode");
  if (!uiSettings.animations) document.body.classList.add("no-animations");
}

function loadUiSettings() {
  const savedSettings = localStorage.getItem("neuroAssistantSettings");

  if (savedSettings) {
    try {
      uiSettings = {
        ...defaultUiSettings,
        ...JSON.parse(savedSettings),
      };
    } catch (error) {
      console.error("Ошибка чтения настроек интерфейса", error);
      uiSettings = { ...defaultUiSettings };
    }
  }

  applyUiSettingsToForm();
  applyLocalization();
  applyTheme();
  applyVisualSettings();
  applyAutoRefresh();
  applyVoiceActivationMode();
}

function saveUiSettings() {
  localStorage.setItem("neuroAssistantSettings", JSON.stringify(uiSettings));
}

function applyUiSettingsToForm() {
  if (ollamaModelInput) ollamaModelInput.value = uiSettings.ollamaModel;
  if (fallbackToggle) fallbackToggle.checked = uiSettings.fallbackEnabled;
  if (whisperModelSelect) whisperModelSelect.value = uiSettings.whisperModel;
  if (speechLanguageSelect) speechLanguageSelect.value = uiSettings.speechLanguage;
  if (voiceActivationModeSelect) voiceActivationModeSelect.value = uiSettings.voiceActivationMode;
  if (wakeWordInput) wakeWordInput.value = uiSettings.wakeWord;
  if (siteLanguageSelect) siteLanguageSelect.value = uiSettings.siteLanguage;
  if (siteThemeSelect) siteThemeSelect.value = uiSettings.theme;
  if (detailedOutputToggle) detailedOutputToggle.checked = uiSettings.detailedOutput;
  if (techInfoToggle) techInfoToggle.checked = uiSettings.showTechInfo;
  if (autoRefreshToggle) autoRefreshToggle.checked = uiSettings.autoRefresh;
  if (refreshIntervalInput) refreshIntervalInput.value = uiSettings.refreshInterval;
  if (saveHistoryToggle) saveHistoryToggle.checked = uiSettings.saveHistory;
  if (confirmActionsToggle) confirmActionsToggle.checked = uiSettings.confirmActions;
  if (defaultReportPeriodSelect) defaultReportPeriodSelect.value = uiSettings.defaultReportPeriod;
  if (exportFormatSelect) exportFormatSelect.value = uiSettings.exportFormat;
}

function applyAutoRefresh() {
  if (autoRefreshTimer) {
    clearInterval(autoRefreshTimer);
    autoRefreshTimer = null;
  }

  if (uiSettings.autoRefresh) {
    const intervalMs = Math.max(Number(uiSettings.refreshInterval || 30), 5) * 1000;
    autoRefreshTimer = setInterval(() => {
      loadDashboard();
    }, intervalMs);
  }
}

function formatCurrency(value) {
  const number = Number(value || 0);

  return new Intl.NumberFormat("ru-RU", {
    style: "currency",
    currency: "RUB",
    maximumFractionDigits: 0,
  }).format(number);
}

function formatDateTime(value) {
  if (!value) return "—";

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "—";

  return date.toLocaleString("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function escapeHtml(value) {
  if (value === null || value === undefined) return "";

  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatValue(value) {
  if (value === null || value === undefined || value === "") return "—";
  if (typeof value === "number") return String(value);
  return escapeHtml(value);
}

function normalizeVoiceText(text) {
  return String(text || "").toLowerCase().trim().replaceAll("ё", "е");
}

function cleanVoiceValue(value) {
  return String(value || "")
    .replace(/[«»"]/g, "")
    .replace(/[.,!?;:]$/g, "")
    .trim();
}

function toDisplayCase(value) {
  const text = cleanVoiceValue(value);

  if (!text) return "";

  return text
    .split(" ")
    .filter(Boolean)
    .map((word) => {
      const upper = word.toUpperCase();

      // Сохраняем аббревиатуры: ООО, ИП, CRM, PDF
      if (word.length <= 4 && word === upper) {
        return word;
      }

      return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
    })
    .join(" ");
}

function capitalizeFirst(value) {
  const text = cleanVoiceValue(value);
  if (!text) return "";

  return text.charAt(0).toUpperCase() + text.slice(1);
}

function extractTextAfterKeyword(text, keywords, stopWords = []) {
  const original = String(text || "").trim();

  for (const keyword of keywords) {
    const regex = new RegExp(`${keyword}\\s+(.+)$`, "i");
    const match = original.match(regex);

    if (match && match[1]) {
      let value = match[1].trim();

      for (const stopWord of stopWords) {
        const stopRegex = new RegExp(`\\s+${stopWord}\\b.*$`, "i");
        value = value.replace(stopRegex, "").trim();
      }

      return cleanVoiceValue(value);
    }
  }

  return "";
}

function extractNumberFromText(text) {
  const rawText = String(text || "");
  const normalized = normalizeVoiceText(rawText);

  const digitMatch = rawText.match(/[0-9][0-9\s.,]*/);

  if (digitMatch) {
    const digits = digitMatch[0].replace(/\D/g, "");

    if (digits) {
      return Number(digits);
    }
  }

  const numberWords = {
    "один": 1,
    "одна": 1,
    "одно": 1,
    "два": 2,
    "две": 2,
    "три": 3,
    "четыре": 4,
    "пять": 5,
    "шесть": 6,
    "семь": 7,
    "восемь": 8,
    "девять": 9,
    "десять": 10,
    "одиннадцать": 11,
    "двенадцать": 12,
    "тринадцать": 13,
    "четырнадцать": 14,
    "пятнадцать": 15,
    "шестнадцать": 16,
    "семнадцать": 17,
    "восемнадцать": 18,
    "девятнадцать": 19,
    "двадцать": 20,
    "тридцать": 30,
    "сорок": 40,
    "пятьдесят": 50,
    "сто": 100,
  };

  for (const [word, number] of Object.entries(numberWords)) {
    if (normalized.includes(word)) {
      return number;
    }
  }

  return null;
}

function parseVoiceDate(text) {
  const normalized = normalizeVoiceText(text);
  const now = new Date();

  if (normalized.includes("послезавтра")) {
    const date = new Date(now);
    date.setDate(date.getDate() + 2);
    return date.toISOString().slice(0, 10);
  }

  if (normalized.includes("завтра")) {
    const date = new Date(now);
    date.setDate(date.getDate() + 1);
    return date.toISOString().slice(0, 10);
  }

  if (normalized.includes("сегодня")) {
    return now.toISOString().slice(0, 10);
  }

  const isoMatch = normalized.match(/\d{4}-\d{2}-\d{2}/);

  if (isoMatch) {
    return isoMatch[0];
  }

  const ruDateMatch = normalized.match(/(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})/);

  if (ruDateMatch) {
    const day = ruDateMatch[1].padStart(2, "0");
    const month = ruDateMatch[2].padStart(2, "0");
    const year = ruDateMatch[3];

    return `${year}-${month}-${day}`;
  }

  return null;
}

function setInputValue(id, value) {
  const input = document.getElementById(id);

  if (input) {
    input.value = value;
    input.dispatchEvent(new Event("input", { bubbles: true }));
    input.dispatchEvent(new Event("change", { bubbles: true }));
    return true;
  }

  console.warn(`Поле ${id} не найдено`);
  return false;
}

function setSelectValue(id, value) {
  const select = document.getElementById(id);

  if (select) {
    select.value = String(value);
    select.dispatchEvent(new Event("change", { bubbles: true }));
    return true;
  }

  console.warn(`Список ${id} не найден`);
  return false;
}

function setVoiceFieldResult(message) {
  if (resultTextBlock) resultTextBlock.textContent = message;
  if (commandOutputSubtitle) commandOutputSubtitle.textContent = message;
}

function parseOrderStatus(text) {
  const normalized = normalizeVoiceText(text);

  if (normalized.includes("нов")) return "Новый";
  if (normalized.includes("обработ")) return "В обработке";
  if (normalized.includes("заверш")) return "Завершён";
  if (normalized.includes("отмен")) return "Отменён";

  return null;
}

function parseTaskStatus(text) {
  const normalized = normalizeVoiceText(text);

  if (normalized.includes("актив")) return "Активная";
  if (normalized.includes("просроч")) return "Просрочена";
  if (normalized.includes("заверш")) return "Завершена";

  return null;
}

function parsePriority(text) {
  const normalized = normalizeVoiceText(text);

  if (normalized.includes("высок")) return "Высокий";
  if (normalized.includes("сред")) return "Средний";
  if (normalized.includes("низк")) return "Низкий";

  return null;
}

function renderParams(parameters) {
  if (!parameters || Object.keys(parameters).length === 0) {
    paramsBlock.innerHTML = `<span class="empty-data">${getT("noParams")}</span>`;
    return;
  }

  const usefulParameters = Object.entries(parameters).filter(([_, value]) => {
    return value !== null && value !== undefined && value !== "";
  });

  if (usefulParameters.length === 0) {
    paramsBlock.innerHTML = `<span class="empty-data">${getT("noParams")}</span>`;
    return;
  }

  paramsBlock.innerHTML = usefulParameters
    .map(([key, value]) => {
      let visibleValue = value;

      if (typeof value === "object") {
        visibleValue = JSON.stringify(value, null, 0);
      }

      return `
        <span class="param-chip">
          <strong>${escapeHtml(key)}:</strong> ${formatValue(visibleValue)}
        </span>
      `;
    })
    .join("");
}

function getCardTitle(item, intent) {
  if (intent === "show_sales" || intent === "create_sale") return item.product_name || "Sale";

  if (intent === "find_order" || intent === "create_order") {
    return uiSettings.siteLanguage === "en"
      ? `Order #${item.id || "—"}`
      : `Заказ №${item.id || "—"}`;
  }

  if (
    intent === "show_active_tasks" ||
    intent === "show_overdue_tasks" ||
    intent === "create_task"
  ) {
    return item.title || (uiSettings.siteLanguage === "en" ? "Task" : "Задача");
  }

  if (intent === "create_employee") {
    return item.full_name || "Сотрудник";
  }

  if (intent === "warehouse_report") {
    return item.product_name || (uiSettings.siteLanguage === "en" ? "Product" : "Товар");
  }

  return item.title || item.product_name || item.customer_name || item.full_name || `ID ${item.id || ""}`;
}

function getPrettyRows(item, intent) {
  const labels =
    uiSettings.siteLanguage === "en"
      ? {
          quantity: "Quantity",
          amount: "Amount",
          date: "Date",
          client: "Client",
          status: "Status",
          priority: "Priority",
          employee: "Employee ID",
          deadline: "Deadline",
          saleId: "Sale ID",
          orderId: "Order ID",
          managerId: "Manager ID",
          taskId: "Task ID",
          description: "Description",
          sold: "Sold",
          name: "Name",
          position: "Position",
          department: "Department",
        }
      : {
          quantity: "Количество",
          amount: "Сумма",
          date: "Дата",
          client: "Клиент",
          status: "Статус",
          priority: "Приоритет",
          employee: "Исполнитель ID",
          deadline: "Срок",
          saleId: "ID продажи",
          orderId: "ID заказа",
          managerId: "Менеджер ID",
          taskId: "ID задачи",
          description: "Описание",
          sold: "Продано",
          name: "ФИО",
          position: "Должность",
          department: "Отдел",
        };

  if (intent === "show_sales" || intent === "create_sale") {
    return [
      [labels.quantity, item.quantity],
      [labels.amount, formatCurrency(item.total_price)],
      [labels.date, item.sale_date],
      [labels.orderId, item.order_id],
    ];
  }

  if (intent === "find_order" || intent === "create_order") {
    return [
      [labels.client, item.customer_name],
      [labels.amount, formatCurrency(item.amount)],
      [labels.status, item.status],
      [labels.managerId, item.manager_id],
      [labels.date, formatDateTime(item.created_at)],
    ];
  }

  if (
    intent === "show_active_tasks" ||
    intent === "show_overdue_tasks" ||
    intent === "create_task"
  ) {
    return [
      [labels.status, item.status],
      [labels.priority, item.priority],
      [labels.employee, item.employee_id],
      [labels.deadline, formatDateTime(item.deadline)],
      [labels.description, item.description],
    ];
  }

  if (intent === "create_employee") {
    return [
      [labels.name, item.full_name],
      [labels.position, item.position],
      [labels.department, item.department],
      [labels.date, formatDateTime(item.created_at)],
    ];
  }

  if (intent === "warehouse_report") {
    return [[labels.sold, item.sold_quantity]];
  }

  return Object.entries(item)
    .slice(0, uiSettings.detailedOutput ? 8 : 4)
    .map(([key, value]) => [key, value]);
}

function renderCommandData(data, intent) {
  if (!data || !Array.isArray(data) || data.length === 0) {
    commandDataBlock.innerHTML = `
      <div class="empty-command-result">
        ${getT("noData")}
      </div>
    `;
    return;
  }

  commandDataBlock.innerHTML = "";

  data.forEach((item) => {
    const card = document.createElement("div");
    card.className = "command-data-card";

    const title = getCardTitle(item, intent);
    const rows = getPrettyRows(item, intent);

    card.innerHTML = `
      <div class="command-data-card-title">${escapeHtml(title)}</div>
      ${rows
        .map(
          ([key, value]) => `
        <div class="command-data-row">
          <span class="command-data-key">${escapeHtml(key)}</span>
          <span class="command-data-value">${formatValue(value)}</span>
        </div>
      `
        )
        .join("")}
    `;

    commandDataBlock.appendChild(card);
  });
}

function renderHistory(history) {
  historyList.innerHTML = "";

  if (!history || history.length === 0) {
    historyList.innerHTML = `<p class="empty-text">${getT("emptyHistory")}</p>`;
    return;
  }

  history.forEach((item) => {
    const element = document.createElement("div");
    element.className = "history-item";

    element.innerHTML = `
      <div class="history-top">
        <span class="history-time">${formatDateTime(item.created_at)}</span>
        <span class="status-badge">${item.status || "Выполнено"}</span>
      </div>
      <p class="history-text">${escapeHtml(item.text || item.recognized_text || "—")}</p>
    `;

    historyList.appendChild(element);
  });
}

function renderTasks(tasks) {
  tasksList.innerHTML = "";

  if (!tasks || tasks.length === 0) {
    tasksList.innerHTML = `<p class="empty-text">${getT("emptyTasks")}</p>`;
    return;
  }

  tasks.forEach((task) => {
    const isHigh = task.priority === "Высокий";

    const element = document.createElement("div");
    element.className = "task-item";

    element.innerHTML = `
      <div class="task-top">
        <p class="task-title">${escapeHtml(task.title || "—")}</p>
        <span class="status-badge ${isHigh ? "priority-high" : "priority-medium"}">
          ${escapeHtml(task.priority || "—")}
        </span>
      </div>
      <p class="task-meta">${uiSettings.siteLanguage === "en" ? "Employee ID" : "Исполнитель ID"}: ${escapeHtml(task.employee_id || "—")}</p>
      <p class="task-meta">${uiSettings.siteLanguage === "en" ? "Deadline" : "Срок"}: ${formatDateTime(task.deadline)}</p>
    `;

    tasksList.appendChild(element);
  });
}

function updateModeButtons(mode) {
  ollamaModeBtn?.classList.remove("active");
  localModeBtn?.classList.remove("active");
  localModeBtn?.classList.remove("reserve-active");

  settingsOllamaModeBtn?.classList.remove("active");
  settingsLocalModeBtn?.classList.remove("active");
  settingsLocalModeBtn?.classList.remove("reserve-active");

  if (mode === "ollama") {
    ollamaModeBtn?.classList.add("active");
    settingsOllamaModeBtn?.classList.add("active");
    if (systemStatusText) {
      systemStatusText.textContent =
        uiSettings.siteLanguage === "en" ? "NLP mode: Ollama" : "Режим NLP: Ollama";
    }
  } else {
    localModeBtn?.classList.add("reserve-active");
    settingsLocalModeBtn?.classList.add("reserve-active");
    if (systemStatusText) {
      systemStatusText.textContent =
        uiSettings.siteLanguage === "en" ? "NLP mode: Local parser" : "Режим NLP: Local parser";
    }
  }

  if (currentNlpModeText) {
    currentNlpModeText.textContent = mode === "ollama" ? "Ollama / Qwen" : "Local parser";
  }
}

async function loadLLMMode() {
  try {
    const response = await fetch("/api/settings/llm-mode");
    if (!response.ok) throw new Error("Ошибка загрузки режима NLP");

    const data = await response.json();
    updateModeButtons(data.mode);
  } catch (error) {
    console.error("Не удалось загрузить режим NLP", error);
  }
}

async function setLLMMode(mode) {
  try {
    const response = await fetch("/api/settings/llm-mode", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ mode }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Ошибка переключения режима");
    }

    updateModeButtons(data.mode);
  } catch (error) {
    console.error(error);
    alert(uiSettings.siteLanguage === "en" ? "Failed to switch NLP mode" : "Не удалось переключить режим NLP");
  }
}

function openPageByVoice(pageName) {
  const pages = {
    dashboard: "pageDashboard",
    voice: "pageVoice",
    actions: "pageActions",
    orders: "pageOrders",
    tasks: "pageTasks",
    reports: "pageReports",
    history: "pageHistory",
    settings: "pageSettings",
  };

  const pageId = pages[pageName];

  if (!pageId) {
    console.warn("Неизвестная страница:", pageName);
    return;
  }

  document.querySelectorAll(".page-section").forEach((section) => {
    section.classList.remove("active-page");
  });

  const targetPage = document.getElementById(pageId);
  if (targetPage) targetPage.classList.add("active-page");

  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.remove("active");
    if (item.dataset.page === pageName) {
      item.classList.add("active");
    }
  });

  if (pageName === "dashboard") loadDashboard();
  if (pageName === "orders") loadOrdersPage();
  if (pageName === "tasks") loadTasksPage();
  if (pageName === "reports") loadReportsPage();
  if (pageName === "history") loadHistoryPage();
  if (pageName === "settings") loadLLMMode();
}

function showPage(pageName) {
  openPageByVoice(pageName);
}

function openManualConfirmAction(recognizedText, action, payload, resultText) {
  showConfirmActionModal({
    recognized_text: recognizedText,
    intent: "confirm_action",
    parameters: {
      action,
      payload,
    },
    source: "manual_action",
    fallback: false,
    fallback_reason: null,
    result_text: resultText,
    data: [],
  });
}

function openManualCreateOrder() {
  openManualConfirmAction(
    "Ручной выбор: добавить заказ",
    "create_order",
    {
      customer_name: "",
      amount: "",
      status: "Новый",
    },
    "Требуется подтверждение добавления заказа"
  );
}

function openManualCreateEmployee() {
  openManualConfirmAction(
    "Ручной выбор: добавить сотрудника",
    "create_employee",
    {
      full_name: "",
      position: "Менеджер",
      department: "Продажи",
    },
    "Требуется подтверждение добавления сотрудника"
  );
}

function openManualCreateSale() {
  openManualConfirmAction(
    "Ручной выбор: добавить продажу",
    "create_sale",
    {
      order_id: null,
      product_name: "",
      quantity: 1,
      total_price: "",
      sale_date: new Date().toISOString().slice(0, 10),
    },
    "Требуется подтверждение добавления продажи"
  );
}

function openManualCreateTask() {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);

  openManualConfirmAction(
    "Ручной выбор: создать задачу",
    "create_task",
    {
      title: "",
      description: "",
      employee_id: null,
      status: "Активная",
      priority: "Средний",
      deadline: `${tomorrow.toISOString().slice(0, 10)}T23:59:00`,
    },
    "Требуется подтверждение создания задачи"
  );
}

function openManualSendMailing() {
  openManualConfirmAction(
    "Ручной выбор: сделать рассылку",
    "send_mailing",
    {
      channels: [],
      target: "employees",
      message: "",
    },
    "Требуется подтверждение отправки рассылки"
  );
}

function createDataCard(title, rows) {
  return `
    <div class="page-data-card">
      <h4>${escapeHtml(title)}</h4>
      ${rows
        .map(
          ([key, value]) => `
        <div class="page-data-row">
          <span class="page-data-key">${escapeHtml(key)}</span>
          <span class="page-data-value">${formatValue(value)}</span>
        </div>
      `
        )
        .join("")}
    </div>
  `;
}

async function loadOrdersPage() {
  ordersPageContent.innerHTML = `<p class="empty-text">${getT("loadingOrders")}</p>`;

  const response = await fetch("/api/pages/orders");
  const data = await response.json();

  if (!data.orders || data.orders.length === 0) {
    ordersPageContent.innerHTML = `<p class="empty-text">${getT("emptyOrders")}</p>`;
    return;
  }

  ordersPageContent.innerHTML = data.orders
    .map((order) => {
      return createDataCard(uiSettings.siteLanguage === "en" ? `Order #${order.id}` : `Заказ №${order.id}`, [
        [uiSettings.siteLanguage === "en" ? "Client" : "Клиент", order.customer_name],
        [uiSettings.siteLanguage === "en" ? "Amount" : "Сумма", formatCurrency(order.amount)],
        [uiSettings.siteLanguage === "en" ? "Status" : "Статус", order.status],
        [uiSettings.siteLanguage === "en" ? "Manager ID" : "Менеджер ID", order.manager_id],
        [uiSettings.siteLanguage === "en" ? "Date" : "Дата", formatDateTime(order.created_at)],
      ]);
    })
    .join("");
}

async function loadTasksPage() {
  tasksPageContent.innerHTML = `<p class="empty-text">${getT("loadingTasks")}</p>`;

  const response = await fetch("/api/pages/tasks");
  const data = await response.json();

  if (!data.tasks || data.tasks.length === 0) {
    tasksPageContent.innerHTML = `<p class="empty-text">${getT("emptyTasksPage")}</p>`;
    return;
  }

  tasksPageContent.innerHTML = data.tasks
    .map((task) => {
      return createDataCard(task.title || (uiSettings.siteLanguage === "en" ? "Task" : "Задача"), [
        [uiSettings.siteLanguage === "en" ? "Status" : "Статус", task.status],
        [uiSettings.siteLanguage === "en" ? "Priority" : "Приоритет", task.priority],
        [uiSettings.siteLanguage === "en" ? "Employee ID" : "Исполнитель ID", task.employee_id],
        [uiSettings.siteLanguage === "en" ? "Deadline" : "Срок", formatDateTime(task.deadline)],
      ]);
    })
    .join("");
}

async function loadReportsPage() {
  reportsPageContent.innerHTML = `<p class="empty-text">${getT("loadingReports")}</p>`;
  reportsPageSummary.innerHTML = "";

  const response = await fetch("/api/pages/reports");
  const data = await response.json();

  const summary = data.summary || {};

  reportsPageSummary.innerHTML = `
    <div class="stat-card">
      <p>${uiSettings.siteLanguage === "en" ? "Total sales" : "Общие продажи"}</p>
      <h3>${formatCurrency(summary.total_sales || 0)}</h3>
    </div>

    <div class="stat-card">
      <p>${uiSettings.siteLanguage === "en" ? "Products sold" : "Продано товаров"}</p>
      <h3>${summary.total_quantity || 0}</h3>
    </div>

    <div class="stat-card">
      <p>${uiSettings.siteLanguage === "en" ? "Average sale" : "Средняя продажа"}</p>
      <h3>${formatCurrency(summary.average_sale || 0)}</h3>
    </div>

    <div class="stat-card">
      <p>${uiSettings.siteLanguage === "en" ? "Orders count" : "Количество заказов"}</p>
      <h3>${summary.orders_count || 0}</h3>
    </div>
  `;

  if (!data.sales || data.sales.length === 0) {
    reportsPageContent.innerHTML = `<p class="empty-text">${getT("emptySales")}</p>`;
    return;
  }

  reportsPageContent.innerHTML = data.sales
    .map((sale) => {
      return createDataCard(sale.product_name || (uiSettings.siteLanguage === "en" ? "Sale" : "Продажа"), [
        [uiSettings.siteLanguage === "en" ? "Quantity" : "Количество", sale.quantity],
        [uiSettings.siteLanguage === "en" ? "Amount" : "Сумма", formatCurrency(sale.total_price)],
        [uiSettings.siteLanguage === "en" ? "Date" : "Дата", sale.sale_date],
        [uiSettings.siteLanguage === "en" ? "Order ID" : "Заказ ID", sale.order_id],
      ]);
    })
    .join("");
}

async function loadHistoryPage() {
  historyPageContent.innerHTML = `<p class="empty-text">${getT("loadingHistory")}</p>`;

  const response = await fetch("/api/pages/history");
  const data = await response.json();

  if (!data.history || data.history.length === 0) {
    historyPageContent.innerHTML = `<p class="empty-text">${getT("emptyHistoryPage")}</p>`;
    return;
  }

  historyPageContent.innerHTML = data.history
    .map((item) => {
      return `
      <div class="page-list-item">
        <div class="page-list-top">
          <span class="page-list-time">${formatDateTime(item.created_at)}</span>
          <span class="page-list-status">${escapeHtml(item.status || "Выполнено")}</span>
        </div>

        <strong>${escapeHtml(item.recognized_text || "—")}</strong>

        <p class="empty-text">${uiSettings.siteLanguage === "en" ? "Intent" : "Интент"}: ${escapeHtml(item.intent || "—")}</p>
        <p>${escapeHtml(item.result_text || "")}</p>
      </div>
    `;
    })
    .join("");
}

async function clearCommandHistory(options = {}) {
  const shouldAskConfirmation = options.askConfirmation !== false;

  if (shouldAskConfirmation) {
    const confirmed = confirm(
      uiSettings.siteLanguage === "en"
        ? "Clear the entire command history?"
        : "Очистить всю историю команд?"
    );

    if (!confirmed) return;
  }

  try {
    const response = await fetch("/api/history/clear", {
      method: "DELETE",
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Ошибка очистки истории");
    }

    if (historyList) {
      historyList.innerHTML = `<p class="empty-text">${getT("emptyHistory")}</p>`;
    }

    if (historyPageContent) {
      historyPageContent.innerHTML = `<p class="empty-text">${getT("emptyHistoryPage")}</p>`;
    }

    await loadDashboard();

    if (pageSections.history?.classList.contains("active-page")) {
      await loadHistoryPage();
    }

    resultTextBlock.textContent = data.result_text || "История команд очищена";
    commandOutputSubtitle.textContent = "Список последних команд очищен";

    lastCommandResultForPdf = {
      recognized_text: "Очистить историю команд",
      intent: "clear_history",
      parameters: {},
      source: "system",
      fallback: false,
      fallback_reason: null,
      result_text: data.result_text || "История команд очищена",
      data: [],
    };
  } catch (error) {
    console.error(error);

    alert(
      uiSettings.siteLanguage === "en"
        ? `Failed to clear history: ${error.message}`
        : `Не удалось очистить историю: ${error.message}`
    );
  }
}

async function buildSalesChart() {
  if (!chartBox) return;

  try {
    chartBox.innerHTML = `
      <div class="empty-command-result">
        Загружаю данные для графика...
      </div>
    `;

    if (commandDataBlock) {
      commandDataBlock.innerHTML = `
        <div class="empty-command-result">
          Данные графика загружаются...
        </div>
      `;
    }

    const response = await fetch("/api/pages/reports");

    if (!response.ok) {
      throw new Error("Ошибка загрузки данных отчёта");
    }

    const data = await response.json();
    const sales = data.sales || [];

    if (!sales.length) {
      chartBox.innerHTML = `
        <div class="empty-command-result">
          Нет данных для построения графика
        </div>
      `;
      if (commandDataBlock) {
        commandDataBlock.innerHTML = `
          <div class="empty-command-result">
            Нет данных продаж для отображения
          </div>
        `;
      }
      return;
    }

    const maxValue = Math.max(...sales.map(item => Number(item.total_price || 0)));

    chartBox.innerHTML = "";
    chartBox.className = "chart-box sales-chart";

    sales.forEach((sale) => {
      const value = Number(sale.total_price || 0);
      const percent = maxValue > 0 ? value / maxValue : 0;
      const barHeight = Math.max(70, Math.round(percent * 200));

      const item = document.createElement("div");
      item.className = "chart-item";

      item.innerHTML = `
        <div class="chart-value">${formatCurrency(value)}</div>

        <div class="chart-bar-wrap">
          <div class="chart-bar" style="height: ${barHeight}px;"></div>
        </div>

        <div class="chart-label">
          ${escapeHtml(sale.product_name || "Товар")}
        </div>
      `;

      chartBox.appendChild(item);
    });

    resultTextBlock.textContent = "График продаж построен";
    commandOutputSubtitle.textContent = "Визуализация по данным таблицы sales";

    if (commandDataBlock) {
      commandDataBlock.innerHTML = `
        <div class="empty-command-result">
          График построен по ${sales.length} записям продаж. Подробные данные отображены на диаграмме выше.
        </div>
      `;
    }

    lastCommandResultForPdf = {
      recognized_text: "Построить график продаж",
      intent: "build_chart",
      parameters: {},
      source: "manual_action",
      fallback: false,
      fallback_reason: null,
      result_text: "График продаж построен",
      data: sales,
    };
  } catch (error) {
    console.error(error);

    chartBox.innerHTML = `
      <div class="empty-command-result">
        Не удалось построить график
      </div>
    `;

    resultTextBlock.textContent = `Ошибка построения графика: ${error.message}`;
    commandOutputSubtitle.textContent = "Проверьте endpoint /api/pages/reports";

    if (commandDataBlock) {
      commandDataBlock.innerHTML = `
        <div class="empty-command-result">
          Не удалось загрузить данные графика
        </div>
      `;
    }
  }
}

function executeVoiceUiCommand(data) {
  if (!data || !data.intent) return;

  const parameters = data.parameters || {};
    if (data.intent === "open_help") {
    openHelpChat();
    return;
  }

  if (data.intent === "help_question") {
    const question = parameters.question || data.recognized_text || "";
    sendHelpQuestion(question);
    return;
  }

  if (data.intent === "clear_history") {
    clearCommandHistory({ askConfirmation: false });
    return;
  }

  if (data.intent === "download_pdf") {
    downloadLastCommandPdf();
    return;
  }

  if (data.intent === "build_chart") {
    buildSalesChart();
    return;
  }

  if (data.intent === "open_page") {
    openPageByVoice(parameters.page);
    return;
  }

  if (data.intent === "change_theme") {
    const theme = parameters.theme;
    if (theme === "dark" || theme === "light") {
      uiSettings.theme = theme;
      saveUiSettings();
      applyUiSettingsToForm();
      applyTheme();
    }
    return;
  }

  if (data.intent === "change_language") {
    const language = parameters.language;
    if (language === "ru" || language === "en") {
      uiSettings.siteLanguage = language;
      saveUiSettings();
      applyUiSettingsToForm();
      applyLocalization();
      loadDashboard();
    }
    return;
  }

  if (data.intent === "change_setting") {
    const setting = parameters.setting;
    const value = parameters.value;

    if (setting && Object.prototype.hasOwnProperty.call(uiSettings, setting)) {
      uiSettings[setting] = value;
      saveUiSettings();
      applyUiSettingsToForm();
      applyTheme();
      applyVisualSettings();
      applyAutoRefresh();

      if (
        setting === "voiceActivationMode" ||
        setting === "wakeWord" ||
        setting === "speechLanguage"
      ) {
        stopWakeWordRecognition();
        applyVoiceActivationMode();
      }

      if (setting === "showTechInfo") {
        sourceBadge.style.display = uiSettings.showTechInfo ? "inline-block" : "none";
      }
    }

    return;
  }

  if (data.intent === "change_nlp_mode") {
    const mode = parameters.mode;
    if (mode === "ollama" || mode === "local_parser") {
      setLLMMode(mode);
    }
  }
}

function formatConfirmCurrency(value) {
  const number = Number(value || 0);

  return new Intl.NumberFormat("ru-RU", {
    style: "currency",
    currency: "RUB",
    maximumFractionDigits: 0,
  }).format(number);
}

async function loadOrderManagers() {
  try {
    const response = await fetch("/api/actions/managers");

    if (!response.ok) throw new Error("Ошибка загрузки менеджеров");

    const data = await response.json();
    orderManagers = data.managers || [];

    return orderManagers;
  } catch (error) {
    console.error("Ошибка загрузки менеджеров", error);
    orderManagers = [];
    return [];
  }
}

async function loadActionEmployees() {
  try {
    const response = await fetch("/api/actions/employees");

    if (!response.ok) throw new Error("Ошибка загрузки сотрудников");

    const data = await response.json();
    actionEmployees = data.employees || [];

    return actionEmployees;
  } catch (error) {
    console.error("Ошибка загрузки сотрудников", error);
    actionEmployees = [];
    return [];
  }
}

async function loadActionOrders() {
  try {
    const response = await fetch("/api/actions/orders");

    if (!response.ok) throw new Error("Ошибка загрузки заказов");

    const data = await response.json();
    actionOrders = data.orders || [];

    return actionOrders;
  } catch (error) {
    console.error("Ошибка загрузки заказов", error);
    actionOrders = [];
    return [];
  }
}

function createOptionList(items, selectedId, labelGetter) {
  if (!items || items.length === 0) {
    return `<option value="">Нет данных</option>`;
  }

  return items
    .map((item) => {
      const selected = Number(item.id) === Number(selectedId) ? "selected" : "";

      return `
        <option value="${item.id}" ${selected}>
          ${escapeHtml(labelGetter(item))}
        </option>
      `;
    })
    .join("");
}

async function showConfirmActionModal(actionData) {
  pendingAction = actionData;

  if (!confirmActionOverlay || !confirmActionBody) return;

  const action = actionData?.parameters?.action;
  const payload = actionData?.parameters?.payload || {};

  if (confirmActionApplyBtn) {
    confirmActionApplyBtn.textContent = action === "send_mailing" ? "Отправить" : "Добавить";
  }

  if (action === "create_order") {
    await loadOrderManagers();

    const selectedManagerId =
      payload.manager_id || (orderManagers.length > 0 ? orderManagers[0].id : "");

    const managerOptions = createOptionList(
      orderManagers,
      selectedManagerId,
      (manager) => `${manager.name} — ${manager.department || "Без отдела"}`
    );

    confirmActionBody.innerHTML = `
      <div class="confirm-row">
        <span class="confirm-key">Действие</span>
        <span class="confirm-value">Добавить заказ</span>
      </div>

      <div class="confirm-row">
        <span class="confirm-key">Клиент</span>
        <input id="confirmCustomerNameInput" class="confirm-input" value="${escapeHtml(payload.customer_name || "")}" />
      </div>

      <div class="confirm-row">
        <span class="confirm-key">Сумма</span>
        <input id="confirmOrderAmountInput" class="confirm-input" type="number" value="${escapeHtml(payload.amount || 0)}" />
      </div>

      <div class="confirm-row">
        <span class="confirm-key">Статус</span>
        <select id="confirmOrderStatusSelect" class="confirm-select">
          <option value="Новый" ${payload.status === "Новый" ? "selected" : ""}>Новый</option>
          <option value="В обработке" ${payload.status === "В обработке" ? "selected" : ""}>В обработке</option>
          <option value="Завершён" ${payload.status === "Завершён" ? "selected" : ""}>Завершён</option>
          <option value="Отменён" ${payload.status === "Отменён" ? "selected" : ""}>Отменён</option>
        </select>
      </div>

      <div class="confirm-row confirm-row-select">
        <span class="confirm-key">Менеджер</span>
        <select id="confirmManagerSelect" class="confirm-select">
          ${managerOptions}
        </select>
      </div>
    `;
  } else if (action === "create_employee") {
    confirmActionBody.innerHTML = `
      <div class="confirm-row">
        <span class="confirm-key">Действие</span>
        <span class="confirm-value">Добавить сотрудника</span>
      </div>

      <div class="confirm-row">
        <span class="confirm-key">ФИО</span>
        <input id="confirmEmployeeNameInput" class="confirm-input" value="${escapeHtml(payload.full_name || "")}" />
      </div>

      <div class="confirm-row">
        <span class="confirm-key">Должность</span>
        <input id="confirmEmployeePositionInput" class="confirm-input" value="${escapeHtml(payload.position || "Менеджер")}" />
      </div>

      <div class="confirm-row">
        <span class="confirm-key">Отдел</span>
        <input id="confirmEmployeeDepartmentInput" class="confirm-input" value="${escapeHtml(payload.department || "Продажи")}" />
      </div>
    `;
  } else if (action === "create_sale") {
    await loadActionOrders();

    const selectedOrderId =
      payload.order_id || (actionOrders.length > 0 ? actionOrders[0].id : "");

    const orderOptions = createOptionList(
      actionOrders,
      selectedOrderId,
      (order) => `Заказ №${order.id} — ${order.customer_name || "Клиент"} — ${formatCurrency(order.amount || 0)}`
    );

    confirmActionBody.innerHTML = `
      <div class="confirm-row">
        <span class="confirm-key">Действие</span>
        <span class="confirm-value">Добавить продажу</span>
      </div>

      <div class="confirm-row confirm-row-select">
        <span class="confirm-key">Заказ</span>
        <select id="confirmSaleOrderSelect" class="confirm-select">
          ${orderOptions}
        </select>
      </div>

      <div class="confirm-row">
        <span class="confirm-key">Товар</span>
        <input id="confirmSaleProductInput" class="confirm-input" value="${escapeHtml(payload.product_name || "")}" />
      </div>

      <div class="confirm-row">
        <span class="confirm-key">Количество</span>
        <input id="confirmSaleQuantityInput" class="confirm-input" type="number" min="1" value="${escapeHtml(payload.quantity || 1)}" />
      </div>

      <div class="confirm-row">
        <span class="confirm-key">Сумма</span>
        <input id="confirmSaleTotalInput" class="confirm-input" type="number" value="${escapeHtml(payload.total_price || 0)}" />
      </div>

      <div class="confirm-row">
        <span class="confirm-key">Дата продажи</span>
        <input id="confirmSaleDateInput" class="confirm-input" type="date" value="${escapeHtml(payload.sale_date || "")}" />
      </div>
    `;
  } else if (action === "create_task") {
    await loadActionEmployees();

    const selectedEmployeeId =
      payload.employee_id || (actionEmployees.length > 0 ? actionEmployees[0].id : "");

    const employeeOptions = createOptionList(
      actionEmployees,
      selectedEmployeeId,
      (employee) => `${employee.name} — ${employee.position || "Сотрудник"}`
    );

    const deadlineDate = payload.deadline ? String(payload.deadline).slice(0, 10) : "";

    confirmActionBody.innerHTML = `
      <div class="confirm-row">
        <span class="confirm-key">Действие</span>
        <span class="confirm-value">Создать задачу</span>
      </div>

      <div class="confirm-row">
        <span class="confirm-key">Название</span>
        <input id="confirmTaskTitleInput" class="confirm-input" value="${escapeHtml(payload.title || "")}" />
      </div>

      <div class="confirm-row">
        <span class="confirm-key">Описание</span>
        <input id="confirmTaskDescriptionInput" class="confirm-input" value="${escapeHtml(payload.description || "")}" />
      </div>

      <div class="confirm-row confirm-row-select">
        <span class="confirm-key">Исполнитель</span>
        <select id="confirmTaskEmployeeSelect" class="confirm-select">
          ${employeeOptions}
        </select>
      </div>

      <div class="confirm-row">
        <span class="confirm-key">Статус</span>
        <select id="confirmTaskStatusSelect" class="confirm-select">
          <option value="Активная" ${payload.status === "Активная" ? "selected" : ""}>Активная</option>
          <option value="Просрочена" ${payload.status === "Просрочена" ? "selected" : ""}>Просрочена</option>
          <option value="Завершена" ${payload.status === "Завершена" ? "selected" : ""}>Завершена</option>
        </select>
      </div>

      <div class="confirm-row">
        <span class="confirm-key">Приоритет</span>
        <select id="confirmTaskPrioritySelect" class="confirm-select">
          <option value="Низкий" ${payload.priority === "Низкий" ? "selected" : ""}>Низкий</option>
          <option value="Средний" ${payload.priority === "Средний" ? "selected" : ""}>Средний</option>
          <option value="Высокий" ${payload.priority === "Высокий" ? "selected" : ""}>Высокий</option>
        </select>
      </div>

      <div class="confirm-row">
        <span class="confirm-key">Срок</span>
        <input id="confirmTaskDeadlineInput" class="confirm-input" type="date" value="${escapeHtml(deadlineDate)}" />
      </div>
    `;
  } else if (action === "send_mailing") {
    const selectedChannels = Array.isArray(payload.channels) ? payload.channels : [];
    const selectedTarget = payload.target || "employees";

    confirmActionBody.innerHTML = `
      <div class="confirm-row">
        <span class="confirm-key">Действие</span>
        <span class="confirm-value">Отправить рассылку</span>
      </div>

      <div class="confirm-row confirm-row-stacked">
        <span class="confirm-key">Канал</span>
        <div class="mailing-channel-grid">
          <button
            id="mailingTelegramChannelBtn"
            class="mailing-channel-btn ${selectedChannels.includes("telegram") ? "active" : ""}"
            type="button"
            data-channel="telegram"
          >
            Telegram
          </button>
          <button class="mailing-channel-btn disabled" type="button" disabled>VK</button>
          <button class="mailing-channel-btn disabled" type="button" disabled>Почта</button>
          <button class="mailing-channel-btn disabled" type="button" disabled>WhatsApp</button>
        </div>
      </div>

      <div class="confirm-row confirm-row-stacked">
        <span class="confirm-key">Получатели</span>
        <div class="mailing-target-grid">
          <button
            class="mailing-target-btn ${selectedTarget === "employees" ? "active" : ""}"
            type="button"
            data-target="employees"
          >
            Работники
          </button>
          <button
            class="mailing-target-btn ${selectedTarget === "clients" ? "active" : ""}"
            type="button"
            data-target="clients"
          >
            Клиенты
          </button>
          <button
            class="mailing-target-btn ${selectedTarget === "all" ? "active" : ""}"
            type="button"
            data-target="all"
          >
            Все
          </button>
        </div>
      </div>

      <div class="confirm-row confirm-row-stacked">
        <span class="confirm-key">Текст рассылки</span>
        <textarea
          id="confirmMailingMessageInput"
          class="confirm-input confirm-textarea"
          rows="5"
          placeholder="Введите текст, который должен появиться в Telegram"
        >${escapeHtml(payload.message || "")}</textarea>
      </div>

      <div class="confirm-row confirm-row-stacked">
        <span class="confirm-key">Вложения</span>
        <input
          id="confirmMailingFilesInput"
          class="confirm-file-input"
          type="file"
          multiple
        />
        <div id="confirmMailingFilesList" class="mailing-files-list">
          Файлы не выбраны
        </div>
      </div>
    `;

    document.getElementById("mailingTelegramChannelBtn")?.addEventListener("click", (event) => {
      event.currentTarget.classList.toggle("active");
    });

    document.querySelectorAll(".mailing-target-btn").forEach((button) => {
      button.addEventListener("click", () => {
        document.querySelectorAll(".mailing-target-btn").forEach((item) => {
          item.classList.remove("active");
        });
        button.classList.add("active");
      });
    });

    document.getElementById("confirmMailingFilesInput")?.addEventListener("change", renderMailingFilesList);
  } else {
    confirmActionBody.innerHTML = `
      <div class="confirm-row">
        <span class="confirm-key">Действие</span>
        <span class="confirm-value">${escapeHtml(action || "—")}</span>
      </div>
    `;
  }

  confirmActionOverlay.classList.remove("hidden");
}

function hideConfirmActionModal() {
  pendingAction = null;

  if (confirmActionOverlay) {
    confirmActionOverlay.classList.add("hidden");
  }
}

function isVoiceConfirmCommand(text) {
  const normalized = normalizeVoiceText(text);

  return (
    normalized === "добавить" ||
    normalized === "подтверди" ||
    normalized === "подтвердить" ||
    normalized === "да" ||
    normalized === "выполнить" ||
    normalized === "отправить" ||
    normalized === "отправь" ||
    normalized === "сохрани" ||
    normalized === "сохранить" ||
    normalized === "add" ||
    normalized === "confirm" ||
    normalized === "yes" ||
    normalized === "save"
  );
}

function isVoiceCancelCommand(text) {
  const normalized = normalizeVoiceText(text);

  return (
    normalized === "отмена" ||
    normalized === "отмени" ||
    normalized === "отменить" ||
    normalized === "нет" ||
    normalized === "не добавлять" ||
    normalized === "не надо" ||
    normalized === "cancel" ||
    normalized === "no"
  );
}

function renderMailingFilesList() {
  const input = document.getElementById("confirmMailingFilesInput");
  const list = document.getElementById("confirmMailingFilesList");

  if (!input || !list) return;

  const files = Array.from(input.files || []);

  if (files.length === 0) {
    list.textContent = "Файлы не выбраны";
    return;
  }

  list.innerHTML = files
    .map((file) => {
      const sizeKb = Math.max(1, Math.round(file.size / 1024));
      return `
        <div class="mailing-file-item">
          <span>${escapeHtml(file.name)}</span>
          <small>${sizeKb} КБ</small>
        </div>
      `;
    })
    .join("");
}

function collectPendingPayloadFromModal() {
  if (!pendingAction) return null;

  const action = pendingAction?.parameters?.action;
  const payload = pendingAction?.parameters?.payload || {};

  if (action === "create_order") {
    payload.customer_name =
      document.getElementById("confirmCustomerNameInput")?.value?.trim() || payload.customer_name;
    payload.amount = Number(document.getElementById("confirmOrderAmountInput")?.value || payload.amount || 0);
    payload.status = document.getElementById("confirmOrderStatusSelect")?.value || payload.status || "Новый";
    payload.manager_id = Number(document.getElementById("confirmManagerSelect")?.value || payload.manager_id || 0);
  }

  if (action === "create_employee") {
    payload.full_name =
      document.getElementById("confirmEmployeeNameInput")?.value?.trim() || payload.full_name;
    payload.position =
      document.getElementById("confirmEmployeePositionInput")?.value?.trim() || payload.position;
    payload.department =
      document.getElementById("confirmEmployeeDepartmentInput")?.value?.trim() || payload.department;
  }

  if (action === "create_sale") {
    payload.order_id = Number(document.getElementById("confirmSaleOrderSelect")?.value || payload.order_id || 0);
    payload.product_name =
      document.getElementById("confirmSaleProductInput")?.value?.trim() || payload.product_name;
    payload.quantity = Number(document.getElementById("confirmSaleQuantityInput")?.value || payload.quantity || 1);
    payload.total_price = Number(document.getElementById("confirmSaleTotalInput")?.value || payload.total_price || 0);
    payload.sale_date = document.getElementById("confirmSaleDateInput")?.value || payload.sale_date;
  }

  if (action === "create_task") {
    payload.title = document.getElementById("confirmTaskTitleInput")?.value?.trim() || payload.title;
    payload.description =
      document.getElementById("confirmTaskDescriptionInput")?.value?.trim() || payload.description || "";
    payload.employee_id = Number(document.getElementById("confirmTaskEmployeeSelect")?.value || payload.employee_id || 0);
    payload.status = document.getElementById("confirmTaskStatusSelect")?.value || payload.status || "Активная";
    payload.priority = document.getElementById("confirmTaskPrioritySelect")?.value || payload.priority || "Средний";

    const deadlineDate = document.getElementById("confirmTaskDeadlineInput")?.value;

    if (deadlineDate) {
      payload.deadline = `${deadlineDate}T23:59:00`;
    }
  }

  if (action === "send_mailing") {
    const selectedChannels = [];
    const telegramBtn = document.getElementById("mailingTelegramChannelBtn");
    const filesInput = document.getElementById("confirmMailingFilesInput");
    const selectedTargetBtn = document.querySelector(".mailing-target-btn.active");

    if (telegramBtn?.classList.contains("active")) {
      selectedChannels.push("telegram");
    }

    payload.channels = selectedChannels;
    payload.target = selectedTargetBtn?.dataset?.target || "employees";
    payload.message = document.getElementById("confirmMailingMessageInput")?.value?.trim() || "";
    payload.attachments_count = filesInput?.files?.length || 0;
  }

  return payload;
}

function trySelectPendingFieldByVoice(text) {
  if (!pendingAction) return false;

  const action = pendingAction?.parameters?.action;
  const payload = pendingAction?.parameters?.payload || {};
  const normalized = normalizeVoiceText(text);

  if (action === "create_order") {
    if (
      normalized.startsWith("клиент ") ||
      normalized.startsWith("клиента ") ||
      normalized.includes(" клиент ")
    ) {
      const value = extractTextAfterKeyword(
        text,
        ["клиент", "клиента"],
        ["сумма", "на сумму", "статус", "менеджер"]
      );

      if (value) {
        const formatted = toDisplayCase(value);

        payload.customer_name = formatted;
        setInputValue("confirmCustomerNameInput", formatted);
        setVoiceFieldResult(`Клиент изменён: ${formatted}`);
        return true;
      }
    }

    if (
      normalized.includes("сумм") ||
      normalized.includes("цена") ||
      normalized.includes("стоимость")
    ) {
      const value = extractNumberFromText(text);

      if (value !== null) {
        payload.amount = value;
        setInputValue("confirmOrderAmountInput", value);
        setVoiceFieldResult(`Сумма заказа изменена: ${formatCurrency(value)}`);
        return true;
      }
    }

    if (normalized.includes("статус")) {
      const status = parseOrderStatus(text);

      if (status) {
        payload.status = status;
        setSelectValue("confirmOrderStatusSelect", status);
        setVoiceFieldResult(`Статус заказа изменён: ${status}`);
        return true;
      }

      setVoiceFieldResult("Статус не распознан. Скажите: новый, в обработке, завершён или отменён");
      return true;
    }

    if (normalized.includes("менеджер") || normalized.includes("менеджера")) {
      let selectedManager = null;

      const numberMatch = normalized.match(/(?:менеджер|менеджера)\s+([0-9]+)/);

      if (numberMatch) {
        const managerId = Number(numberMatch[1]);
        selectedManager = orderManagers.find((manager) => Number(manager.id) === managerId);
      }

      if (!selectedManager) {
        selectedManager = orderManagers.find((manager) => {
          const name = String(manager.name || "").toLowerCase().replaceAll("ё", "е");
          const surname = name.split(" ")[0];

          return normalized.includes(name) || normalized.includes(surname);
        });
      }

      if (!selectedManager) {
        setVoiceFieldResult("Менеджер не найден. Скажите: менеджер Иванов или менеджер 1");
        return true;
      }

      payload.manager_id = selectedManager.id;
      setSelectValue("confirmManagerSelect", selectedManager.id);
      setVoiceFieldResult(`Выбран менеджер: ${selectedManager.name}`);
      return true;
    }

    return false;
  }

  if (action === "create_employee") {
    if (
      normalized.startsWith("фио ") ||
      normalized.includes("фио ") ||
      normalized.includes("имя сотрудника")
    ) {
      const value = extractTextAfterKeyword(
        text,
        ["фио", "имя сотрудника", "сотрудник"],
        ["должность", "отдел", "департамент"]
      );

      if (value) {
        const formatted = toDisplayCase(value);

        payload.full_name = formatted;
        setInputValue("confirmEmployeeNameInput", formatted);
        setVoiceFieldResult(`ФИО изменено: ${formatted}`);
        return true;
      }
    }

    if (normalized.includes("должность")) {
      const value = extractTextAfterKeyword(
        text,
        ["должность", "на должность"],
        ["отдел", "департамент"]
      );

      if (value) {
        const formatted = toDisplayCase(value);

        payload.position = formatted;
        setInputValue("confirmEmployeePositionInput", formatted);
        setVoiceFieldResult(`Должность изменена: ${formatted}`);
        return true;
      }
    }

    if (normalized.includes("отдел") || normalized.includes("департамент")) {
      const value = extractTextAfterKeyword(
        text,
        ["отдел", "департамент"],
        ["должность"]
      );

      if (value) {
        const formatted = toDisplayCase(value);

        payload.department = formatted;
        setInputValue("confirmEmployeeDepartmentInput", formatted);
        setVoiceFieldResult(`Отдел изменён: ${formatted}`);
        return true;
      }
    }

    return false;
  }

  if (action === "create_sale") {
    if (normalized.includes("заказ")) {
      const numberMatch = normalized.match(/заказ\s+([0-9]+)/);

      if (!numberMatch) {
        setVoiceFieldResult("Номер заказа не распознан. Скажите: заказ 5");
        return true;
      }

      const orderId = Number(numberMatch[1]);
      const selectedOrder = actionOrders.find((order) => Number(order.id) === orderId);

      if (!selectedOrder) {
        setVoiceFieldResult("Заказ не найден в списке");
        return true;
      }

      payload.order_id = selectedOrder.id;
      setSelectValue("confirmSaleOrderSelect", selectedOrder.id);
      setVoiceFieldResult(`Выбран заказ №${selectedOrder.id}`);
      return true;
    }

    if (normalized.includes("товар") || normalized.includes("продукт")) {
      const value = extractTextAfterKeyword(
        text,
        ["товар", "продукт"],
        ["количество", "кол-во", "сумма", "на сумму", "цена", "стоимость", "дата"]
      );

      if (value) {
        const formatted = toDisplayCase(value);

        payload.product_name = formatted;
        setInputValue("confirmSaleProductInput", formatted);
        setVoiceFieldResult(`Товар изменён: ${formatted}`);
        return true;
      }
    }

    if (
      normalized.includes("количество") ||
      normalized.includes("кол-во") ||
      normalized.includes("штук") ||
      normalized.includes("штуки")
    ) {
      const value = extractNumberFromText(text);

      if (value !== null) {
        payload.quantity = value;
        setInputValue("confirmSaleQuantityInput", value);
        setVoiceFieldResult(`Количество изменено: ${value}`);
        return true;
      }

      setVoiceFieldResult("Количество не распознано. Скажите: количество 4 или количество четыре");
      return true;
    }

    if (
      normalized.includes("сумм") ||
      normalized.includes("цена") ||
      normalized.includes("стоимость")
    ) {
      const value = extractNumberFromText(text);

      if (value !== null) {
        payload.total_price = value;
        setInputValue("confirmSaleTotalInput", value);
        setVoiceFieldResult(`Сумма продажи изменена: ${formatCurrency(value)}`);
        return true;
      }
    }

    if (
      normalized.includes("дата") ||
      normalized.includes("сегодня") ||
      normalized.includes("завтра") ||
      normalized.includes("послезавтра")
    ) {
      const date = parseVoiceDate(text);

      if (date) {
        payload.sale_date = date;
        setInputValue("confirmSaleDateInput", date);
        setVoiceFieldResult(`Дата продажи изменена: ${date}`);
        return true;
      }

      setVoiceFieldResult("Дата не распознана. Скажите: дата сегодня, дата завтра или 2026-04-30");
      return true;
    }

    return false;
  }

  if (action === "create_task") {
    if (normalized.includes("название") || normalized.startsWith("назови ")) {
      const value = extractTextAfterKeyword(
        text,
        ["название", "назови"],
        ["описание", "исполнитель", "сотрудник", "статус", "приоритет", "срок", "дедлайн"]
      );

      if (value) {
        const formatted = toDisplayCase(value);

        payload.title = formatted;
        setInputValue("confirmTaskTitleInput", formatted);
        setVoiceFieldResult(`Название задачи изменено: ${formatted}`);
        return true;
      }
    }

    if (normalized.includes("описание")) {
      const value = extractTextAfterKeyword(
        text,
        ["описание"],
        ["исполнитель", "сотрудник", "статус", "приоритет", "срок", "дедлайн"]
      );

      if (value) {
        const formatted = capitalizeFirst(value);

        payload.description = formatted;
        setInputValue("confirmTaskDescriptionInput", formatted);
        setVoiceFieldResult(`Описание изменено: ${formatted}`);
        return true;
      }
    }

    if (normalized.includes("исполнитель") || normalized.includes("сотрудник")) {
      let selectedEmployee = null;

      const numberMatch = normalized.match(/(?:исполнитель|сотрудник)\s+([0-9]+)/);

      if (numberMatch) {
        const employeeId = Number(numberMatch[1]);
        selectedEmployee = actionEmployees.find((employee) => Number(employee.id) === employeeId);
      }

      if (!selectedEmployee) {
        selectedEmployee = actionEmployees.find((employee) => {
          const name = String(employee.name || "").toLowerCase().replaceAll("ё", "е");
          const surname = name.split(" ")[0];

          return normalized.includes(name) || normalized.includes(surname);
        });
      }

      if (!selectedEmployee) {
        setVoiceFieldResult("Исполнитель не найден. Скажите: исполнитель Иванов или сотрудник 1");
        return true;
      }

      payload.employee_id = selectedEmployee.id;
      setSelectValue("confirmTaskEmployeeSelect", selectedEmployee.id);
      setVoiceFieldResult(`Выбран исполнитель: ${selectedEmployee.name}`);
      return true;
    }

    if (normalized.includes("статус")) {
      const status = parseTaskStatus(text);

      if (status) {
        payload.status = status;
        setSelectValue("confirmTaskStatusSelect", status);
        setVoiceFieldResult(`Статус задачи изменён: ${status}`);
        return true;
      }

      setVoiceFieldResult("Статус не распознан. Скажите: активная, просрочена или завершена");
      return true;
    }

    if (normalized.includes("приоритет")) {
      const priority = parsePriority(text);

      if (priority) {
        payload.priority = priority;
        setSelectValue("confirmTaskPrioritySelect", priority);
        setVoiceFieldResult(`Приоритет задачи изменён: ${priority}`);
        return true;
      }

      setVoiceFieldResult("Приоритет не распознан. Скажите: высокий, средний или низкий");
      return true;
    }

    if (
      normalized.includes("срок") ||
      normalized.includes("дедлайн") ||
      normalized.includes("сегодня") ||
      normalized.includes("завтра") ||
      normalized.includes("послезавтра")
    ) {
      const date = parseVoiceDate(text);

      if (date) {
        payload.deadline = `${date}T23:59:00`;
        setInputValue("confirmTaskDeadlineInput", date);
        setVoiceFieldResult(`Срок задачи изменён: ${date}`);
        return true;
      }

      setVoiceFieldResult("Срок не распознан. Скажите: срок завтра или срок 2026-04-30");
      return true;
    }

    return false;
  }

  if (action === "send_mailing") {
    if (
      normalized.includes("телеграм") ||
      normalized.includes("telegram") ||
      normalized === "тг" ||
      normalized.includes(" тг")
    ) {
      if (!Array.isArray(payload.channels)) {
        payload.channels = [];
      }

      if (!payload.channels.includes("telegram")) {
        payload.channels.push("telegram");
      }

      document.getElementById("mailingTelegramChannelBtn")?.classList.add("active");
      setVoiceFieldResult("Выбран канал Telegram");
      return true;
    }

    if (
      normalized.includes("работник") ||
      normalized.includes("сотрудник")
    ) {
      document.querySelectorAll(".mailing-target-btn").forEach((item) => item.classList.remove("active"));
      document.querySelector('.mailing-target-btn[data-target="employees"]')?.classList.add("active");
      payload.target = "employees";
      setVoiceFieldResult("Выбраны получатели: работники");
      return true;
    }

    if (
      normalized.includes("клиент") ||
      normalized.includes("обычн")
    ) {
      document.querySelectorAll(".mailing-target-btn").forEach((item) => item.classList.remove("active"));
      document.querySelector('.mailing-target-btn[data-target="clients"]')?.classList.add("active");
      payload.target = "clients";
      setVoiceFieldResult("Выбраны получатели: клиенты");
      return true;
    }

    if (
      normalized === "всем" ||
      normalized.includes("для всех") ||
      normalized.includes("все получатели")
    ) {
      document.querySelectorAll(".mailing-target-btn").forEach((item) => item.classList.remove("active"));
      document.querySelector('.mailing-target-btn[data-target="all"]')?.classList.add("active");
      payload.target = "all";
      setVoiceFieldResult("Выбраны получатели: все");
      return true;
    }

    if (
      normalized.startsWith("текст ") ||
      normalized.startsWith("сообщение ") ||
      normalized.startsWith("напиши ") ||
      normalized.includes("текст рассылки")
    ) {
      const value = extractTextAfterKeyword(
        text,
        ["текст рассылки", "текст", "сообщение", "напиши"],
        ["канал", "телеграм", "telegram"]
      );

      if (value) {
        const message = capitalizeFirst(value);

        payload.message = message;
        setInputValue("confirmMailingMessageInput", message);
        setVoiceFieldResult("Текст рассылки изменён");
        return true;
      }
    }

    if (normalized.length > 2) {
      const message = capitalizeFirst(text.trim());

      payload.message = message;
      setInputValue("confirmMailingMessageInput", message);
      setVoiceFieldResult("Текст рассылки изменён");
      return true;
    }

    return false;
  }

  return false;
}

async function confirmPendingAction() {
  if (!pendingAction) return;

  const actionData = pendingAction;
  const action = actionData?.parameters?.action;
  const payload = collectPendingPayloadFromModal();

  if (!payload) return;

  if (action === "create_order" && !payload.manager_id) {
    alert("Выберите менеджера для заказа");
    return;
  }

  if (action === "create_sale" && !payload.order_id) {
    alert("Выберите заказ для продажи");
    return;
  }

  if (action === "create_task" && !payload.employee_id) {
    alert("Выберите исполнителя задачи");
    return;
  }

  if (action === "send_mailing" && (!payload.channels || payload.channels.length === 0)) {
    alert("Выберите канал Telegram");
    return;
  }

  if (action === "send_mailing" && !payload.message && !payload.attachments_count) {
    alert("Введите текст рассылки или прикрепите файл");
    return;
  }

  try {
    let response;

    if (action === "send_mailing") {
      const formData = new FormData();
      const filesInput = document.getElementById("confirmMailingFilesInput");
      const files = Array.from(filesInput?.files || []);

      formData.append("channels", JSON.stringify(payload.channels || []));
      formData.append("target", payload.target || "employees");
      formData.append("message", payload.message || "");

      files.forEach((file) => {
        formData.append("files", file);
      });

      response = await fetch("/api/mailings/send", {
        method: "POST",
        body: formData,
      });
    } else {
      response = await fetch("/api/actions/confirm", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          action,
          payload,
        }),
      });
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Ошибка подтверждения действия");
    }

    hideConfirmActionModal();

    const result = {
      recognized_text: actionData.recognized_text || "",
      intent: action,
      parameters: payload,
      source: "confirmed_action",
      fallback: false,
      fallback_reason: null,
      result_text: data.result_text || "Действие выполнено",
      data: data.data || [],
    };

    renderCommandResult(result);
    await loadDashboard();

    if (pageSections.orders?.classList.contains("active-page")) await loadOrdersPage();
    if (pageSections.tasks?.classList.contains("active-page")) await loadTasksPage();
    if (pageSections.reports?.classList.contains("active-page")) await loadReportsPage();
  } catch (error) {
    console.error(error);
    alert(
      uiSettings.siteLanguage === "en"
        ? "Failed to confirm action"
        : `Не удалось выполнить действие: ${error.message}`
    );
  }
}

function cancelPendingAction() {
  hideConfirmActionModal();

  resultTextBlock.textContent = "Действие отменено";
  commandOutputSubtitle.textContent = "Добавление в базу данных отменено";
}

function renderCommandResult(data) {
  lastCommandResultForPdf = data;

  recognizedText.textContent = `«${data.recognized_text || "—"}»`;

  const intent = data.intent || "—";
  const source = data.source || "—";
  const resultText =
    data.result_text || (uiSettings.siteLanguage === "en" ? "No result" : "Результат отсутствует");

  intentBadge.textContent = intent;
  sourceBadge.textContent = source;
  resultTextBlock.textContent = resultText;

  intentBadge.classList.remove("error");
  sourceBadge.classList.remove("local", "ollama");

  if (intent === "error") intentBadge.classList.add("error");

  if (
    source === "local_parser" ||
    source === "local_ui_parser" ||
    source === "local_action_parser" ||
    source === "confirmed_action" ||
    source === "system"
  ) {
    sourceBadge.classList.add("local");
  }

  if (source === "ollama" || source === "ollama_ui_parser") {
    sourceBadge.classList.add("ollama");
  }

  if (data.fallback) sourceBadge.textContent = `${source} / fallback`;

  sourceBadge.style.display = uiSettings.showTechInfo ? "inline-block" : "none";

  renderParams(data.parameters || {});

  commandOutputSubtitle.textContent = resultText;
  renderCommandData(data.data || [], intent);

  if (data.intent === "confirm_action") {
    showConfirmActionModal(data);
  }
}

async function loadDashboard() {
  try {
    const response = await fetch("/api/dashboard");

    if (!response.ok) throw new Error("Ошибка загрузки dashboard");

    const data = await response.json();

    commandsToday.textContent = data.stats.commands_today ?? 0;
    successCommands.textContent = data.stats.success_commands ?? 0;
    activeTasksCount.textContent = data.stats.active_tasks ?? 0;
    reportsCount.textContent = data.stats.reports_count ?? 0;

    const sales = Number(data.reports.total_sales || 0);
    const orders = Number(data.reports.orders_count || 0);
    const avg = orders > 0 ? sales / orders : 0;

    totalSales.textContent = formatCurrency(sales);
    ordersCount.textContent = orders;
    averageCheck.textContent = formatCurrency(avg);

    renderHistory(data.history);
    renderTasks(data.tasks);
  } catch (error) {
    console.error(error);

    historyList.innerHTML = `<p class="empty-text">${
      uiSettings.siteLanguage === "en" ? "Failed to load history" : "Не удалось загрузить историю"
    }</p>`;
    tasksList.innerHTML = `<p class="empty-text">${
      uiSettings.siteLanguage === "en" ? "Failed to load tasks" : "Не удалось загрузить задачи"
    }</p>`;
  }
}

async function startRecording() {
  try {
    if (wakeRecognitionActive) stopWakeWordRecognition();

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    audioChunks = [];
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
      stream.getTracks().forEach((track) => track.stop());
      await sendAudio(audioBlob);

      if (uiSettings.voiceActivationMode === "wake_word") {
        setTimeout(startWakeWordRecognition, 700);
      }
    };

    mediaRecorder.start();
    isRecording = true;

    recordBtn.classList.add("recording");
    recordBtn.textContent = "⏹";
    voiceTitle.textContent = uiSettings.siteLanguage === "en" ? "Recording..." : "Идёт запись...";
    systemStatusText.textContent = uiSettings.siteLanguage === "en" ? "Listening" : "Слушаю команду";

    recognizedText.textContent = "—";
    intentBadge.textContent = "—";
    sourceBadge.textContent = "—";
    sourceBadge.style.display = "inline-block";
    resultTextBlock.textContent = uiSettings.siteLanguage === "en" ? "Recording voice..." : "Запись голоса...";
    paramsBlock.innerHTML = `<span class="empty-data">${
      uiSettings.siteLanguage === "en" ? "Waiting for result" : "Ожидание результата"
    }</span>`;

    commandDataBlock.innerHTML = `
      <div class="empty-command-result">
        ${uiSettings.siteLanguage === "en" ? "Waiting for command result..." : "Ожидание результата команды..."}
      </div>
    `;
    commandOutputSubtitle.textContent =
      uiSettings.siteLanguage === "en" ? "Command is being processed" : "Команда обрабатывается";
  } catch (error) {
    console.error(error);
    alert(uiSettings.siteLanguage === "en" ? "Failed to access microphone" : "Не удалось получить доступ к микрофону");
  }
}

function stopRecording() {
  if (mediaRecorder && isRecording) {
    mediaRecorder.stop();
    isRecording = false;

    recordBtn.classList.remove("recording");
    recordBtn.textContent = "🎤";
    voiceTitle.textContent = uiSettings.siteLanguage === "en" ? "Processing audio..." : "Обрабатываю аудио...";
    systemStatusText.textContent = uiSettings.siteLanguage === "en" ? "Processing command" : "Обработка команды";
    resultTextBlock.textContent = uiSettings.siteLanguage === "en" ? "Audio sent to server..." : "Аудио отправлено на сервер...";
  }
}

function shouldExecuteUiIntent(intent) {
  return (
    intent === "open_page" ||
    intent === "change_theme" ||
    intent === "change_language" ||
    intent === "change_setting" ||
    intent === "change_nlp_mode" ||
    intent === "clear_history" ||
    intent === "download_pdf" ||
    intent === "build_chart" ||
    intent === "open_help" ||
    intent === "help_question"
  );
}

async function sendAudio(audioBlob) {
  const formData = new FormData();
  formData.append("file", audioBlob, "voice.webm");

  try {
    const response = await fetch("/api/voice", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Ошибка обработки аудио");

    const data = await response.json();

    if (pendingAction) {
      const text = data.recognized_text || "";

      if (trySelectPendingFieldByVoice(text)) return;

      if (isVoiceConfirmCommand(text)) {
        await confirmPendingAction();
        return;
      }

      if (isVoiceCancelCommand(text)) {
        cancelPendingAction();
        return;
      }
    }

    renderCommandResult(data);

    if (shouldExecuteUiIntent(data.intent)) {
      executeVoiceUiCommand(data);
    }

    voiceTitle.textContent = uiSettings.siteLanguage === "en" ? "Command processed" : "Команда обработана";
    systemStatusText.textContent = uiSettings.siteLanguage === "en" ? "Ready for commands" : "Готов к приёму команд";

    if (data.intent !== "open_page" && data.intent !== "clear_history") await loadDashboard();

    await loadLLMMode();
  } catch (error) {
    console.error(error);

    recognizedText.textContent = uiSettings.siteLanguage === "en" ? "Audio processing error" : "Ошибка обработки аудио";
    intentBadge.textContent = "error";
    intentBadge.classList.add("error");
    sourceBadge.textContent = "system";
    resultTextBlock.textContent =
      uiSettings.siteLanguage === "en"
        ? "Check /api/voice endpoint and server console"
        : "Проверьте endpoint /api/voice и консоль сервера";
    paramsBlock.innerHTML = `<span class="empty-data">${getT("noParams")}</span>`;

    commandDataBlock.innerHTML = `
      <div class="empty-command-result">
        ${uiSettings.siteLanguage === "en" ? "Command processing error" : "Ошибка обработки команды"}
      </div>
    `;
    commandOutputSubtitle.textContent = uiSettings.siteLanguage === "en" ? "An error occurred" : "Произошла ошибка";

    voiceTitle.textContent = uiSettings.siteLanguage === "en" ? "Error" : "Ошибка";
    systemStatusText.textContent = uiSettings.siteLanguage === "en" ? "Processing error" : "Ошибка обработки";
  }
}

async function sendTextCommand(commandText) {
  if (!commandText) return;

  if (pendingAction) {
    if (trySelectPendingFieldByVoice(commandText)) return;

    if (isVoiceConfirmCommand(commandText)) {
      await confirmPendingAction();
      return;
    }

    if (isVoiceCancelCommand(commandText)) {
      cancelPendingAction();
      return;
    }
  }

  if (wakeCommandProcessing) return;

  wakeCommandProcessing = true;

  try {
    recognizedText.textContent = `«${commandText}»`;
    voiceTitle.textContent =
      uiSettings.siteLanguage === "en" ? "Wake word command detected" : "Команда по ключевому слову обнаружена";
    systemStatusText.textContent = uiSettings.siteLanguage === "en" ? "Processing command" : "Обработка команды";
    resultTextBlock.textContent =
      uiSettings.siteLanguage === "en" ? "Sending command to server..." : "Отправляю команду на сервер...";

    const response = await fetch("/api/voice/text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: commandText }),
    });

    if (!response.ok) throw new Error("Text command processing error");

    const data = await response.json();

    renderCommandResult(data);

    if (shouldExecuteUiIntent(data.intent)) {
      executeVoiceUiCommand(data);
    }

    voiceTitle.textContent = uiSettings.siteLanguage === "en" ? "Command processed" : "Команда обработана";
    systemStatusText.textContent = uiSettings.siteLanguage === "en" ? "Ready for commands" : "Готов к приёму команд";

    if (data.intent !== "open_page" && data.intent !== "clear_history") await loadDashboard();

    await loadLLMMode();
  } catch (error) {
    console.error(error);
    voiceTitle.textContent =
      uiSettings.siteLanguage === "en" ? "Wake word command error" : "Ошибка команды по ключевому слову";
    systemStatusText.textContent = uiSettings.siteLanguage === "en" ? "Processing error" : "Ошибка обработки";
  } finally {
    wakeCommandProcessing = false;
  }
}

function getSpeechRecognitionConstructor() {
  return window.SpeechRecognition || window.webkitSpeechRecognition || null;
}

function updateWakeWordStatus(status, text) {
  if (!wakeWordStatusDot || !wakeWordStatusText) return;

  wakeWordStatusDot.classList.remove("active", "inactive", "error");

  if (status === "active") {
    wakeWordStatusDot.classList.add("active");
  } else if (status === "error") {
    wakeWordStatusDot.classList.add("error");
  } else {
    wakeWordStatusDot.classList.add("inactive");
  }

  wakeWordStatusText.textContent = text;
}

function getRecognitionLanguage() {
  if (uiSettings.speechLanguage === "en") return "en-US";
  return "ru-RU";
}

function extractCommandAfterWakeWord(transcript) {
  const wakeWord = (uiSettings.wakeWord || "помощник").toLowerCase().trim();
  const normalizedTranscript = transcript.toLowerCase().trim();

  const wakeIndex = normalizedTranscript.indexOf(wakeWord);

  if (wakeIndex === -1) return null;

  const command = transcript
    .slice(wakeIndex + wakeWord.length)
    .replace(/^,/, "")
    .replace(/^\./, "")
    .replace(/^:/, "")
    .replace(/^!/, "")
    .trim();

  return command || null;
}

function startWakeWordRecognition() {
  const SpeechRecognitionConstructor = getSpeechRecognitionConstructor();

  if (!SpeechRecognitionConstructor) {
    updateWakeWordStatus("error", getT("wakeUnsupported"));
    return;
  }

  if (wakeRecognitionActive || wakeCommandProcessing || isRecording) return;

  wakeRecognition = new SpeechRecognitionConstructor();
  wakeRecognition.lang = getRecognitionLanguage();
  wakeRecognition.continuous = true;
  wakeRecognition.interimResults = false;
  wakeRecognition.maxAlternatives = 1;

  wakeRecognition.onstart = () => {
    wakeRecognitionActive = true;
    updateWakeWordStatus("active", `${getT("wakeWaiting")}: ${uiSettings.wakeWord}`);
  };

  wakeRecognition.onresult = (event) => {
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript.trim();
      console.log("Wake transcript:", transcript);

      const command = extractCommandAfterWakeWord(transcript);

      if (command) sendTextCommand(command);
    }
  };

  wakeRecognition.onerror = (event) => {
    console.warn("Wake recognition error:", event.error);

    if (event.error === "not-allowed" || event.error === "service-not-allowed") {
      updateWakeWordStatus("error", getT("wakeDenied"));
      stopWakeWordRecognition();
      return;
    }

    updateWakeWordStatus("error", getT("wakeError"));
  };

  wakeRecognition.onend = () => {
    wakeRecognitionActive = false;

    if (uiSettings.voiceActivationMode === "wake_word") {
      updateWakeWordStatus("inactive", "Перезапуск режима ожидания...");

      setTimeout(() => {
        startWakeWordRecognition();
      }, 1200);
    } else {
      updateWakeWordStatus("inactive", getT("wakeDisabled"));
    }
  };

  try {
    wakeRecognition.start();
  } catch (error) {
    console.warn("Wake recognition start error:", error);
  }
}

function stopWakeWordRecognition() {
  if (wakeRecognition) {
    try {
      wakeRecognition.onend = null;
      wakeRecognition.stop();
    } catch (error) {
      console.warn("Wake recognition stop error:", error);
    }
  }

  wakeRecognition = null;
  wakeRecognitionActive = false;

  updateWakeWordStatus("inactive", getT("wakeDisabled"));
}

function applyVoiceActivationMode() {
  if (uiSettings.voiceActivationMode === "wake_word") {
    startWakeWordRecognition();
  } else {
    stopWakeWordRecognition();
  }
}

function collectCurrentResultForPdf() {
  return {
    recognized_text: recognizedText ? recognizedText.textContent.replace(/[«»]/g, "").trim() : "",
    intent: intentBadge ? intentBadge.textContent.trim() : "",
    source: sourceBadge ? sourceBadge.textContent.trim() : "",
    result_text: resultTextBlock ? resultTextBlock.textContent.trim() : "",
    parameters: {},
    data: [],
  };
}

async function downloadLastCommandPdf() {
  const payload = lastCommandResultForPdf || collectCurrentResultForPdf();

  if (!payload || (!payload.recognized_text && !payload.result_text)) {
    alert(uiSettings.siteLanguage === "en" ? "Run a voice command first" : "Сначала выполните голосовую команду");
    return;
  }

  try {
    const response = await fetch("/api/pdf/download", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error("PDF download error");

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "neuro_assistant_report.pdf";

    document.body.appendChild(link);
    link.click();

    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error(error);
    alert(uiSettings.siteLanguage === "en" ? "Failed to download PDF" : "Не удалось скачать PDF");
  }
}

function openHelpChat() {
  if (!helpChatPanel) return;

  helpChatPanel.classList.remove("hidden");

  setTimeout(() => {
    helpChatInput?.focus();
  }, 100);
}

function closeHelpChat() {
  if (!helpChatPanel) return;

  helpChatPanel.classList.add("hidden");
}

function toggleHelpChat() {
  if (!helpChatPanel) return;

  if (helpChatPanel.classList.contains("hidden")) {
    openHelpChat();
  } else {
    closeHelpChat();
  }
}

function formatHelpAnswerText(text) {
  const wakeWord = uiSettings.wakeWord || "помощник";

  return String(text || "")
    .replaceAll("{wake_word}", wakeWord)
    .replaceAll("Помощник,", `${wakeWord.charAt(0).toUpperCase() + wakeWord.slice(1)},`)
    .replaceAll("«Помощник", `«${wakeWord.charAt(0).toUpperCase() + wakeWord.slice(1)}`);
}

function appendHelpMessage(role, text) {
  if (!helpChatMessages) return;

  const message = document.createElement("div");
  message.className = `help-message ${role}`;

  const roleText = role === "user" ? "Вы" : "Ассистент";

  message.innerHTML = `
    <div class="help-message-role">${roleText}</div>
    <div class="help-message-text">${escapeHtml(formatHelpAnswerText(text))}</div>
  `;

  helpChatMessages.appendChild(message);
  helpChatMessages.scrollTop = helpChatMessages.scrollHeight;
}

async function sendHelpQuestion(questionText = null) {
  const question = String(questionText || helpChatInput?.value || "").trim();

  if (!question) return;

  openHelpChat();

  appendHelpMessage("user", question);

  if (helpChatInput) {
    helpChatInput.value = "";
  }

  const loadingMessage = document.createElement("div");
  loadingMessage.className = "help-message assistant";
  loadingMessage.innerHTML = `
    <div class="help-message-role">Ассистент</div>
    <div class="help-message-text">Ищу подсказку...</div>
  `;

  helpChatMessages.appendChild(loadingMessage);
  helpChatMessages.scrollTop = helpChatMessages.scrollHeight;

  try {
    const response = await fetch("/api/help/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Ошибка справочного чата");
    }

    loadingMessage.querySelector(".help-message-text").textContent =
      formatHelpAnswerText(data.answer || "Не удалось найти ответ.");
  } catch (error) {
    console.error(error);

    loadingMessage.querySelector(".help-message-text").textContent =
      "Не удалось получить ответ. Попробуйте спросить: «Какие команды доступны?»";
  }
}

recordBtn?.addEventListener("click", () => {
  if (!isRecording) {
    startRecording();
  } else {
    stopRecording();
  }
});

ollamaModeBtn?.addEventListener("click", () => {
  setLLMMode("ollama");
});

localModeBtn?.addEventListener("click", () => {
  setLLMMode("local_parser");
});

settingsOllamaModeBtn?.addEventListener("click", () => {
  setLLMMode("ollama");
});

settingsLocalModeBtn?.addEventListener("click", () => {
  setLLMMode("local_parser");
});

document.querySelectorAll(".nav-item").forEach((item) => {
  item.addEventListener("click", () => {
    const pageName = item.dataset.page || "dashboard";
    showPage(pageName);
  });
});

document.querySelectorAll("[data-open-page]").forEach((button) => {
  button.addEventListener("click", () => {
    const pageName = button.dataset.openPage;
    showPage(pageName);
  });
});

saveOllamaModelBtn?.addEventListener("click", () => {
  uiSettings.ollamaModel = ollamaModelInput.value || "qwen2.5:1.5b";
  saveUiSettings();
  alert(uiSettings.siteLanguage === "en" ? "Model name saved" : "Название модели сохранено");
});

fallbackToggle?.addEventListener("change", () => {
  uiSettings.fallbackEnabled = fallbackToggle.checked;
  saveUiSettings();
});

whisperModelSelect?.addEventListener("change", () => {
  uiSettings.whisperModel = whisperModelSelect.value;
  saveUiSettings();
});

speechLanguageSelect?.addEventListener("change", () => {
  uiSettings.speechLanguage = speechLanguageSelect.value;
  saveUiSettings();

  if (uiSettings.voiceActivationMode === "wake_word") {
    stopWakeWordRecognition();
    startWakeWordRecognition();
  }
});

voiceActivationModeSelect?.addEventListener("change", () => {
  uiSettings.voiceActivationMode = voiceActivationModeSelect.value;
  saveUiSettings();
  applyVoiceActivationMode();
});

wakeWordInput?.addEventListener("change", () => {
  uiSettings.wakeWord = wakeWordInput.value.trim() || "помощник";
  saveUiSettings();

  if (uiSettings.voiceActivationMode === "wake_word") {
    stopWakeWordRecognition();
    startWakeWordRecognition();
  }
});

siteLanguageSelect?.addEventListener("change", () => {
  uiSettings.siteLanguage = siteLanguageSelect.value;
  saveUiSettings();
  applyLocalization();
  applyUiSettingsToForm();
  loadDashboard();

  if (uiSettings.voiceActivationMode === "wake_word") {
    stopWakeWordRecognition();
    startWakeWordRecognition();
  }
});

siteThemeSelect?.addEventListener("change", () => {
  uiSettings.theme = siteThemeSelect.value;
  saveUiSettings();
  applyTheme();
});

detailedOutputToggle?.addEventListener("change", () => {
  uiSettings.detailedOutput = detailedOutputToggle.checked;
  saveUiSettings();
});

techInfoToggle?.addEventListener("change", () => {
  uiSettings.showTechInfo = techInfoToggle.checked;
  saveUiSettings();
  sourceBadge.style.display = uiSettings.showTechInfo ? "inline-block" : "none";
});

autoRefreshToggle?.addEventListener("change", () => {
  uiSettings.autoRefresh = autoRefreshToggle.checked;
  saveUiSettings();
  applyAutoRefresh();
});

refreshIntervalInput?.addEventListener("change", () => {
  uiSettings.refreshInterval = Number(refreshIntervalInput.value || 30);
  saveUiSettings();
  applyAutoRefresh();
});

saveHistoryToggle?.addEventListener("change", () => {
  uiSettings.saveHistory = saveHistoryToggle.checked;
  saveUiSettings();
});

confirmActionsToggle?.addEventListener("change", () => {
  uiSettings.confirmActions = confirmActionsToggle.checked;
  saveUiSettings();
});

defaultReportPeriodSelect?.addEventListener("change", () => {
  uiSettings.defaultReportPeriod = defaultReportPeriodSelect.value;
  saveUiSettings();
});

exportFormatSelect?.addEventListener("change", () => {
  uiSettings.exportFormat = exportFormatSelect.value;
  saveUiSettings();
});

confirmActionApplyBtn?.addEventListener("click", confirmPendingAction);
confirmActionCancelBtn?.addEventListener("click", cancelPendingAction);

clearHistoryBtn?.addEventListener("click", () => {
  clearCommandHistory({ askConfirmation: true });
});

downloadPdfBtn?.addEventListener("click", downloadLastCommandPdf);
buildChartBtn?.addEventListener("click", buildSalesChart);
manualCreateOrderBtn?.addEventListener("click", openManualCreateOrder);
manualCreateEmployeeBtn?.addEventListener("click", openManualCreateEmployee);
manualCreateSaleBtn?.addEventListener("click", openManualCreateSale);
manualCreateTaskBtn?.addEventListener("click", openManualCreateTask);
manualSendMailingBtn?.addEventListener("click", openManualSendMailing);
manualBuildChartBtn?.addEventListener("click", buildSalesChart);
manualDownloadPdfBtn?.addEventListener("click", downloadLastCommandPdf);
manualClearHistoryBtn?.addEventListener("click", () => clearCommandHistory());
manualOpenHelpBtn?.addEventListener("click", openHelpChat);

helpChatToggleBtn?.addEventListener("click", toggleHelpChat);
helpChatCloseBtn?.addEventListener("click", closeHelpChat);

helpChatSendBtn?.addEventListener("click", () => {
  sendHelpQuestion();
});

helpChatInput?.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    sendHelpQuestion();
  }
});

document.querySelectorAll(".help-quick-btn").forEach((button) => {
  button.addEventListener("click", () => {
    const question = button.dataset.helpQuestion;
    sendHelpQuestion(question);
  });
});

loadUiSettings();
loadLLMMode();
loadDashboard();
