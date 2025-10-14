// API Service
class APIService {
    constructor() {
        this.baseURL = API_CONFIG.BASE_URL;
        this.token = this.getToken();
    }

    getToken() {
        return localStorage.getItem(STORAGE_KEYS.TOKEN);
    }

    setToken(token) {
        localStorage.setItem(STORAGE_KEYS.TOKEN, token);
        this.token = token;
    }

    clearToken() {
        localStorage.removeItem(STORAGE_KEYS.TOKEN);
        localStorage.removeItem(STORAGE_KEYS.USER);
        this.token = null;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (this.token && !options.skipAuth) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Đã có lỗi xảy ra');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Auth APIs
    async register(userData) {
        return this.request(API_CONFIG.ENDPOINTS.REGISTER, {
            method: 'POST',
            body: JSON.stringify(userData),
            skipAuth: true
        });
    }

    async login(credentials) {
        const data = await this.request(API_CONFIG.ENDPOINTS.LOGIN, {
            method: 'POST',
            body: JSON.stringify(credentials),
            skipAuth: true
        });
        this.setToken(data.access_token);
        return data;
    }

    async logout() {
        try {
            await this.request(API_CONFIG.ENDPOINTS.LOGOUT, {
                method: 'POST'
            });
        } finally {
            this.clearToken();
        }
    }

    async getCurrentUser() {
        return this.request(API_CONFIG.ENDPOINTS.ME);
    }

    // Todo APIs
    async getTodos(filters = {}) {
        const params = new URLSearchParams();
        
        if (filters.status) params.append('status', filters.status);
        if (filters.priority) params.append('priority', filters.priority);
        if (filters.search) params.append('search', filters.search);
        if (filters.sort_by) params.append('sort_by', filters.sort_by);
        if (filters.sort_order) params.append('sort_order', filters.sort_order);

        const queryString = params.toString();
        const endpoint = queryString 
            ? `${API_CONFIG.ENDPOINTS.TODOS}?${queryString}`
            : API_CONFIG.ENDPOINTS.TODOS;

        return this.request(endpoint);
    }

    async createTodo(todoData) {
        return this.request(API_CONFIG.ENDPOINTS.TODOS, {
            method: 'POST',
            body: JSON.stringify(todoData)
        });
    }

    async updateTodo(id, todoData) {
        return this.request(API_CONFIG.ENDPOINTS.TODO_BY_ID(id), {
            method: 'PUT',
            body: JSON.stringify(todoData)
        });
    }

    async deleteTodo(id) {
        return this.request(API_CONFIG.ENDPOINTS.TODO_BY_ID(id), {
            method: 'DELETE'
        });
    }

    // Admin APIs
    async getUsers() {
        return this.request(API_CONFIG.ENDPOINTS.ADMIN_USERS);
    }

    async getStats() {
        return this.request(API_CONFIG.ENDPOINTS.ADMIN_STATS);
    }

    async blockUser(id) {
        return this.request(API_CONFIG.ENDPOINTS.ADMIN_BLOCK_USER(id), {
            method: 'PUT'
        });
    }

    async unblockUser(id) {
        return this.request(API_CONFIG.ENDPOINTS.ADMIN_UNBLOCK_USER(id), {
            method: 'PUT'
        });
    }

    async deleteUser(id) {
        return this.request(API_CONFIG.ENDPOINTS.ADMIN_DELETE_USER(id), {
            method: 'DELETE'
        });
    }
}

// Create global API instance
const api = new APIService();
