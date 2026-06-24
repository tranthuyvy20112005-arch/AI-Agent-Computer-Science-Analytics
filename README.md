# 🌸 Strategic AI Agent Analytics - Khối Ngành Khoa Học Máy Tính

## 🎓 Thông Tin Sinh Viên
* **Họ và tên:** Trần Thúy Vy 🎀
* **Mã số sinh viên:** 030239230297
* **Chuyên ngành:** Khoa học Dữ liệu trong Kinh doanh
* **Trường:** Đại học Ngân hàng TP.Hồ Chí Minh (HUB)
* **Môn học:** Trực quan hóa dữ liệu 

---

## 📝 Giới Thiệu Đề Tài
Dự án tập trung vào việc **Phân tích định lượng và Khuyến nghị chiến lược triển khai hệ thống AI Agent** phục vụ riêng cho 9 phân khúc vị trí cốt lõi thuộc lĩnh vực Khoa học máy tính (KHMT). Nghiên cứu sử dụng phương pháp luận tiếp cận dữ liệu thực định (Empirical Data) để tối ưu hóa hiệu suất tài chính và giải phóng thặng dư chất xám cho doanh nghiệp.

### 🛠️ Công cụ triển khai:
* **Nguồn dữ liệu:** Bộ dữ liệu chuẩn WorkBank (Bao gồm các chiều dữ liệu: Tác vụ công việc, khảo sát tâm lý lao động và đánh giá của chuyên gia công nghệ).
* **Nền tảng giao diện:** Streamlit Dashboard (Pastel Soft-Tech Style).

---

## 📊 Các Tính Năng Đột Phá Trên Dashboard
1. **Tab 1 - Bản đồ Thị trường & Chỉ số Ma sát:** Trực quan hóa tương quan Thu nhập - Quy mô dòng tiền bằng mô hình Bong bóng và tính toán động **Chỉ số ma sát công nghệ (Friction Score)** nhằm phát hiện điểm nghẽn cổ chai của doanh nghiệp.
2. **Tab 2 - Tâm lý học & Giả lập Tài chính ROI:** Điều tra sâu phản ứng/nỗi sợ hãi của nhân sự đối với AI. Đồng thời tích hợp **Mô hình giả lập ROI số giờ giải phóng và dòng tiền tối ưu** theo thời gian thực (Real-time Financial Simulation).
3. **Tab 3 - Bản thiết kế Phân rã Tác vụ:** Chuyển đổi mô hình quản trị tĩnh sang mô hình phân lớp động 3 tầng quy trình (Hệ thống tự trị, Hệ thống cộng sinh, và Hệ thống đặc quyền của con người).

---

## 🚀 Hướng Dẫn Khởi Chạy Ứng Dụng Cục Bộ (Local Run)

Để khởi chạy ứng dụng trên máy tính cá nhân, vui lòng thực hiện theo các bước lệnh sau:

```bash
# 1. Cài đặt các thư viện phụ thuộc có sẵn trong requirements.txt
pip install -r requirements.txt

# 2. Khởi chạy Server Streamlit để mở giao diện Web
streamlit run app.py
