# 🎯 Hướng dẫn sử dụng Frontend Todo App

## 📱 Truy cập ứng dụng

1. **Khởi động server** (nếu chưa chạy):
```bash
python main.py
```

2. **Mở browser** và truy cập:
```
http://localhost:8000
```

---

## 🔐 Bước 1: Đăng nhập / Đăng ký

### Đăng ký tài khoản mới

1. Khi vào trang lần đầu, bạn sẽ thấy form **Đăng nhập**
2. Click vào link **"Đăng ký ngay"** ở dưới form
3. Điền thông tin:
   - **Tên**: Tên hiển thị của bạn
   - **Email**: Email hợp lệ (ví dụ: user@example.com)
   - **Mật khẩu**: Tối thiểu 6 ký tự
4. Click nút **"Đăng ký"**
5. Nếu thành công, form sẽ tự động chuyển về **Đăng nhập** với email đã điền sẵn

### Đăng nhập

1. Nhập **Email** và **Mật khẩu**
2. Click nút **"Đăng nhập"**
3. Nếu thành công, bạn sẽ được chuyển đến trang Todo App

### Tài khoản có sẵn để test

**User thường:**
```
Email: test@example.com
Password: password123
```

**Admin:**
```
Email: admin@example.com
Password: admin123
```

---

## 📝 Bước 2: Quản lý công việc (Todos)

### Thêm công việc mới

1. Ở card **"Thêm công việc mới"** (màu trắng ở trên cùng):
   - **Tiêu đề**: Tên công việc (bắt buộc)
   - **Mô tả**: Chi tiết công việc (tùy chọn)
   - **Độ ưu tiên**: Chọn Thấp/Trung bình/Cao
   - **Hạn chót**: Chọn ngày và giờ (tùy chọn)

2. Click nút **"Thêm công việc"**

3. Công việc mới sẽ xuất hiện trong danh sách bên dưới

### Xem danh sách công việc

- Sau khi đăng nhập, tất cả công việc của bạn hiển thị dạng **cards**
- Mỗi card hiển thị:
  - ✅ Tiêu đề và mô tả
  - ✅ Badges trạng thái (Chưa làm/Đang làm/Hoàn thành)
  - ✅ Badge độ ưu tiên (Thấp/Trung bình/Cao)
  - ✅ Hạn chót và thời gian còn lại
  - ✅ Ngày tạo
  - ✅ Nút Sửa và Xóa

- **Card có viền màu** theo độ ưu tiên:
  - 🔴 **Đỏ**: Cao
  - 🟡 **Vàng**: Trung bình  
  - 🔵 **Xanh**: Thấp

### Sửa công việc

1. Click nút **"Sửa"** trên card công việc
2. Một popup (modal) sẽ hiện ra với thông tin hiện tại
3. Chỉnh sửa các thông tin:
   - Tiêu đề
   - Mô tả
   - **Trạng thái**: Chưa làm → Đang làm → Hoàn thành
   - Độ ưu tiên
   - Hạn chót
4. Click **"Lưu thay đổi"**
5. Hoặc click **"Hủy"** để đóng mà không lưu

### Xóa công việc

1. Click nút **"Xóa"** trên card công việc
2. Một hộp thoại xác nhận sẽ xuất hiện
3. Click **OK** để xóa hoặc **Cancel** để hủy
4. Sau khi xóa, công việc sẽ biến mất khỏi danh sách

---

## 🔍 Bước 3: Tìm kiếm và Lọc

### Tìm kiếm

1. Ở card **Filters** (ngay dưới form thêm todo)
2. Gõ từ khóa vào ô **"Tìm kiếm"**
3. Kết quả tự động hiển thị (không cần nhấn Enter)
4. Tìm kiếm trong cả **tiêu đề** và **mô tả**

### Lọc theo Trạng thái

1. Chọn dropdown **"Trạng thái"**:
   - **Tất cả**: Hiển thị tất cả
   - **Chưa làm**: Chỉ hiển thị công việc chưa bắt đầu
   - **Đang làm**: Đang thực hiện
   - **Hoàn thành**: Đã xong

