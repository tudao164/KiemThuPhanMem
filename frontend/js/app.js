// Main App Controller
class TodoApp {
    constructor() {
        this.currentUser = null;
        this.currentTodoId = null;
        this.filters = {
            status: '',
            priority: '',
            search: '',
            sort_by: 'created_at',
            sort_order: 'desc'
        };
        
        this.init();
    }

    async init() {
        this.setupEventListeners();
        await this.checkAuth();
    }

    setupEventListeners() {
        // Auth form listeners
        document.getElementById('showRegister').addEventListener('click', (e) => {
            e.preventDefault();
            ui.showRegisterForm();
        });

        document.getElementById('showLogin').addEventListener('click', (e) => {
            e.preventDefault();
            ui.showLoginForm();
        });

        document.getElementById('loginFormElement').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        document.getElementById('registerFormElement').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleRegister();
        });

        // Logout
        document.getElementById('logoutBtn').addEventListener('click', () => {
            this.handleLogout();
        });

        // Add todo
        document.getElementById('addTodoForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleAddTodo();
        });

        // Filters
        document.getElementById('searchInput').addEventListener('input', (e) => {
            this.filters.search = e.target.value;
            this.debouncedLoadTodos();
        });

        document.getElementById('filterStatus').addEventListener('change', (e) => {
            this.filters.status = e.target.value;
            this.loadTodos();
        });

        document.getElementById('filterPriority').addEventListener('change', (e) => {
            this.filters.priority = e.target.value;
            this.loadTodos();
        });

        document.getElementById('sortBy').addEventListener('change', (e) => {
            this.filters.sort_by = e.target.value;
            this.loadTodos();
        });

        document.getElementById('sortOrder').addEventListener('change', (e) => {
            this.filters.sort_order = e.target.value;
            this.loadTodos();
        });

        // Todo actions (event delegation)
        document.getElementById('todosList').addEventListener('click', (e) => {
            const editBtn = e.target.closest('.edit-todo');
            const deleteBtn = e.target.closest('.delete-todo');

            if (editBtn) {
                const id = parseInt(editBtn.dataset.id);
                this.handleEditTodo(id);
            } else if (deleteBtn) {
                const id = parseInt(deleteBtn.dataset.id);
                this.handleDeleteTodo(id);
            }
        });

        // Edit modal
        document.getElementById('editTodoForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleUpdateTodo();
        });

        document.getElementById('closeEditModal').addEventListener('click', () => {
            this.closeEditModal();
        });

        document.getElementById('cancelEdit').addEventListener('click', () => {
            this.closeEditModal();
        });

        // Admin panel
        document.getElementById('adminPanelBtn').addEventListener('click', () => {
            this.showAdminPanel();
        });

        document.getElementById('backToTodos').addEventListener('click', () => {
            ui.showSection('todoSection');
        });

        // User actions (event delegation)
        document.getElementById('usersList').addEventListener('click', (e) => {
            const blockBtn = e.target.closest('.block-user');
            const unblockBtn = e.target.closest('.unblock-user');
            const deleteBtn = e.target.closest('.delete-user');

            if (blockBtn) {
                const id = parseInt(blockBtn.dataset.id);
                this.handleBlockUser(id);
            } else if (unblockBtn) {
                const id = parseInt(unblockBtn.dataset.id);
                this.handleUnblockUser(id);
            } else if (deleteBtn) {
                const id = parseInt(deleteBtn.dataset.id);
                this.handleDeleteUser(id);
            }
        });
    }

    // Debounce for search
    debouncedLoadTodos = this.debounce(() => this.loadTodos(), 500);

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Auth methods
    async checkAuth() {
        const token = api.getToken();
        
        if (!token) {
            ui.showAuthContainer();
            return;
        }

        try {
            ui.showLoading();
            this.currentUser = await api.getCurrentUser();
            this.showApp();
        } catch (error) {
            ui.showAuthContainer();
            ui.showToast('Phiên đăng nhập đã hết hạn', 'error');
            api.clearToken();
        } finally {
            ui.hideLoading();
        }
    }

    async handleLogin() {
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        try {
            ui.showLoading();
            await api.login({ email, password });
            this.currentUser = await api.getCurrentUser();
            ui.showToast('Đăng nhập thành công!', 'success');
            this.showApp();
        } catch (error) {
            ui.showToast(error.message || 'Đăng nhập thất bại', 'error');
        } finally {
            ui.hideLoading();
        }
    }

    async handleRegister() {
        const name = document.getElementById('registerName').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;

        try {
            ui.showLoading();
            await api.register({ name, email, password });
            ui.showToast('Đăng ký thành công! Hãy đăng nhập.', 'success');
            ui.showLoginForm();
            
            // Auto fill login form
            document.getElementById('loginEmail').value = email;
            document.getElementById('loginPassword').value = password;
        } catch (error) {
            ui.showToast(error.message || 'Đăng ký thất bại', 'error');
        } finally {
            ui.hideLoading();
        }
    }

    async handleLogout() {
        try {
            ui.showLoading();
            await api.logout();
            ui.showToast('Đã đăng xuất', 'success');
            ui.showAuthContainer();
            this.currentUser = null;
        } catch (error) {
            ui.showToast('Lỗi khi đăng xuất', 'error');
        } finally {
            ui.hideLoading();
        }
    }

    // App display
    showApp() {
        ui.showAppContainer();
        ui.showSection('todoSection');
        
        // Update user info
        document.getElementById('userName').innerHTML = 
            `<i class="fas fa-user"></i> ${ui.escapeHtml(this.currentUser.name)}`;
        
        // Show admin button if user is admin
        if (this.currentUser.role === 'admin') {
            document.getElementById('adminPanelBtn').classList.remove('hidden');
        } else {
            document.getElementById('adminPanelBtn').classList.add('hidden');
        }
        
        this.loadTodos();
    }

    // Todo methods
    async loadTodos() {
        try {
            ui.showLoading();
            const todos = await api.getTodos(this.filters);
            ui.renderTodos(todos);
        } catch (error) {
            ui.showToast('Lỗi khi tải danh sách công việc', 'error');
        } finally {
            ui.hideLoading();
        }
    }

    async handleAddTodo() {
        const title = document.getElementById('todoTitle').value;
        const description = document.getElementById('todoDescription').value;
        const priority = document.getElementById('todoPriority').value;
        const dueDate = document.getElementById('todoDueDate').value;

        const todoData = {
            title,
            description: description || null,
            priority,
            due_date: dueDate || null,
            status: 'pending'
        };

        try {
            ui.showLoading();
            await api.createTodo(todoData);
            ui.showToast('Đã thêm công việc mới', 'success');
            document.getElementById('addTodoForm').reset();
            await this.loadTodos();
        } catch (error) {
            ui.showToast(error.message || 'Lỗi khi thêm công việc', 'error');
        } finally {
            ui.hideLoading();
        }
    }

    async handleEditTodo(id) {
        try {
            ui.showLoading();
            const todos = await api.getTodos();
            const todo = todos.find(t => t.id === id);
            
            if (!todo) {
                ui.showToast('Không tìm thấy công việc', 'error');
                return;
            }

            this.currentTodoId = id;
            
            // Fill form
            document.getElementById('editTodoTitle').value = todo.title;
            document.getElementById('editTodoDescription').value = todo.description || '';
            document.getElementById('editTodoStatus').value = todo.status;
            document.getElementById('editTodoPriority').value = todo.priority;
            
            if (todo.due_date) {
                const date = new Date(todo.due_date);
                const localDateTime = new Date(date.getTime() - date.getTimezoneOffset() * 60000)
                    .toISOString()
                    .slice(0, 16);
                document.getElementById('editTodoDueDate').value = localDateTime;
            } else {
                document.getElementById('editTodoDueDate').value = '';
            }
            
            // Show modal
            document.getElementById('editModal').classList.remove('hidden');
        } catch (error) {
            ui.showToast('Lỗi khi tải thông tin công việc', 'error');
        } finally {
            ui.hideLoading();
        }
    }

    async handleUpdateTodo() {
        const title = document.getElementById('editTodoTitle').value;
        const description = document.getElementById('editTodoDescription').value;
        const status = document.getElementById('editTodoStatus').value;
        const priority = document.getElementById('editTodoPriority').value;
        const dueDate = document.getElementById('editTodoDueDate').value;

        const todoData = {
            title,
            description: description || null,
            status,
            priority,
            due_date: dueDate || null
        };

        try {
            ui.showLoading();
            await api.updateTodo(this.currentTodoId, todoData);
            ui.showToast('Đã cập nhật công việc', 'success');
            this.closeEditModal();
            await this.loadTodos();
        } catch (error) {
            ui.showToast(error.message || 'Lỗi khi cập nhật công việc', 'error');
        } finally {
            ui.hideLoading();
        }
    }

    async handleDeleteTodo(id) {
        if (!confirm('Bạn có chắc muốn xóa công việc này?')) {
            return;
        }

        try {
            ui.showLoading();
            await api.deleteTodo(id);
            ui.showToast('Đã xóa công việc', 'success');
            await this.loadTodos();
        } catch (error) {
            ui.showToast(error.message || 'Lỗi khi xóa công việc', 'error');
        } finally {
            ui.hideLoading();
        }
    }

    closeEditModal() {
        document.getElementById('editModal').classList.add('hidden');
        this.currentTodoId = null;
    }

    // Admin methods
    async showAdminPanel() {
        ui.showSection('adminSection');
        await this.loadAdminData();
    }

    async loadAdminData() {
        try {
            ui.showLoading();
            const [stats, users] = await Promise.all([
                api.getStats(),
                api.getUsers()
            ]);
            
            ui.renderStats(stats);
            ui.renderUsers(users);
        } catch (error) {
            ui.showToast('Lỗi khi tải dữ liệu admin', 'error');
        } finally {
            ui.hideLoading();
        }
    }

    async handleBlockUser(id) {
        if (!confirm('Bạn có chắc muốn khóa người dùng này?')) {
            return;
        }

        try {
            ui.showLoading();
            await api.blockUser(id);
            ui.showToast('Đã khóa người dùng', 'success');
            await this.loadAdminData();
        } catch (error) {
            ui.showToast(error.message || 'Lỗi khi khóa người dùng', 'error');
        } finally {
            ui.hideLoading();
        }
    }

    async handleUnblockUser(id) {
        try {
            ui.showLoading();
            await api.unblockUser(id);
            ui.showToast('Đã mở khóa người dùng', 'success');
            await this.loadAdminData();
        } catch (error) {
            ui.showToast(error.message || 'Lỗi khi mở khóa người dùng', 'error');
        } finally {
            ui.hideLoading();
        }
    }

    async handleDeleteUser(id) {
        if (!confirm('Bạn có chắc muốn xóa người dùng này? Hành động này không thể hoàn tác!')) {
            return;
        }

        try {
            ui.showLoading();
            await api.deleteUser(id);
            ui.showToast('Đã xóa người dùng', 'success');
            await this.loadAdminData();
        } catch (error) {
            ui.showToast(error.message || 'Lỗi khi xóa người dùng', 'error');
        } finally {
            ui.hideLoading();
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TodoApp();
});
