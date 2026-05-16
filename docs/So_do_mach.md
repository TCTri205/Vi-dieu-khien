# KẾ HOẠCH DỰ ÁN NHÀ THÔNG MINH - AI & IoT

**Nền tảng:** Raspberry Pi 4 | **Ngôn ngữ:** Python | **AI:** Nhận diện khuôn mặt

## 1. Yêu Cầu Nguồn Điện (Cực kỳ quan trọng)

Vì hệ thống có sự chênh lệch điện áp, bạn PHẢI phân chia nguồn như sau để không làm cháy Raspberry Pi:

- **Nguồn 1 (Cho bộ não):** Cục sạc điện thoại chân Type-C (yêu cầu đầu ra **5V - 2A** hoặc **5V - 3A** trở lên) cắm trực tiếp vào Raspberry Pi 4. (Tuyệt đối không cắm điện tường 220V trực tiếp).
    
- **Nguồn 2 (Cho cơ bắp):** Khay pin 4x AA (6V) sẽ cấp nguồn ĐỘC LẬP cho Động cơ Servo (Cửa) và Mạch tải của Relay (Quạt).
    
- **QUY TẮC SỐ 1 (GND CHUNG):** Bạn bắt buộc phải nối 1 sợi dây từ cực Âm (-) của khay pin vào chân GND của Raspberry Pi. Nếu không có dây "Mass chung" này, tín hiệu điều khiển sẽ bị nhiễu và hệ thống không hoạt động.
    

## 2. Sơ Đồ Nối Dây Chi Tiết (Wiring)

Hãy chuẩn bị Breadboard và nối từ từ theo danh sách sau:

### A. Động cơ Servo SG90 (Cửa tự động)

- **Dây Đỏ (VCC):** Nối vào cực Dương (+) của khay pin 6V. _(Servo chạy 6V rất khỏe)_.
    
- **Dây Nâu (GND):** Nối vào cực Âm (-) của khay pin (Mass chung).
    
- **Dây Cam (Tín hiệu):** Nối vào chân **GPIO 5** (Chân vật lý 29) của Pi.
    

### B. Module Relay 1 kênh & Quạt mini

- **Cấp nguồn và tín hiệu cho Relay (Bên mạch điều khiển):**
    
    - **Chân VCC (Relay):** Nối vào chân **5V** của Pi.
        
    - **Chân GND (Relay):** Nối vào Mass chung.
        
    - **Chân IN (Relay):** Nối vào chân **GPIO 27** của Pi.
        
- **Nối Quạt qua Relay (Bên mạch chịu tải tải):**
    
    - Nối cực Âm (-) của Quạt vào Mass chung (cực âm của khay pin).
        
    - Nối cực Dương (+) của Quạt vào chân **NO** (Normally Open) của Relay.
        
    - Nối chân **COM** của Relay vào cực Dương (+) của khay pin 6V.
        

### C. Đèn LED (Trong nhà)

- **Chân dài (+):** Nối qua 1 con điện trở (220Ω hoặc 330Ω) rồi cắm vào chân **GPIO 17** của Pi.
    
- **Chân ngắn (-):** Nối vào Mass chung.
    

### D. Cảm biến Siêu âm (HY-SRF05) ⚠️ LƯU Ý RỦI RO CHÁY MẠCH

Cảm biến này có 5 chân, cách nối tương tự HC-SR04 nhưng bỏ trống chân OUT:

- **VCC:** Nối vào chân **5V** của Pi.
    
- **GND:** Nối vào Mass chung.
    
- **Trig:** Nối vào chân **GPIO 23** của Pi.
    
- **OUT:** Bỏ trống (Không cắm dây).
    
- **Echo:** ⚠️ **DỪNG LẠI!** Chân Echo trả về điện áp 5V, nhưng chân GPIO của Pi chỉ chịu được tối đa 3.3V. Cắm trực tiếp có thể cháy Pi.
    
    - _Giải pháp (Mạch phân áp):_ Bạn dùng 2 con điện trở 3k3. Nối con số 1 từ chân Echo của cảm biến sang chân **GPIO 24** của Pi. Nối tiếp con số 2 từ chân **GPIO 24** đó cắm xuống Mass (GND). Việc này giúp chia đôi dòng điện 5V xuống 2.5V, an toàn tuyệt đối cho Pi.
        