### Lọc theo Độ ưu tiên

1. Chọn dropdown **"Độ ưu tiên"**:
   - **Tất cả**: Hiển thị tất cả
   - **Thấp**: Ưu tiên thấp
   - **Trung bình**: Ưu tiên vừa
   - **Cao**: Ưu tiên cao (quan trọng)

### Sắp xếp

1. **Sắp xếp theo**:
   - **Ngày tạo** (mặc định)
   - **Hạn chót**
   - **Độ ưu tiên**
   - **Trạng thái**

2. **Thứ tự**:
   - **Giảm dần** (mới nhất/cao nhất trước)
   - **Tăng dần** (cũ nhất/thấp nhất trước)

### Kết hợp nhiều filters

Bạn có thể kết hợp:
- Tìm kiếm + Lọc trạng thái + Lọc độ ưu tiên + Sắp xếp

Ví dụ: Tìm "mua" + Trạng thái "Chưa làm" + Ưu tiên "Cao" + Sắp xếp theo "Hạn chót"

---

## 👑 Bước 4: Admin Panel (Chỉ Admin)

### Truy cập Admin Panel

1. Đăng nhập với tài khoản **Admin**
2. Bạn sẽ thấy nút **"Admin"** màu tím ở góc phải header
3. Click nút **"Admin"**

### Xem thống kê hệ thống

Màn hình Admin hiển thị 5 thẻ thống kê:

1. **Tổng người dùng**: Số lượng tài khoản đã đăng ký
2. **Người dùng hoạt động**: Tài khoản chưa bị khóa
3. **Tổng công việc**: Tất cả todos trong hệ thống
4. **Đã hoàn thành**: Todos có trạng thái "Hoàn thành"
5. **Chưa hoàn thành**: Todos đang "Pending"

### Quản lý người dùng

Dưới phần thống kê là **"Quản lý người dùng"**:

#### Xem danh sách người dùng
- Hiển thị tất cả users (cả Admin và User thường)
- Mỗi user có:
  - Tên
  - Email
  - Badge "Admin" (nếu là admin)
  - Badge "Đã khóa" (nếu bị khóa)

#### Khóa người dùng
1. Tìm user cần khóa (không phải admin)
2. Click nút **"Khóa"** màu vàng
3. Xác nhận trong popup
4. User sẽ không thể đăng nhập nữa

#### Mở khóa người dùng
1. Tìm user đã bị khóa
2. Click nút **"Mở khóa"** màu xanh
3. User có thể đăng nhập lại

#### Xóa người dùng
1. Tìm user cần xóa (không phải admin)
2. Click nút **"Xóa"** màu đỏ
3. Xác nhận trong popup
4. ⚠️ **Cảnh báo**: Hành động này không thể hoàn tác!
5. User và tất cả todos của user sẽ bị xóa

#### Giới hạn
- ❌ **Không thể khóa** tài khoản Admin
- ❌ **Không thể xóa** tài khoản Admin
- ✅ Chỉ có thể quản lý User thường

### Quay lại Todos

Click nút **"Quay lại"** ở góc phải để trở về trang Todo

---

## 🔔 Thông báo (Toasts)

### Toast là gì?
- Thông báo nhỏ xuất hiện ở **góc trên bên phải**
- Tự động biến mất sau **3 giây**
- Hiển thị kết quả các hành động

### Các loại toast:

✅ **Success (Xanh lá)**
- "Đăng nhập thành công!"
- "Đã thêm công việc mới"
- "Đã cập nhật công việc"

❌ **Error (Đỏ)**
- "Đăng nhập thất bại"
- "Email đã tồn tại"
- "Không có quyền truy cập"

⚠️ **Warning (Vàng)**
- Các cảnh báo khác

ℹ️ **Info (Xanh dương)**
- Thông tin chung

---

## 🔄 Đăng xuất

1. Click nút **"Đăng xuất"** màu đỏ ở góc phải header
2. Token sẽ bị vô hiệu hóa (blacklist)
3. Tự động chuyển về trang đăng nhập
4. Không thể dùng token cũ nữa (bảo mật)

