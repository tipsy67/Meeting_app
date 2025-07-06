// Telegram WebApp Mock и инициализация
const initTelegramWebApp = () => {
  if (!window.Telegram?.WebApp) {
    console.warn("Telegram WebApp not detected! Running in debug mode");
    window.Telegram = {
      WebApp: {
        initDataUnsafe: { user: { id: Math.floor(Math.random() * 10000) } },
        expand: () => console.debug("Telegram.WebApp.expand()"),
        showAlert: (msg) => console.warn(`ALERT: ${msg}`)
      }
    };
  }
  return window.Telegram.WebApp;
};

// Конфигурация API
const API_CONFIG = {
  BASE_URL: 'http://localhost:8000/users',
  ENDPOINTS: {
    set_user: '',
    get_speakers: '/speakers',
    add_to_speaker: '/add-to-speaker',
    get_listeners: '/listeners',
    save_lecture: '/save-lecture',
    get_lectures: '/open-lecture',
    delete_lectures: '/delete-lecture',
    get_listeners_from_lecture: '/listeners-from-lecture'
  },
  getUrl(endpoint) {
    return `${this.BASE_URL}${this.ENDPOINTS[endpoint]}`;
  }
};

// Инициализация приложения
const tg = initTelegramWebApp();
tg.expand();
const userId = tg.initDataUnsafe.user?.id;

// Кэш элементов DOM
const DOM = {
  mainMenu: document.getElementById('mainMenu'),
  newLectureForm: document.getElementById('newLectureForm'),
  lecturesList: document.getElementById('lecturesList'),
  editLectureMenu: document.getElementById('editLectureMenu'),
  listenersList: document.getElementById('listenersList'),
  lecturesContainer: document.getElementById('lecturesContainer'),
  lectureNameInput: document.getElementById('lectureName'),
  currentLectureTitle: document.getElementById('currentLectureTitle'),
  newLectureBtn: document.getElementById('newLectureBtn'),
  openLecturesBtn: document.getElementById('openLecturesBtn'),
  saveLectureBtn: document.getElementById('saveLectureBtn'),
  backFromNewLectureBtn: document.getElementById('backFromNewLectureBtn'),
  backFromLecturesBtn: document.getElementById('backFromLecturesBtn'),
  deleteLectureBtn: document.getElementById('deleteLectureBtn'),
  backFromEditBtn: document.getElementById('backFromEditBtn')
};

// Сервис API
const ApiService = {
  async request(endpoint, { method = 'GET', params = {}, data } = {}) {
    try {
      const url = new URL(API_CONFIG.getUrl(endpoint));
      Object.entries(params).forEach(([key, value]) => {
        url.searchParams.append(key, String(value));
      });

      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: data ? JSON.stringify(data) : undefined
      });

      if (!response.ok) {
        const error = await this.parseError(response);
        throw error;
      }
      return await response.json();
    } catch (error) {
      this.handleError(error);
      return null;
    }
  },

  async parseError(response) {
    try {
      const errorData = await response.json();
      return new Error(errorData.message || `HTTP ${response.status}`);
    } catch {
      return new Error(await response.text() || 'Unknown error');
    }
  },

  handleError(error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error('API Error:', error);
    tg.showAlert(`Ошибка: ${errorMessage}`);
  }
};