### E. Còi báo Buzzer (Âm thanh phản hồi)

_(Nếu là còi 2 chân tròn)_

- **Chân dài (+):** Nối thẳng vào chân **GPIO 25** của Pi.
    
- **Chân ngắn (-):** Nối vào Mass chung.
    

_(Nếu là dạng Module có 3 chân)_

- **VCC:** Nối vào 3.3V hoặc 5V của Pi.
    
- **GND:** Nối vào Mass chung.
    
- **I/O (hoặc IN/S):** Nối vào chân **GPIO 25** của Pi.
    

### F. Webcam USB

- Cắm trực tiếp vào bất kỳ cổng USB (ưu tiên cổng USB 3.0 màu xanh) nào của Raspberry Pi.
    

## 3. Luồng Thuật Toán (Logic Flow)

Hệ thống phần mềm của bạn sẽ chạy 2 luồng (Threads) song song bằng Python:

### Luồng 1: Bảo Vệ & AI (Auto Door)

1. Vòng lặp liên tục đọc khoảng cách từ cảm biến siêu âm.
    
2. **NẾU** khoảng cách < 30cm (Có người đứng trước nhà):
    
    - Dừng đọc cảm biến tạm thời.
        
    - Kích hoạt Webcam USB chụp 1 khung hình (Dùng thư viện `OpenCV`).
        
    - Đưa ảnh qua model AI nhận diện khuôn mặt (Dùng thư viện `face_recognition`).
        
    - **NẾU** là "Người quen":
        
        - **Còi Buzzer kêu 1 tiếng bíp ngắn** (Bật GPIO 25 HIGH -> Chờ 0.2s -> Tắt LOW).
            
        - Phát lệnh cho Servo quay 90° (Mở cửa).
            
        - `time.sleep(5)` (Giữ cửa mở 5 giây cho người đi vào).
            
        - Quay Servo về 0° (Đóng cửa).
            
    - **NẾU** là "Người lạ":
        
        - **Còi Buzzer kêu 3 tiếng bíp liên tục** (Bật/Tắt GPIO 25 ba lần, mỗi lần cách nhau 0.1s).
            
        - Gửi cảnh báo hình ảnh người đó qua Telegram cho bạn. (Tùy chọn thêm).
            

### Luồng 2: App Điều Khiển (Smart Home)

Có 2 cách làm App cho sinh viên làm vi điều khiển:

- **Cách 1 (Telegram Bot):** Dùng Telegram làm App. Tạo các menu nút bấm `[Bật Đèn]`, `[Tắt Đèn]`, `[Bật Quạt]`, `[Tắt Quạt]`. Khi bạn ấn trên Telegram, Pi nhận lệnh và điều khiển các chân GPIO 17 (Đèn) và GPIO 27 (Relay Quạt).
    
- **Cách 2 (Web App nội bộ):** Dùng `Flask` (Python) tạo một trang web đơn giản có giao diện 4 nút bấm. Truy cập trang web này bằng điện thoại (cùng chung mạng WiFi với Pi) để điều khiển.
    

## 4. Các bước triển khai tiếp theo cho bạn

1. **Hoàn thiện phần thô:** Gắn Servo vào cửa, gắn siêu âm ra ngoài, đặt Webcam cố định hướng ra cửa.
    
2. **Cắm dây Breadboard:** Làm cẩn thận theo mục 2, đặc biệt chú ý mạch phân áp cho cảm biến siêu âm và dây Mass chung.
    
3. **Cài đặt thư viện trên Pi:** Bật terminal Pi lên và cài đặt: `pip install RPi.GPIO opencv-python face_recognition`
    
4. **Code từng phần:** Viết script test Còi Buzzer riêng -> Test Cảm biến siêu âm -> Test Servo -> Test Camera -> Cuối cùng mới ghép lại thành 1 file hoàn chỉnh.