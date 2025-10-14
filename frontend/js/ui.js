// UI Service
class UIService {
    // Show/Hide loading
    showLoading() {
        document.getElementById('loadingOverlay').classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loadingOverlay').classList.add('hidden');
    }

    // Toast notifications
    showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = type === 'success' ? 'fa-check-circle' : 
                     type === 'error' ? 'fa-exclamation-circle' : 
                     type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle';
        
        toast.innerHTML = `
            <i class="fas ${icon} toast-icon"></i>
            <span class="toast-message">${message}</span>
        `;
        
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    // Format date
    formatDate(dateString) {
        if (!dateString) return 'Không có';
        const date = new Date(dateString);
        return date.toLocaleString('vi-VN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    // Format relative time
    formatRelativeTime(dateString) {
        if (!dateString) return '';
        
        const date = new Date(dateString);
        const now = new Date();
        const diff = date - now;
        
        if (diff < 0) {
            return '<span style="color: var(--danger-color);">Đã quá hạn</span>';
        }
        
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        if (days > 0) {
            return `<span style="color: var(--warning-color);">Còn ${days} ngày</span>`;
        }
        
        const hours = Math.floor(diff / (1000 * 60 * 60));
        return `<span style="color: var(--danger-color);">Còn ${hours} giờ</span>`;
    }

    // Render todo card
    renderTodoCard(todo) {
        return `
            <div class="todo-card priority-${todo.priority}" data-id="${todo.id}">
                <div class="todo-header">
                    <div>
                        <h3 class="todo-title">${this.escapeHtml(todo.title)}</h3>
                        <div class="todo-badges">
                            <span class="badge badge-status ${todo.status}">${STATUS_LABELS[todo.status]}</span>
                            <span class="badge badge-priority ${todo.priority}">${PRIORITY_LABELS[todo.priority]}</span>
                        </div>
                    </div>
                </div>
                
                ${todo.description ? `<p class="todo-description">${this.escapeHtml(todo.description)}</p>` : ''}
                
                <div class="todo-meta">
                    ${todo.due_date ? `
                        <div>
                            <i class="fas fa-calendar"></i>
                            Hạn: ${this.formatDate(todo.due_date)} ${this.formatRelativeTime(todo.due_date)}
                        </div>
                    ` : ''}
                    <div>
                        <i class="fas fa-clock"></i>
                        Tạo: ${this.formatDate(todo.created_at)}
                    </div>
                </div>
                
                <div class="todo-actions">
                    <button class="btn btn-sm btn-primary edit-todo" data-id="${todo.id}">
                        <i class="fas fa-edit"></i> Sửa
                    </button>
                    <button class="btn btn-sm btn-danger delete-todo" data-id="${todo.id}">
                        <i class="fas fa-trash"></i> Xóa
                    </button>
                </div>
            </div>
        `;
    }

    // Render todos list
    renderTodos(todos) {
        const container = document.getElementById('todosList');
        const countElement = document.getElementById('todoCount');
        
        countElement.textContent = `${todos.length} công việc`;
        
        if (todos.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-inbox"></i>
                    <h3>Chưa có công việc nào</h3>
                    <p>Hãy thêm công việc đầu tiên của bạn!</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = todos.map(todo => this.renderTodoCard(todo)).join('');
    }

    // Render user item
    renderUserItem(user) {
        const isAdmin = user.role === 'admin';
        const isActive = user.is_active;
        
        return `
            <div class="user-item">
                <div class="user-item-info">
                    <div class="user-item-name">
                        ${this.escapeHtml(user.name)}
                        ${isAdmin ? '<span class="badge badge-priority high">Admin</span>' : ''}
                        ${!isActive ? '<span class="badge badge-status pending">Đã khóa</span>' : ''}
                    </div>
                    <div class="user-item-email">${this.escapeHtml(user.email)}</div>
                </div>
                <div class="user-item-actions">
                    ${!isAdmin ? `
                        ${isActive ? `
                            <button class="btn btn-sm btn-warning block-user" data-id="${user.id}">
                                <i class="fas fa-ban"></i> Khóa
                            </button>
                        ` : `
                            <button class="btn btn-sm btn-success unblock-user" data-id="${user.id}">
                                <i class="fas fa-check"></i> Mở khóa
                            </button>
                        `}
                        <button class="btn btn-sm btn-danger delete-user" data-id="${user.id}">
                            <i class="fas fa-trash"></i> Xóa
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
    }

    // Render users list
    renderUsers(users) {
        const container = document.getElementById('usersList');
        
        if (users.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-users"></i>
                    <h3>Chưa có người dùng nào</h3>
                </div>
            `;
            return;
        }
        
        container.innerHTML = users.map(user => this.renderUserItem(user)).join('');
    }

    // Render stats
    renderStats(stats) {
        const container = document.getElementById('statsGrid');
        
        container.innerHTML = `
            <div class="stat-card">
                <div class="stat-icon users">
                    <i class="fas fa-users"></i>
                </div>
                <div class="stat-info">
                    <h3>${stats.total_users}</h3>
                    <p>Tổng người dùng</p>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon users">
                    <i class="fas fa-user-check"></i>
                </div>
                <div class="stat-info">
                    <h3>${stats.active_users}</h3>
                    <p>Người dùng hoạt động</p>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon todos">
                    <i class="fas fa-tasks"></i>
                </div>
                <div class="stat-info">
                    <h3>${stats.total_todos}</h3>
                    <p>Tổng công việc</p>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon completed">
                    <i class="fas fa-check-circle"></i>
                </div>
                <div class="stat-info">
                    <h3>${stats.completed_todos}</h3>
                    <p>Đã hoàn thành</p>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon pending">
                    <i class="fas fa-clock"></i>
                </div>
                <div class="stat-info">
                    <h3>${stats.pending_todos}</h3>
                    <p>Chưa hoàn thành</p>
                </div>
            </div>
        `;
    }

    // Escape HTML to prevent XSS
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Show/Hide sections
    showSection(sectionId) {
        document.querySelectorAll('.todo-section, .admin-section').forEach(section => {
            section.classList.add('hidden');
        });
        document.getElementById(sectionId).classList.remove('hidden');
    }

    // Show/Hide containers
    showAuthContainer() {
        document.getElementById('authContainer').classList.remove('hidden');
        document.getElementById('appContainer').classList.add('hidden');
    }

    showAppContainer() {
        document.getElementById('authContainer').classList.add('hidden');
        document.getElementById('appContainer').classList.remove('hidden');
    }

    // Toggle auth forms
    showLoginForm() {
        document.getElementById('loginForm').classList.remove('hidden');
        document.getElementById('registerForm').classList.add('hidden');
    }

    showRegisterForm() {
        document.getElementById('loginForm').classList.add('hidden');
        document.getElementById('registerForm').classList.remove('hidden');
    }
}

// Create global UI instance
const ui = new UIService();