// Менеджер лекций
const LectureManager = {
  async fetchListeners() {
    try {
      const data = await ApiService.request('get_listeners', {
        params: { user_id: userId }
      });
      if (!data?.listeners) return;

      DOM.listenersList.innerHTML = data.listeners.map(listener => `
        <div class="list-group-item form-check">
          <input class="form-check-input" type="checkbox" 
                id="listener-${listener._id}">
          <label class="form-check-label" for="listener-${listener._id}">
            ${listener.name}
          </label>
        </div>
      `).join('');
    } catch (error) {
      console.error('Failed to fetch listeners:', error);
    }
  },

  async fetchLectures() {
    try {
      const data = await ApiService.request('get_lectures', {
        params: { user_id: userId }
      });
      if (!data?.lectures) return;

      DOM.lecturesContainer.innerHTML = data.lectures.map(lecture => `
        <div class="list-group-item lecture-card">
          <h5>${lecture.name}</h5>
          <button class="btn btn-sm btn-primary" 
                  data-lecture="${encodeURIComponent(lecture.name)}">
            Открыть
          </button>
        </div>
      `).join('');

      // Добавляем обработчики через делегирование событий
      DOM.lecturesContainer.addEventListener('click', (e) => {
        const button = e.target.closest('[data-lecture]');
        if (button) {
          this.openLecture(decodeURIComponent(button.dataset.lecture || ''));
        }
      });
    } catch (error) {
      console.error('Failed to fetch lectures:', error);
    }
  },

  openLecture(lectureName) {
    Navigation.show('editLectureMenu');
    DOM.currentLectureTitle.textContent = lectureName;
  },

  async saveLecture() {
    const lectureName = DOM.lectureNameInput.value.trim();
    if (!lectureName) {
      tg.showAlert('Введите название лекции!');
      DOM.lectureNameInput.classList.add('is-invalid');
      return;
    }
    DOM.lectureNameInput.classList.remove('is-invalid');

    const selectedListeners = Array.from(
      document.querySelectorAll('#listenersList input[type="checkbox"]:checked')
    ).map(checkbox => checkbox.id.replace('listener-', ''));

    const result = await ApiService.request('save_lecture', {
      method: 'POST',
      data: { userId, lectureName, listeners: selectedListeners }
    });

    if (result) {
      tg.showAlert('Лекция сохранена!');
      DOM.lectureNameInput.value = '';
      Navigation.show('mainMenu');
    }
  },

  async deleteLecture() {
    const lectureName = DOM.currentLectureTitle.textContent;
    const result = await ApiService.request('delete_lectures', {
      method: 'POST',
      data: { userId, lectureName }
    });

    if (result) {
      tg.showAlert('Лекция удалена!');
      await this.fetchLectures();
      Navigation.show('lecturesList');
    }
  }
};

// Навигация
const Navigation = {
  show(screen) {
    [DOM.mainMenu, DOM.newLectureForm, DOM.lecturesList, DOM.editLectureMenu].forEach(el => {
      el?.classList.add('hidden');
    });

    const currentScreen = {
      'mainMenu': DOM.mainMenu,
      'newLectureForm': DOM.newLectureForm,
      'lecturesList': DOM.lecturesList,
      'editLectureMenu': DOM.editLectureMenu
    }[screen];

    if (currentScreen) {
      currentScreen.classList.remove('hidden');
    }

    if (screen === 'newLectureForm') {
      LectureManager.fetchListeners().catch(console.error);
    }
    if (screen === 'lecturesList') {
      LectureManager.fetchLectures().catch(console.error);
    }
  }
};

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', () => {
  // Проверка, что все DOM элементы найдены
  Object.entries(DOM).forEach(([name, element]) => {
    if (!element && name !== 'currentLectureTitle') {
      console.error(`DOM element ${name} not found`);
    }
  });

  // Назначение обработчиков
  DOM.newLectureBtn?.addEventListener('click', () => Navigation.show('newLectureForm'));
  DOM.openLecturesBtn?.addEventListener('click', () => Navigation.show('lecturesList'));
  DOM.saveLectureBtn?.addEventListener('click', () => LectureManager.saveLecture().catch(console.error));
  DOM.backFromNewLectureBtn?.addEventListener('click', () => Navigation.show('mainMenu'));
  DOM.backFromLecturesBtn?.addEventListener('click', () => Navigation.show('mainMenu'));
  DOM.deleteLectureBtn?.addEventListener('click', () => LectureManager.deleteLecture().catch(console.error));
  DOM.backFromEditBtn?.addEventListener('click', () => Navigation.show('lecturesList'));

  // Показать главное меню по умолчанию
  Navigation.show('mainMenu');
});