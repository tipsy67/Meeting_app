const API_CONFIG = {
    BASE_URL: 'https://gb59jr-213-87-151-31.ru.tuna.am',
    ENDPOINTS: {
        login: '/auth/login',
        refresh: '/auth/refresh',

        set_user: '/users',
        get_speakers: '/users/speakers',
        add_to_speaker: '/users/speakers/listeners',

        get_listeners: '/users/listeners',
        get_selected_speakers: '/users/listeners/speakers',
        remove_from_listeners: '/users/listeners/speakers',

        save_lecture: '/lectures',
        get_lectures: '/lectures',
        delete_lectures: '/lectures',

        get_listeners_from_lecture: '/lectures/listeners',
        remove_from_all_lectures: '/lectures/listeners-unsubscribe',
        remove_from_lecture: '/lectures/listeners-unsubscribe-lecture',
        create_meeting: '/conferences/new'
    },
    getUrl(endpoint) {
        if (!this.ENDPOINTS[endpoint]) {
            throw new Error(`Unknown endpoint: ${endpoint}`);
        }
        return `${this.BASE_URL}${this.ENDPOINTS[endpoint]}`;
    }
};

// Инициализация Telegram WebApp
const initTelegramWebApp = () => {
    if (!window.Telegram?.WebApp) {
        console.warn("Telegram WebApp not detected! Running in debug mode");
        window.Telegram = {
            WebApp: {
                initData: 'debug_user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22Debug%22%2C%22last_name%22%3A%22User%22%2C%22username%22%3A%22debug_user%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D',
                expand: () => console.debug("Telegram.WebApp.expand()"),
                showAlert: (msg) => alert(`ALERT: ${msg}`),
                ready: (callback) => callback(),
                close: () => console.debug("WebApp closed"),
                isExpanded: true,
                colorScheme: 'light',
                version: '6.0',
                platform: 'unknown'
            }
        };
    }
    return window.Telegram.WebApp;
};

// Получение пользовательских данных
const getTelegramUserData = (webApp) => {
    if (!webApp?.initData) {
        console.warn("No initData in Telegram WebApp");
        return null;
    }

    try {
        const params = new URLSearchParams(webApp.initData);
        const userParam = params.get('user');
        if (!userParam) {
            console.warn("No user parameter in initData");
            return null;
        }
        return JSON.parse(decodeURIComponent(userParam));
    } catch (e) {
        console.error("Error parsing user data:", e);
        return null;
    }
};

// Инициализация приложения
const tg = initTelegramWebApp();
const userData = getTelegramUserData(tg);
const userId = userData?.id || null;

console.log('Telegram WebApp initialized:', tg);
console.log('User data:', userData);
console.log('User ID:', userId);

