# Frontend Todo App

## Tính năng

### 🔐 Authentication
- ✅ Đăng ký tài khoản mới
- ✅ Đăng nhập với email/password
- ✅ Đăng xuất (token blacklist)
- ✅ Auto-login khi có token hợp lệ

### 📝 Todo Management
- ✅ Thêm công việc mới
  - Tiêu đề, mô tả, hạn chót, độ ưu tiên
- ✅ Xem danh sách công việc
  - Card layout với màu sắc theo độ ưu tiên
  - Hiển thị trạng thái, hạn chót, thời gian còn lại
- ✅ Sửa công việc
  - Modal popup để chỉnh sửa
  - Cập nhật trạng thái, độ ưu tiên
- ✅ Xóa công việc
  - Confirm trước khi xóa

### 🔍 Filter & Search
- ✅ Tìm kiếm trong tiêu đề và mô tả (realtime)
- ✅ Lọc theo trạng thái (Chưa làm, Đang làm, Hoàn thành)
- ✅ Lọc theo độ ưu tiên (Thấp, Trung bình, Cao)
- ✅ Sắp xếp theo nhiều tiêu chí
  - Ngày tạo, Hạn chót, Độ ưu tiên, Trạng thái
- ✅ Sắp xếp tăng dần/giảm dần

### 👑 Admin Panel (Chỉ Admin)
- ✅ Thống kê hệ thống
  - Tổng người dùng, người dùng hoạt động
  - Tổng công việc, đã hoàn thành, chưa hoàn thành
- ✅ Quản lý người dùng
  - Xem danh sách tất cả users
  - Khóa/Mở khóa người dùng
  - Xóa người dùng (không thể xóa admin)

### 🎨 UI/UX Features
- ✅ Responsive design (Mobile, Tablet, Desktop)
- ✅ Gradient background đẹp mắt
- ✅ Card layout hiện đại
- ✅ Toast notifications (success, error, warning)
- ✅ Loading overlay
- ✅ Modal popups
- ✅ Icon đẹp với Font Awesome
- ✅ Smooth animations
- ✅ Color-coded priorities
- ✅ Status badges
- ✅ Empty states

## Tech Stack

- **HTML5** - Semantic markup
- **CSS3** - Modern styling, Grid, Flexbox, Animations
- **Vanilla JavaScript** - ES6+, Classes, Async/Await
- **Font Awesome 6** - Icons
- **Local Storage** - Token persistence
- **Fetch API** - HTTP requests

## Kiến trúc Code

### Separation of Concerns

```
frontend/
├── index.html          # Main HTML structure
├── css/
│   └── styles.css      # All styling
└── js/
    ├── config.js       # Configuration & constants
    ├── api.js          # API service (all HTTP requests)
    ├── ui.js           # UI service (rendering, DOM manipulation)
    └── app.js          # Main app controller (business logic)
```

### Design Patterns

1. **Service Pattern**: API và UI được tách thành services riêng
2. **MVC-like**: app.js là controller, ui.js là view, api.js là model
3. **Event Delegation**: Efficient event handling
4. **Debouncing**: Search optimization
5. **Singleton**: Global instances của api, ui

## API Integration

### Authentication Flow
```javascript
// Register
api.register({ name, email, password })

// Login
api.login({ email, password })
// → Token được lưu vào localStorage
// → Auto-add vào headers cho requests tiếp theo

// Logout
api.logout()
// → Token được xóa khỏi localStorage
```

### Todo Operations
```javascript
// Get todos with filters
api.getTodos({ 
    status: 'pending', 
    priority: 'high',
    search: 'buy',
    sort_by: 'due_date',
    sort_order: 'asc'
})

// Create todo
api.createTodo({ title, description, due_date, priority })

// Update todo
api.updateTodo(id, { status: 'completed' })

// Delete todo
api.deleteTodo(id)
```

### Admin Operations
```javascript
// Get stats
api.getStats()

// Get all users
api.getUsers()

// Block/Unblock user
api.blockUser(id)
api.unblockUser(id)

// Delete user
api.deleteUser(id)
```

## Sử dụng