---

## 📱 Responsive Design

### Desktop (Màn hình lớn)
- Hiển thị đầy đủ
- Cards xếp theo grid 3-4 cột
- Filters nằm ngang

### Tablet (Màn hình vừa)
- Cards xếp 2 cột
- Filters vẫn nằm ngang

### Mobile (Điện thoại)
- Cards xếp 1 cột
- Filters xếp dọc
- Menu thu gọn
- Nút to hơn, dễ chạm

---

## 🎨 Màu sắc & Ý nghĩa

### Độ ưu tiên
- 🔴 **Cao (Đỏ)**: Cần làm gấp, quan trọng
- 🟡 **Trung bình (Vàng/Cam)**: Bình thường
- 🔵 **Thấp (Xanh)**: Không gấp

### Trạng thái
- ⚪ **Chưa làm (Xám)**: Mới tạo, chưa bắt đầu
- 🟡 **Đang làm (Vàng)**: Đang thực hiện
- 🟢 **Hoàn thành (Xanh lá)**: Đã xong

### Hạn chót
- 🟢 **Còn nhiều ngày**: Màu vàng nhạt
- 🟡 **Sắp hết hạn**: Màu vàng đậm
- 🔴 **Đã quá hạn**: Màu đỏ, hiện "Đã quá hạn"

---

## ⌨️ Keyboard Shortcuts (Không có)

Frontend này chưa có keyboard shortcuts. Sử dụng chuột hoặc touch.

---

## 💾 Lưu trữ dữ liệu

### LocalStorage
- **Token**: Được lưu trong browser
- Tự động đăng nhập lại nếu token còn hạn
- Xóa khi đăng xuất hoặc clear browser data

### Database (Backend)
- Tất cả todos lưu trên server
- Đồng bộ giữa các thiết bị nếu dùng cùng tài khoản

---

## 🐛 Xử lý lỗi thường gặp

### "Token không hợp lệ" / Tự động logout
- **Nguyên nhân**: Token hết hạn (30 phút)
- **Giải pháp**: Đăng nhập lại

### "Email đã tồn tại"
- **Nguyên nhân**: Email đã được đăng ký
- **Giải pháp**: Dùng email khác hoặc đăng nhập

### "Không có quyền truy cập"
- **Nguyên nhân**: Không phải admin hoặc không phải chủ todo
- **Giải pháp**: Chỉ sửa/xóa todo của bạn

### Trang trắng / Không load
- **Nguyên nhân**: Backend không chạy
- **Giải pháp**: Kiểm tra `python main.py` đang chạy

### CORS Error
- **Nguyên nhân**: Cấu hình CORS
- **Giải pháp**: Đã được xử lý trong code, không nên gặp

---

## 🎯 Tips & Tricks

### 1. Quản lý công việc hiệu quả
- Dùng **Độ ưu tiên** để đánh dấu việc quan trọng
- Đặt **Hạn chót** cho mọi việc
- Cập nhật **Trạng thái** thường xuyên
- Dùng **Tìm kiếm** để tìm nhanh

### 2. Filter thông minh
- Lọc "Chưa làm" + "Cao" để thấy việc gấp
- Sắp xếp theo "Hạn chót" để thấy việc sắp hết hạn
- Tìm kiếm để nhóm các việc liên quan

### 3. Admin
- Check thống kê thường xuyên
- Xóa user không hoạt động
- Khóa user vi phạm thay vì xóa (có thể mở lại)

### 4. Bảo mật
- Đăng xuất khi dùng máy công cộng
- Không share password
- Token tự hết hạn sau 30 phút

---

## 📞 Cần trợ giúp?

- 📖 Đọc **README.md** cho thông tin kỹ thuật
- 📖 Đọc **TEST_GUIDE.md** cho test scenarios
- 🌐 Truy cập **http://localhost:8000/docs** để xem API docs

---

**Chúc bạn quản lý công việc hiệu quả! 🎉📝**