// JWT сервис
const JwtService = {
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,

    setTokens(tokenInfo) {
        if (!tokenInfo?.access_token) {
            throw new Error("Access token is required");
        }

        this.accessToken = tokenInfo.access_token;
        localStorage.setItem('accessToken', tokenInfo.access_token);

        if (tokenInfo.refresh_token !== undefined && tokenInfo.refresh_token !== null) {
            this.refreshToken = tokenInfo.refresh_token;
            localStorage.setItem('refreshToken', tokenInfo.refresh_token);
        }

        console.log('Tokens updated', {
            access: this.accessToken,
            refresh: this.refreshToken, // Используем текущее значение (новое или старое)
            tokenType: tokenInfo.token_type || 'Bearer'
        });
    },

    clearTokens() {
        this.accessToken = null;
        this.refreshToken = null;
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        console.log('Tokens cleared');
    },

    getAuthHeader() {
        return this.accessToken ? {
            'Authorization': `Bearer ${this.accessToken}`
        } : {};
    },

    async refresh() {
        if (!this.refreshToken) {
            console.log('No refresh token available');
            this.clearTokens();
            return false;
        }

        try {
            console.log('Attempting token refresh with token:', this.refreshToken);
            const response = await fetch(API_CONFIG.getUrl('refresh'), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.refreshToken}`
                }
            });

            console.log('Refresh response status:', response.status);

            if (response.ok) {
                const data = await response.json();
                console.log('Refresh successful, new tokens:', data);
                this.setTokens(data);
                return true;
            }

            console.log('Token refresh failed with status:', response.status);
            const errorText = await response.text();
            console.log('Refresh error response:', errorText);
            this.clearTokens();
            return false;
        } catch (error) {
            console.error('Refresh token failed:', error);
            this.clearTokens();
            return false;
        }
    }
};

// Auth сервис
const AuthService = {
    async login() {
        try {
            if (!tg.initData) {
                console.error('No initData available for login');
                tg.showAlert('Не удалось получить данные Telegram. Пожалуйста, перезагрузите приложение.');
                return false;
            }

            console.log('Attempting login with initData:', tg.initData);

            const response = await fetch(API_CONFIG.getUrl('login'), {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({initData: tg.initData})
            });

            console.log('Login response status:', response.status);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Login failed with status:', response.status, 'Error:', errorText);
                tg.showAlert('Ошибка входа. Пожалуйста, попробуйте снова.');
                return false;
            }

            const tokens = await response.json();
            console.log('Login successful, received tokens:', tokens);
            JwtService.setTokens(tokens);
            return true;
        } catch (error) {
            console.error('Authentication failed:', error);
            tg.showAlert('Ошибка соединения. Проверьте интернет и попробуйте снова.');
            return false;
        }
    },

    logout() {
        JwtService.clearTokens();
    },

    isAuthenticated() {
        return !!JwtService.accessToken;
    },

    async ensureAuth() {
        if (this.isAuthenticated()) {
            console.log('Already authenticated');
            return true;
        }

        console.log('Not authenticated, attempting login');
        return await this.login();
    }
};

// Сервис API
const ApiService = {
    async request(endpoint, {method = 'GET', params = {}, data} = {}) {
        console.log(`API request to ${endpoint}`, {method, params, data});

        // Для эндпоинтов login и refresh не проверяем авторизацию
        if (!['login', 'refresh'].includes(endpoint)) {
            // Проверяем наличие токена
            if (!JwtService.accessToken) {
                console.log('No access token, attempting login');
                if (!await AuthService.login()) {
                    throw new Error('Authentication required');
                }
            }
        }

        const url = new URL(API_CONFIG.getUrl(endpoint));
        Object.entries(params).forEach(([key, value]) => {
            url.searchParams.append(key, String(value));
        });

        try {
            console.log(`Making request to ${url.toString()}`);
            let response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    ...JwtService.getAuthHeader()
                },
                body: data ? JSON.stringify(data) : undefined
            });

            console.log(`Response status for ${endpoint}:`, response.status);

            // Если 401 - пробуем обновить токен только один раз
            if (response.status === 401) {
                console.log('Received 401, attempting token refresh');
                if (await JwtService.refresh()) {
                    console.log('Retrying request with new token');
                    response = await fetch(url, {
                        method,
                        headers: {
                            'Content-Type': 'application/json',
                            ...JwtService.getAuthHeader()
                        },
                        body: data ? JSON.stringify(data) : undefined
                    });

                    console.log(`Retry response status for ${endpoint}:`, response.status);
                } else {
                    throw new Error('Session expired');
                }
            }

            if (!response.ok) {
                throw await this.parseError(response);
            }

            const responseData = await response.json();
            console.log(`API response for ${endpoint}:`, responseData);
            return responseData;
        } catch (error) {
            console.error(`API request to ${endpoint} failed:`, error);
            this.handleError(error);
            throw error;
        }
    },

    async parseError(response) {
        try {
            const errorData = await response.json();
            return new Error(errorData.message || `HTTP ${response.status}`);
        } catch {
            const text = await response.text();
            return new Error(text || `HTTP ${response.status}`);
        }
    },

    handleError(error) {
        const message = error instanceof Error ? error.message : 'Unknown error';
        console.error('API Error:', error);
        tg.showAlert(`Ошибка: ${message}`);
    }
};

// DOM элементы
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
    newMeetingBtn: document.getElementById('newMeetingBtn'),
    newMeetingForm: document.getElementById('newMeetingForm'),
    meetingDateTime: document.getElementById('meetingDateTime'),
    confirmMeetingBtn: document.getElementById('confirmMeetingBtn'),
    backFromMeetingFormBtn: document.getElementById('backFromMeetingFormBtn'),
    currentMeetingLectureTitle: document.getElementById('currentMeetingLectureTitle'),
    lectureDuration: document.getElementById('lectureDuration'),
    editLectureForm: document.getElementById('editLectureForm'),
    editLectureTitle: document.getElementById('editLectureTitle'),
    editLectureNameInput: document.getElementById('editLectureName'),
    editListenersList: document.getElementById('editListenersList'),
    saveEditedLectureBtn: document.getElementById('saveEditedLectureBtn'),
    backFromEditLectureBtn: document.getElementById('backFromEditLectureBtn'),
    leaveLectureBtn: document.getElementById('leaveLectureBtn'),
    leaveLectureForm: document.getElementById('leaveLectureForm'),
    lecturesToLeaveList: document.getElementById('lecturesToLeaveList'),
    confirmLeaveLectureBtn: document.getElementById('confirmLeaveLectureBtn'),
    backFromLeaveLectureBtn: document.getElementById('backFromLeaveLectureBtn'),
};

// Менеджер слушателей
const ListenerManager = {
    async fetchMyLectures() {
        try {
            const data = await ApiService.request('get_lectures', {
                params: {listener_id: userId}
            });
            if (!data?.lectures) return;

            DOM.lecturesToLeaveList.innerHTML = data.lectures.map(lecture => `
            <div class="list-group-item d-flex align-items-center">
                <div class="form-check flex-grow-1">
                    <input class="form-check-input" type="radio" 
                           name="lecture" 
                           id="lecture-${lecture.id}" 
                           value="${lecture.id}_${lecture.name}">
                    <label class="form-check-label ms-2" for="lecture-${lecture.id}">
                        ${lecture.name || 'No name'}
                            <span class="text-muted small">@${lecture.speaker?.username || ''}
                            (${lecture.speaker?.first_name || ''} ${lecture.speaker?.last_name || ''} )</span>
                    </label>
                </div>
            </div>
        `).join('');
        } catch (error) {
            console.error('Failed to fetch listener lectures:', error);
            tg.showAlert('Ошибка загрузки ваших лекций');
        }
    },

    async leaveLecture() {
        try {
            const selectedLecture = document.querySelector('#lecturesToLeaveList input[name="lecture"]:checked');
            if (!selectedLecture) {
                tg.showAlert('Выберите лекцию!');
                return;
            }

            const result = await ApiService.request('remove_from_lecture', {
                method: 'DELETE',
                params: {listener_id: userId, lecture: selectedLecture.value}
            });

            if (result) {
                tg.showAlert('Вы успешно отписались от лекции!');
                Navigation.show('listenerMenu');
            }
        } catch (error) {
            console.error('Leave lecture error:', error);
            tg.showAlert('Ошибка отписки от лекции');
        }
    },
    async fetchSpeakers() {
        try {
            const [speakersData, selectedSpeakersData] = await Promise.all([
                ApiService.request('get_speakers'),
                ApiService.request('get_selected_speakers', {params: {listener_id: userId}})
            ]);

            if (!speakersData?.speakers) return;

            const selectedSpeakerIds = selectedSpeakersData?.speakers?.map(s => s.id) || [];

            DOM.speakersList.innerHTML = speakersData.speakers.map(speaker => {
                const isSelected = selectedSpeakerIds.includes(speaker.id);
                return `
                    <div class="list-group-item d-flex align-items-center">
                        <div class="form-check flex-grow-1">
                            <input class="form-check-input" type="radio" name="speaker" 
                                  id="speaker-${speaker.id}" value="${speaker.id}"
                                  ${isSelected ? 'disabled' : ''}>
                            <label class="form-check-label ms-2" for="speaker-${speaker.id}" 
                                  ${isSelected ? 'style="opacity: 0.5;"' : ''}>
                                ${speaker.username} ${speaker.full_name ? `(${speaker.full_name})` : ''}
                                ${isSelected ? ' ✅' : ''}
                            </label>
                        </div>
                    </div>
                `;
            }).join('');
        } catch (error) {
            console.error('Failed to fetch speakers:', error);
            tg.showAlert('Ошибка загрузки списка лекторов');
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
                               id="speaker-${speaker.id}" 
                               value="${speaker.id}">
                        <label class="form-check-label ms-2" for="speaker-${speaker.id}">
                            ${speaker.username || 'No username'} 
                            (${speaker.full_name || 'No name'})
                        </label>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Failed to fetch listener lectures:', error);
            tg.showAlert('Ошибка загрузки ваших лекторов');
        }
    },

    async joinSpeaker() {
        try {
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
        } catch (error) {
            console.error('Join speaker error:', error);
            tg.showAlert('Ошибка добавления к лектору');
        }
    },

    async leaveSpeaker() {
        try {
            const selectedSpeaker = document.querySelector('#speakersToLeaveList input[name="speaker"]:checked');
            if (!selectedSpeaker) {
                tg.showAlert('Выберите лектора!');
                return;
            }

            const result = await ApiService.request('remove_from_all_lectures', {
                method: 'DELETE',
                params: {listener_id: userId, speaker_id: selectedSpeaker.value}
            });

            if (result) {
                tg.showAlert('Вы успешно отписались от лектора!');
                Navigation.show('listenerMenu');
            }
        } catch (error) {
            console.error('Leave speaker error:', error);
            tg.showAlert('Ошибка отписки от лектора');
        }
    }
};

// Менеджер лекций
const LectureManager = {
    currentLectureName: '',

    async prepareEditForm() {
        try {
            const [lectureData, allListeners] = await Promise.all([
                ApiService.request('get_listeners_from_lecture', {
                    params: {name: this.currentLectureName, speaker_id: userId}
                }),
                ApiService.request('get_listeners', {params: {speaker_id: userId}})
            ]);

            if (!allListeners?.listeners) return;

            const currentListeners = lectureData?.listeners?.map(l => l.id) || [];

            DOM.editListenersList.innerHTML = allListeners.listeners.map(listener => `
                <div class="list-group-item d-flex align-items-center">
                    <div class="form-check flex-grow-1">
                        <input class="form-check-input" type="checkbox" 
                              id="edit-listener-${listener.id}"
                              ${currentListeners.includes(listener.id) ? 'checked' : ''}>
                        <label class="form-check-label ms-2" for="edit-listener-${listener.id}">
                            ${listener.username} ${listener.full_name ? `(${listener.full_name})` : ''}
                        </label>
                    </div>
                </div>
            `).join('');

            DOM.editLectureTitle.textContent = `Редактирование: ${this.currentLectureName}`;
            DOM.editLectureNameInput.value = this.currentLectureName.replace(`${userId}_`, '');
        } catch (error) {
            console.error('Prepare edit form error:', error);
            tg.showAlert('Ошибка подготовки формы редактирования');
        }
    },

    async saveEditedLecture() {
        try {
            const lectureName = DOM.editLectureNameInput.value.trim();
            if (!lectureName) {
                tg.showAlert('Введите название лекции!');
                DOM.editLectureNameInput.classList.add('is-invalid');
                return;
            }
            DOM.editLectureNameInput.classList.remove('is-invalid');

            const selectedListeners = Array.from(
                document.querySelectorAll('#editListenersList input[type="checkbox"]:checked')
            ).map(checkbox => parseInt(checkbox.id.replace('edit-listener-', '')));

            const result = await ApiService.request('save_lecture', {
                method: 'POST',
                data: {
                    name: `${userId}_${lectureName}`,
                    data: selectedListeners.length > 0 ? selectedListeners : [0]
                }
            });

            if (result) {
                tg.showAlert('Лекция обновлена!');
                this.currentLectureName = `${lectureName}`;
                DOM.currentLectureTitle.textContent = this.currentLectureName;
                await this.fetchLectures();
                Navigation.show('editLectureMenu');
            }
        } catch (error) {
            console.error('Save edited lecture error:', error);
            tg.showAlert('Ошибка сохранения лекции');
        }
    },

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
                              id="listener-${listener.id}">
                        <label class="form-check-label ms-2" for="listener-${listener.id}">
                            ${listener.username} ${listener.full_name ? `(${listener.full_name})` : ''}
                        </label>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Fetch listeners error:', error);
            tg.showAlert('Ошибка загрузки слушателей');
        }
    },

    async fetchLectures() {
        try {
            const data = await ApiService.request('get_lectures', {
                params: {speaker_id: userId}
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

            DOM.lecturesContainer.querySelectorAll('[data-lecture]').forEach(button => {
                button.addEventListener('click', () => {
                    this.openLecture(decodeURIComponent(button.dataset.lecture));
                });
            });
        } catch (error) {
            console.error('Fetch lectures error:', error);
            tg.showAlert('Ошибка загрузки лекций');
        }
    },

    openLecture(lectureName) {
        this.currentLectureName = lectureName;
        DOM.currentLectureTitle.textContent = lectureName;
        Navigation.show('editLectureMenu');
    },

    async saveLecture() {
        try {
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

            const result = await ApiService.request('save_lecture', {
                method: 'POST',
                data: {
                    name: `${userId}_${lectureName}`,
                    data: selectedListeners.length > 0 ? selectedListeners : [0]
                }
            });

            if (result) {
                tg.showAlert('Лекция сохранена!');
                DOM.lectureNameInput.value = '';
                Navigation.show('mainMenu');
            }
        } catch (error) {
            console.error('Save lecture error:', error);
            tg.showAlert('Ошибка сохранения лекции');
        }
    },

    async deleteLecture() {
        try {
            const lectureName = DOM.currentLectureTitle.textContent;
            const result = await ApiService.request('delete_lectures', {
                method: 'DELETE',
                params: {
                    speaker_id: userId,
                    name: lectureName
                }
            });

            if (result) {
                tg.showAlert('Лекция удалена!');
                await this.fetchLectures();
                Navigation.show('lecturesList');
            }
        } catch (error) {
            console.error('Delete lecture error:', error);
            tg.showAlert('Ошибка удаления лекции');
        }
    },

    initMeetingForm() {
        const lectureName = DOM.currentLectureTitle.textContent;
        DOM.currentMeetingLectureTitle.textContent = `Новая встреча: ${lectureName}`;

        const now = new Date();
        now.setMinutes(now.getMinutes() + 10);
        const formattedDateTime = now.toISOString().slice(0, 16);

        DOM.meetingDateTime.min = formattedDateTime;
        DOM.meetingDateTime.value = formattedDateTime;
        DOM.meetingDateTime.classList.remove('is-invalid');
        DOM.lectureDuration.classList.remove('is-invalid');
    },

    async createMeeting() {
        try {
            const selectedDateTime = new Date(DOM.meetingDateTime.value);
            const minDateTime = new Date();
            minDateTime.setMinutes(minDateTime.getMinutes() + 10);

            const duration = parseInt(DOM.lectureDuration.value) || 60;
            if (duration < 5 || duration > 180) {
                DOM.lectureDuration.classList.add('is-invalid');
                tg.showAlert('Длительность должна быть от 5 до 180 минут');
                return false;
            }
            if (!DOM.meetingDateTime.value || selectedDateTime < minDateTime) {
                DOM.meetingDateTime.classList.add('is-invalid');
                tg.showAlert('Выберите время не ранее чем через 10 минут');
                return false;
            }

            const result = await ApiService.request('create_meeting', {
                method: 'POST',
                data: {
                    lecture_name: DOM.currentLectureTitle.textContent,
                    speaker: userId,
                    start_datetime: selectedDateTime.toISOString(),
                    duration: duration,
                }
            });

            if (result) {
                tg.showAlert('Встреча успешно создана!');
                return true;
            }
        } catch (error) {
            console.error('Create meeting error:', error);
            tg.showAlert('Ошибка создания встречи');
        }
        return false;
    },

    editLectureListeners() {
        Navigation.show('editLectureForm');
    }
};

// Навигация
const Navigation = {
    screens: [
        'appMainMenu', 'mainMenu', 'listenerMenu',
        'joinSpeakerForm', 'leaveSpeakerForm', 'leaveLectureForm',
        'newLectureForm', 'lecturesList', 'editLectureMenu',
        'editLectureForm', 'newMeetingForm'
    ],

    show(screen) {
        if (!this.screens.includes(screen)) {
            console.error(`Unknown screen: ${screen}`);
            return;
        }

        // Скрываем все экраны
        this.screens.forEach(screenName => {
            const element = DOM[screenName];
            if (element) {
                element.classList.add('hidden');
            } else if (screenName !== 'currentMeetingLectureTitle') {
                console.warn(`DOM element ${screenName} not found`);
            }
        });

        // Показываем запрошенный экран
        if (DOM[screen]) {
            DOM[screen].classList.remove('hidden');
        } else {
            console.error(`Screen ${screen} not found in DOM`);
            return;
        }

        // Инициализация экрана
        switch (screen) {
            case 'newLectureForm':
                DOM.currentEditLectureTitle.textContent = 'Новая лекция';
                DOM.lectureNameInput.value = '';
                LectureManager.fetchListeners()
                    .catch(error => {
                        console.error('Error fetching listeners:', error);
                        tg.showAlert('Ошибка загрузки слушателей');
                    });
                break;
            case 'editLectureForm':
                LectureManager.prepareEditForm()
                    .catch(error => {
                        console.error('Error preparing edit form:', error);
                        tg.showAlert('Ошибка подготовки формы');
                    });
                break;
            case 'lecturesList':
                LectureManager.fetchLectures()
                    .catch(error => {
                        console.error('Error fetching lectures:', error);
                        tg.showAlert('Ошибка загрузки лекций');
                    });
                break;
            case 'joinSpeakerForm':
                ListenerManager.fetchSpeakers()
                    .catch(error => {
                        console.error('Error fetching speakers:', error);
                        tg.showAlert('Ошибка загрузки списка лекторов');
                    });
                break;
            case 'leaveSpeakerForm':
                ListenerManager.fetchMySpeakers()
                    .catch(error => {
                        console.error('Error fetching my speakers:', error);
                        tg.showAlert('Ошибка загрузки ваших лекторов');
                    });
                break;
            case 'newMeetingForm':
                LectureManager.initMeetingForm();
                break;
            case 'leaveLectureForm':
                ListenerManager.fetchMyLectures()
                    .catch(error => {
                        console.error('Error fetching my lectures:', error);
                        tg.showAlert('Ошибка загрузки ваших лекций');
                    });
                break;
        }
    }
};

// Инициализация приложения
document.addEventListener('DOMContentLoaded', async () => {
    console.log('App initializing...');

    // Инициализация Telegram WebApp
    tg.expand();
    tg.ready();

    try {
        console.log('Authentication process started');

        // 1. Проверяем наличие токенов
        const hasValidTokens = JwtService.accessToken && JwtService.refreshToken;
        console.log('Initial token state:', {
            accessToken: !!JwtService.accessToken,
            refreshToken: !!JwtService.refreshToken
        });

        // 2. Если токены есть, просто продолжаем (валидность проверится при первом запросе)
        if (hasValidTokens) {
            console.log('Found existing tokens, proceeding');
        }
        // 3. Если есть только refresh token, пробуем обновить
        else if (JwtService.refreshToken) {
            console.log('Attempting token refresh');
            if (!await JwtService.refresh()) {
                console.log('Token refresh failed, performing full login');
                await performLogin();
            }
        }
        // 4. Если токенов нет, делаем полный логин
        else {
            console.log('No tokens found, performing full login');
            await performLogin();
        }

        console.log('Authentication completed successfully');
        setupEventListeners();
        Navigation.show('appMainMenu');
    } catch (error) {
        console.error('Initialization failed:', error);
        AuthService.logout();
        tg.showAlert('Ошибка авторизации. Пожалуйста, перезагрузите страницу.');
    }

    async function performLogin() {
        console.log('Performing login...');
        if (!await AuthService.login()) {
            throw new Error('Login failed');
        }
        console.log('Login successful');
    }
});

function setupEventListeners() {
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
    DOM.confirmJoinSpeakerBtn?.addEventListener('click', () => ListenerManager.joinSpeaker());
    DOM.confirmleaveSpeakerBtn?.addEventListener('click', () => ListenerManager.leaveSpeaker());
    DOM.backFromJoinSpeakerBtn?.addEventListener('click', () => Navigation.show('listenerMenu'));
    DOM.backFromleaveSpeakerBtn?.addEventListener('click', () => Navigation.show('listenerMenu'));
    DOM.leaveLectureBtn?.addEventListener('click', () => Navigation.show('leaveLectureForm'));
    DOM.confirmLeaveLectureBtn?.addEventListener('click', () => ListenerManager.leaveLecture());
    DOM.backFromLeaveLectureBtn?.addEventListener('click', () => Navigation.show('listenerMenu'));

    // Лекции
    DOM.saveLectureBtn?.addEventListener('click', () => LectureManager.saveLecture());
    DOM.backFromNewLectureBtn?.addEventListener('click', () => Navigation.show('mainMenu'));
    DOM.backFromLecturesBtn?.addEventListener('click', () => Navigation.show('mainMenu'));
    DOM.deleteLectureBtn?.addEventListener('click', () => LectureManager.deleteLecture());
    DOM.backFromEditBtn?.addEventListener('click', () => Navigation.show('lecturesList'));
    DOM.editListenersBtn?.addEventListener('click', () => LectureManager.editLectureListeners());
    DOM.saveEditedLectureBtn?.addEventListener('click', () => LectureManager.saveEditedLecture());
    DOM.backFromEditLectureBtn?.addEventListener('click', () => Navigation.show('editLectureMenu'));

    // Встречи
    DOM.newMeetingBtn?.addEventListener('click', () => Navigation.show('newMeetingForm'));
    DOM.confirmMeetingBtn?.addEventListener('click', async () => {
        if (await LectureManager.createMeeting()) {
            Navigation.show('editLectureMenu');
        }
    });
    DOM.backFromMeetingFormBtn?.addEventListener('click', () => Navigation.show('editLectureMenu'));
}