### 1. Start Backend
```bash
cd d:\KiemThuPhanMem
python main.py
```

### 2. Truy cập Frontend
Mở browser và truy cập:
```
http://localhost:8000
```

### 3. Đăng ký/Đăng nhập
- Trang đầu tiên sẽ là form đăng nhập
- Click "Đăng ký ngay" để tạo tài khoản mới
- Sau khi đăng ký, tự động chuyển về form đăng nhập với email đã điền sẵn

### 4. Sử dụng Todo App
- **Thêm công việc**: Điền form ở trên cùng
- **Xem danh sách**: Tự động load sau khi đăng nhập
- **Tìm kiếm**: Gõ vào ô tìm kiếm (tự động tìm)
- **Lọc**: Chọn filters bên dưới
- **Sửa**: Click nút "Sửa" trên todo card
- **Xóa**: Click nút "Xóa" (có confirm)

### 5. Admin Panel (Chỉ Admin)
- Đăng nhập với tài khoản admin
- Click nút "Admin" ở header
- Xem stats và quản lý users

## Credentials mặc định

### User thường
```
Email: test@example.com
Password: password123
```

### Admin
```
Email: admin@example.com
Password: admin123
```

## Responsive Breakpoints

- **Desktop**: > 768px
  - Multi-column grid layout
  - Full filters bar
  
- **Tablet**: 481px - 768px
  - 2-column grid
  - Stacked filters
  
- **Mobile**: ≤ 480px
  - Single column
  - Vertical navigation
  - Simplified layout

## Browser Support

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)

## Features Highlights

### Auto-refresh Token
- Token được lưu trong localStorage
- Auto-include trong headers của mọi API request
- Auto-redirect về login khi token expired

### Real-time Search
- Debounced search (500ms)
- Search trong cả title và description
- Không cần click nút search

### Smart Date Display
- Format ngày theo locale Việt Nam
- Hiển thị thời gian còn lại (Còn X ngày/giờ)
- Highlight khi quá hạn (màu đỏ)

### Color-coded Priorities
- **Cao** (High): Đỏ
- **Trung bình** (Medium): Vàng/Cam
- **Thấp** (Low): Xanh

### Status Badges
- **Chưa làm** (Pending): Xám
- **Đang làm** (In Progress): Vàng
- **Hoàn thành** (Completed): Xanh lá

### Toast Notifications
- Auto-dismiss sau 3 giây
- Color-coded theo type
- Smooth animations
- Stack multiple toasts

## Security

- ✅ XSS Protection: HTML escaping
- ✅ Token in localStorage (not in cookies)
- ✅ HTTPS recommended for production
- ✅ Token blacklist on logout

## Performance

- ✅ Debounced search
- ✅ Event delegation
- ✅ Minimal DOM manipulation
- ✅ CSS animations (GPU accelerated)
- ✅ Lazy loading data

## Customization

### Colors
Edit CSS variables in `styles.css`:
```css
:root {
    --primary-color: #4f46e5;
    --success-color: #10b981;
    --danger-color: #ef4444;
    /* ... */
}
```

### API URL
Edit in `config.js`:
```javascript
const API_CONFIG = {
    BASE_URL: 'http://localhost:8000',
    /* ... */
};
```

## Troubleshooting

### CORS Error
- Đảm bảo backend có CORS middleware
- Check `allow_origins` in main.py

### Token Expired
- Token có thời hạn 30 phút
- Tự động redirect về login
- Đăng nhập lại để lấy token mới

### Static Files Not Loading
- Đảm bảo aiofiles đã được cài
- Check path trong main.py
- Restart server

## Future Enhancements

- [ ] Dark mode
- [ ] Drag & drop todo ordering
- [ ] Todo categories/tags
- [ ] File attachments
- [ ] Export to PDF/CSV
- [ ] Push notifications
- [ ] Collaborative todos
- [ ] Activity log
- [ ] Recurring todos
- [ ] Todo templates

## Screenshots

### Login/Register
![Login](screenshots/login.png)

### Todo List
![Todos](screenshots/todos.png)

### Admin Panel
![Admin](screenshots/admin.png)

---

**Enjoy managing your todos! 🎉**
