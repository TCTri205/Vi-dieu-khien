#!/usr/bin/env python3
"""
Script chẩn đoán phần cứng toàn diện.
Chạy: GPIOZERO_PIN_FACTORY=lgpio python3 tests/diagnose_hw.py
"""
import time
import sys

# ===== BẢNG THAM CHIẾU PIN =====
# GPIO 17 = Chân vật lý 11  (LED - ĐÃ HOẠT ĐỘNG)
# GPIO 18 = Chân vật lý 12  (Servo signal)
# GPIO 25 = Chân vật lý 22  (Buzzer)
# GPIO 27 = Chân vật lý 13  (Relay - ĐÃ HOẠT ĐỘNG)
# GPIO 23 = Chân vật lý 16  (Trig)
# GPIO 24 = Chân vật lý 18  (Echo)

GPIO_TO_PHYSICAL = {
    17: 11, 18: 12, 27: 13, 22: 15,
    23: 16, 24: 18, 25: 22, 5: 29,
    6: 31, 12: 32, 13: 33, 19: 35,
    16: 36, 26: 37, 20: 38, 21: 40,
}

print("=" * 55)
print("  CHẨN ĐOÁN PHẦN CỨNG RASPBERRY PI")
print("=" * 55)

# ===== BƯỚC 1: Kiểm tra lgpio trực tiếp =====
print("\n[BƯỚC 1] Kiểm tra thư viện lgpio trực tiếp...")
try:
    import lgpio
    h = lgpio.gpiochip_open(0)
    print(f"  ✅ lgpio mở chip thành công (handle={h})")
except Exception as e:
    print(f"  ❌ Lỗi mở lgpio: {e}")
    sys.exit(1)

# ===== BƯỚC 2: Test từng GPIO bằng lgpio trực tiếp =====
test_pins = {
    17: "LED (đã biết hoạt động)",
    27: "Relay (đã biết hoạt động)",
    25: "Buzzer",
    18: "Servo signal",
}

print("\n[BƯỚC 2] Test OUTPUT từng chân GPIO bằng lgpio trực tiếp...")
print("  Mỗi chân sẽ được BẬT 2 giây rồi TẮT.")
print("  Hãy quan sát LED/Relay/Buzzer/Servo và ghi nhận.\n")

for gpio, name in test_pins.items():
    phys = GPIO_TO_PHYSICAL.get(gpio, "?")
    input(f"  Nhấn ENTER để test GPIO {gpio} (Chân vật lý {phys}) - {name}...")
    try:
        lgpio.gpio_claim_output(h, gpio)
        lgpio.gpio_write(h, gpio, 1)  # HIGH
        print(f"    -> GPIO {gpio} = HIGH (BẬT)")
        time.sleep(2)
        lgpio.gpio_write(h, gpio, 0)  # LOW
        print(f"    -> GPIO {gpio} = LOW  (TẮT)")
        lgpio.gpio_free(h, gpio)
        print(f"    ✅ GPIO {gpio} test xong.\n")
    except Exception as e:
        print(f"    ❌ Lỗi GPIO {gpio}: {e}\n")

# ===== BƯỚC 3: Test PWM bằng lgpio =====
print("\n[BƯỚC 3] Test PWM (còi và servo) bằng lgpio trực tiếp...")

input("  Nhấn ENTER để test PWM trên GPIO 25 (Buzzer - 1kHz)...")
try:
    lgpio.gpio_claim_output(h, 25)
    # tx_pwm(handle, gpio, frequency_Hz, duty_cycle_percent)
    lgpio.tx_pwm(h, 25, 1000, 50)  # 1kHz, 50% duty
    print("    -> Đang phát PWM 1kHz trên GPIO 25...")
    time.sleep(2)
    lgpio.tx_pwm(h, 25, 0, 0)  # Tắt
    lgpio.gpio_free(h, 25)
    print("    ✅ PWM Buzzer test xong.\n")
except Exception as e:
    print(f"    ❌ Lỗi PWM Buzzer: {e}\n")

input("  Nhấn ENTER để test PWM trên GPIO 18 (Servo - 50Hz)...")
try:
    lgpio.gpio_claim_output(h, 18)
    # Servo cần tín hiệu: tx_servo(handle, gpio, pulse_width_us)
    lgpio.tx_servo(h, 18, 1500)  # 1500us = vị trí giữa
    print("    -> Servo -> Giữa (1500us)")
    time.sleep(2)
    lgpio.tx_servo(h, 18, 2000)  # 2000us = ~90 độ
    print("    -> Servo -> 90° (2000us)")
    time.sleep(2)
    lgpio.tx_servo(h, 18, 1000)  # 1000us = ~0 độ
    print("    -> Servo -> 0° (1000us)")
    time.sleep(2)
    lgpio.tx_servo(h, 18, 0)  # Tắt
    lgpio.gpio_free(h, 18)
    print("    ✅ PWM Servo test xong.\n")
except Exception as e:
    print(f"    ❌ Lỗi PWM Servo: {e}\n")

# ===== BƯỚC 4: Hướng dẫn Cross-test =====
print("\n[BƯỚC 4] CROSS-TEST (Quan trọng nhất!)")
print("=" * 55)
print("  Nếu Bước 2 và 3 cho thấy GPIO 25/18 không lỗi")
print("  nhưng thiết bị vẫn im, hãy thử đổi chân:")
print()
print("  a) RÚT dây tín hiệu Buzzer khỏi GPIO 25 (vật lý 22)")
print("     CẮM vào GPIO 17 (vật lý 11) thay LED")
print("     Chạy lại test GPIO 17 ở Bước 2")
print("     -> Còi kêu: GPIO 25 cắm sai chân")
print("     -> Còi im:  Còi hỏng hoặc cần nguồn mạnh hơn")
print()
print("  b) RÚT dây tín hiệu Servo khỏi GPIO 18 (vật lý 12)")
print("     CẮM vào GPIO 17 (vật lý 11)")
print("     -> Servo rung/nhúc: GPIO 18 cắm sai")
print("     -> Servo im: Kiểm tra nguồn pin 6V")
print()

# ===== Dọn dẹp =====
lgpio.gpiochip_close(h)
print("✅ Chẩn đoán hoàn tất.")
