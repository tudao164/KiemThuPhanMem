// API Configuration
const API_CONFIG = {
    BASE_URL: 'http://localhost:8000',
    ENDPOINTS: {
        // Auth
        REGISTER: '/api/auth/register',
        LOGIN: '/api/auth/login',
        LOGOUT: '/api/auth/logout',
        ME: '/api/auth/me',
        
        // Todos
        TODOS: '/api/todos',
        TODO_BY_ID: (id) => `/api/todos/${id}`,
        
        // Admin
        ADMIN_USERS: '/api/admin/users',
        ADMIN_STATS: '/api/admin/stats',
        ADMIN_BLOCK_USER: (id) => `/api/admin/users/${id}/block`,
        ADMIN_UNBLOCK_USER: (id) => `/api/admin/users/${id}/unblock`,
        ADMIN_DELETE_USER: (id) => `/api/admin/users/${id}`
    }
};

// Storage keys
const STORAGE_KEYS = {
    TOKEN: 'todo_app_token',
    USER: 'todo_app_user'
};

// Status translations
const STATUS_LABELS = {
    pending: 'Chưa làm',
    in_progress: 'Đang làm',
    completed: 'Hoàn thành'
};

const PRIORITY_LABELS = {
    low: 'Thấp',
    medium: 'Trung bình',
    high: 'Cao'
};
