// Telegram WebApp Mock и инициализация
const initTelegramWebApp = () => {
    if (!window.Telegram?.WebApp) {
        console.warn("Telegram WebApp not detected! Running in debug mode");
        window.Telegram = {
            WebApp: {
                initDataUnsafe: {user: {id: Math.floor(Math.random() * 10000)}},
                expand: () => console.debug("Telegram.WebApp.expand()"),
                showAlert: (msg) => console.warn(`ALERT: ${msg}`)
            }
        };
    }
    return window.Telegram.WebApp;
};

// Конфигурация API
const API_CONFIG = {
    BASE_URL: 'https://ijqmrk-37-44-40-134.ru.tuna.am/users',
    ENDPOINTS: {
        set_user: '',
        get_speakers: '/speakers',
        get_selected_speakers: '/speakers-selected',
        add_to_speaker: '/add-to-speaker',
        get_listeners: '/listeners',
        save_lecture: '/save-lecture',
        get_lectures: '/open-lecture',
        delete_lectures: '/delete-lecture',
        get_listeners_from_lecture: '/listeners-from-lecture',
        remove_from_listeners: '/remove-from-listeners'
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
    appMainMenu: document.getElementById('appMainMenu'),
    speakerPanelBtn: document.getElementById('speakerPanelBtn'),
    listenerPanelBtn: document.getElementById('listenerPanelBtn'),
    subscriptionBtn: document.getElementById('subscriptionBtn'),
    helpBtn: document.getElementById('helpBtn'),
    listenerMenu: document.getElementById('listenerMenu'),
    joinSpeakerBtn: document.getElementById('joinSpeakerBtn'),
    leaveSpeakerBtn: document.getElementById('leaveSpeakerBtn'),
    backToMainMenuBtn: document.getElementById('backToMainMenuBtn'),
    backToMainMenuFromListenerBtn: document.getElementById('backToMainMenuFromListenerBtn'),
    joinSpeakerForm: document.getElementById('joinSpeakerForm'),
    leaveSpeakerForm: document.getElementById('leaveSpeakerForm'),
    speakersList: document.getElementById('speakersList'),
    speakersToLeaveList: document.getElementById('speakersToLeaveList'),
    confirmJoinSpeakerBtn: document.getElementById('confirmJoinSpeakerBtn'),
    confirmleaveSpeakerBtn: document.getElementById('confirmleaveSpeakerBtn'),
    backFromJoinSpeakerBtn: document.getElementById('backFromJoinSpeakerBtn'),
    backFromleaveSpeakerBtn: document.getElementById('backFromleaveSpeakerBtn'),
    mainMenu: document.getElementById('mainMenu'),
    newLectureForm: document.getElementById('newLectureForm'),
    lecturesList: document.getElementById('lecturesList'),
    editLectureMenu: document.getElementById('editLectureMenu'),
    listenersList: document.getElementById('listenersList'),
    lecturesContainer: document.getElementById('lecturesContainer'),
    lectureNameInput: document.getElementById('lectureName'),
    currentLectureTitle: document.getElementById('currentLectureTitle'),
    currentEditLectureTitle: document.getElementById('currentEditLectureTitle'),
    newLectureBtn: document.getElementById('newLectureBtn'),
    openLecturesBtn: document.getElementById('openLecturesBtn'),
    saveLectureBtn: document.getElementById('saveLectureBtn'),
    backFromNewLectureBtn: document.getElementById('backFromNewLectureBtn'),
    backFromLecturesBtn: document.getElementById('backFromLecturesBtn'),
    deleteLectureBtn: document.getElementById('deleteLectureBtn'),
    backFromEditBtn: document.getElementById('backFromEditBtn'),
    editListenersBtn: document.getElementById('editListenersBtn'),

};

// Сервис API
const ApiService = {
    async request(endpoint, {method = 'GET', params = {}, data} = {}) {
        try {
            const url = new URL(API_CONFIG.getUrl(endpoint));
            Object.entries(params).forEach(([key, value]) => {
                url.searchParams.append(key, String(value));
            });

            const response = await fetch(url, {
                method,
                headers: {'Content-Type': 'application/json'},
                body: data ? JSON.stringify(data) : undefined
            });

            if (!response.ok) {
                return this.handleError(await this.parseError(response));
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

const ListenerManager = {
    async fetchSpeakers() {
        try {
            const data = await ApiService.request('get_speakers');
            if (!data?.speakers) return;

            DOM.speakersList.innerHTML = data.speakers.map(speaker => `
        <div class="list-group-item d-flex align-items-center">
          <div class="form-check flex-grow-1">
            <input class="form-check-input" type="radio" name="speaker" 
                  id="speaker-${speaker._id}" value="${speaker._id}">
            <label class="form-check-label ms-2" for="speaker-${speaker._id}">
              ${speaker.username} ${speaker.full_name ? `(${speaker.full_name})` : ''}
            </label>
          </div>
        </div>
      `).join('');
        } catch (error) {
            console.error('Failed to fetch speakers:', error);
        }
    },

    async fetchMySpeakers() {
        try {
            const data = await ApiService.request('get_selected_speakers', {
                params: {listener_id: userId}
            });
            if (!data?.speakers) return;

            DOM.speakersToLeaveList.innerHTML = data.speakers.map(speaker => `
            <div class="list-group-item d-flex align-items-center">
                <div class="form-check flex-grow-1">
                    <input class="form-check-input" type="radio" 
                           name="speaker" 
                           id="speaker-${speaker._id}" 
                           value="${speaker._id}">
                    <label class="form-check-label ms-2" for="speaker-${speaker._id}">
                        ${speaker.username || 'No username'} 
                        (${speaker.full_name || 'No name'})
                    </label>
                </div>
            </div>
        `).join('');
        } catch (error) {
            console.error('Failed to fetch listener lectures:', error);
        }
    },

    async joinSpeaker() {
        const selectedSpeaker = document.querySelector('#speakersList input[name="speaker"]:checked');
        if (!selectedSpeaker) {
            tg.showAlert('Выберите лектора!');
            return;
        }

        const result = await ApiService.request('add_to_speaker', {
            method: 'POST',
            data: {listener_id: userId, speaker_id: selectedSpeaker.value}
        });
        if (result) {
            tg.showAlert('Вы успешно добавились к лектору!');
            Navigation.show('listenerMenu');
        }
    },

    async leaveSpeaker() {
        const selectedLecture = document.querySelector('#speakersToLeaveList input[name="speaker"]:checked');
        if (!selectedLecture) {
            tg.showAlert('Выберите лектора!');
            return;
        }

        const result = await ApiService.request('remove_from_listeners', {
            method: 'DELETE',
            params: {listener_id: userId, speaker_id: selectedLecture.value}
        });
        if (result) {
            tg.showAlert('Вы успешно отписались от лектора!');
            tg.showAlert(JSON.stringify(result.message));
            Navigation.show('listenerMenu');
        }
    }
};

// Менеджер лекций
const LectureManager = {
    async fetchListeners() {
        try {
            const data = await ApiService.request('get_listeners', {
                params: {speaker_id: userId}
            });
            if (!data?.listeners) return;

            DOM.listenersList.innerHTML = data.listeners.map(listener => `
      <div class="list-group-item d-flex align-items-center">
        <div class="form-check flex-grow-1">
          <input class="form-check-input" type="checkbox" 
                id="listener-${listener._id}">
          <label class="form-check-label ms-2" for="listener-${listener._id}">
            ${listener.username} ${listener.full_name ? `(${listener.full_name})` : ''}
          </label>
        </div>
      </div>
    `).join('');
        } catch (error) {
            console.error('Failed to fetch listeners:', error);
        }
    },

    async fetchLectures() {
        try {
            const data = await ApiService.request('get_lectures', {
                params: {user_id: userId}
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
        ).map(checkbox => parseInt(checkbox.id.replace('listener-', '')));

        const requestData = {
            name: `${userId}_${lectureName}`,
            data: selectedListeners.length > 0 ? selectedListeners : [0]
        };

        // tg.showAlert(JSON.stringify(requestData));

        const result = await ApiService.request('save_lecture', {
            method: 'POST',
            data: requestData
        });

        if (result) {
            tg.showAlert('Лекция сохранена!');
            DOM.lectureNameInput.value = '';
            Navigation.show('mainMenu');
        }
    },

    async deleteLecture() {
        const lectureName = DOM.currentLectureTitle.textContent;
        const requestData = {
            speaker_id: userId,
            name: lectureName
        }

        const result = await ApiService.request('delete_lectures', {
            method: 'DELETE',
            params: requestData
        });

        if (result) {
            tg.showAlert('Лекция удалена!');
            await this.fetchLectures();
            Navigation.show('lecturesList');
        }
    },

    async editLectureListeners() {
        // try {
        const lectureName = DOM.currentLectureTitle.textContent;

        // 1. Получаем текущих слушателей лекции
        const lectureData = await ApiService.request('get_listeners_from_lecture', {
            params: {
                name: lectureName,
                speaker_id: userId
            }
        });

        // 2. Получаем всех доступных слушателей
        const allListeners = await ApiService.request('get_listeners', {
            params: {speaker_id: userId}
        });

        if (!allListeners?.listeners) return;

        // 3. Отмечаем уже выбранных слушателей
        const currentListeners = lectureData?.listeners?.map(l => l._id) || [];

        // 4. Показываем форму редактирования
        DOM.listenersList.innerHTML = allListeners.listeners.map(listener => `
        <div class="list-group-item d-flex align-items-center">
          <div class="form-check flex-grow-1">
            <input class="form-check-input" type="checkbox" 
                  id="listener-${listener._id}"
                  ${currentListeners.includes(listener._id) ? 'checked' : ''}>
            <label class="form-check-label ms-2" for="listener-${listener._id}">
              ${listener.username} ${listener.full_name ? `(${listener.full_name})` : ''}
            </label>
          </div>
        </div>
      `).join('');

        // 5. Обновляем UI
        DOM.currentEditLectureTitle.textContent = `Редактирование: ${lectureName}`;
        DOM.lectureNameInput.value = lectureName
        Navigation.show('editLectureForm');
    }
};

const Navigation = {
    show(screen) {
        // Скрываем все экраны
        [
            DOM.appMainMenu, DOM.mainMenu, DOM.listenerMenu,
            DOM.joinSpeakerForm, DOM.leaveSpeakerForm,
            DOM.newLectureForm, DOM.lecturesList, DOM.editLectureMenu
        ].forEach(el => {
            el?.classList.add('hidden');
        });

        const currentScreen = {
            'appMainMenu': DOM.appMainMenu,
            'mainMenu': DOM.mainMenu,
            'listenerMenu': DOM.listenerMenu,
            'joinSpeakerForm': DOM.joinSpeakerForm,
            'leaveSpeakerForm': DOM.leaveSpeakerForm,
            'newLectureForm': DOM.newLectureForm,
            'editLectureForm': DOM.newLectureForm,
            'lecturesList': DOM.lecturesList,
            'editLectureMenu': DOM.editLectureMenu
        }[screen];

        if (currentScreen) {
            currentScreen.classList.remove('hidden');
        }

        // Инициализация экранов при показе
        if (screen === 'newLectureForm') {
            DOM.currentEditLectureTitle.textContent = `Новая лекция`;
            LectureManager.fetchListeners().catch(console.error);
        }
        if (screen === 'lecturesList') {
            LectureManager.fetchLectures().catch(console.error);
        }
        if (screen === 'joinSpeakerForm') {
            ListenerManager.fetchSpeakers().catch(console.error);
        }
        if (screen === 'leaveSpeakerForm') {
            ListenerManager.fetchMySpeakers().catch(console.error);
        }
    }
};

// Обновляем инициализацию обработчиков
document.addEventListener('DOMContentLoaded', () => {
    // Проверка DOM элементов
    Object.entries(DOM).forEach(([name, element]) => {
        if (!element && !name.startsWith('current')) {
            console.error(`DOM element ${name} not found`);
        }
    });

    // Главное меню
    DOM.speakerPanelBtn?.addEventListener('click', () => Navigation.show('mainMenu'));
    DOM.listenerPanelBtn?.addEventListener('click', () => Navigation.show('listenerMenu'));
    DOM.subscriptionBtn?.addEventListener('click', () => tg.showAlert('Функционал подписки в разработке'));
    DOM.helpBtn?.addEventListener('click', () => tg.showAlert('Помощь: используйте меню для навигации'));

    // Меню лектора
    DOM.newLectureBtn?.addEventListener('click', () => Navigation.show('newLectureForm'));
    DOM.openLecturesBtn?.addEventListener('click', () => Navigation.show('lecturesList'));
    DOM.backToMainMenuBtn?.addEventListener('click', () => Navigation.show('appMainMenu'));

    // Меню слушателя
    DOM.joinSpeakerBtn?.addEventListener('click', () => Navigation.show('joinSpeakerForm'));
    DOM.leaveSpeakerBtn?.addEventListener('click', () => Navigation.show('leaveSpeakerForm'));
    DOM.backToMainMenuFromListenerBtn?.addEventListener('click', () => Navigation.show('appMainMenu'));

    // Формы слушателя
    DOM.confirmJoinSpeakerBtn?.addEventListener('click', () => ListenerManager.joinSpeaker().catch(console.error));
    DOM.confirmleaveSpeakerBtn?.addEventListener('click', () => ListenerManager.leaveSpeaker().catch(console.error));
    DOM.backFromJoinSpeakerBtn?.addEventListener('click', () => Navigation.show('listenerMenu'));
    DOM.backFromleaveSpeakerBtn?.addEventListener('click', () => Navigation.show('listenerMenu'));

    // Существующие обработчики
    DOM.saveLectureBtn?.addEventListener('click', () => LectureManager.saveLecture().catch(console.error));
    DOM.backFromNewLectureBtn?.addEventListener('click', () => Navigation.show('mainMenu'));
    DOM.backFromLecturesBtn?.addEventListener('click', () => Navigation.show('mainMenu'));
    DOM.deleteLectureBtn?.addEventListener('click', () => LectureManager.deleteLecture().catch(console.error));
    DOM.backFromEditBtn?.addEventListener('click', () => Navigation.show('lecturesList'));
    DOM.editListenersBtn?.addEventListener('click', () => LectureManager.editLectureListeners().catch(console.error));

    // Показать главное меню приложения по умолчанию
    Navigation.show('appMainMenu');
});