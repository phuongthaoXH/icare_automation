"""
Script debug: Dump HTML popover sau khi click dropdown Trạng thái.
Chạy: python debug_dump_dialog.py
Kết quả: reports/popover_html.txt
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

USERNAME = "0107489961_ICARE01"
PASSWORD = "12345678aA@"   # ← đổi đúng password nếu khác

opts = Options()
opts.add_argument("--start-maximized")
driver = webdriver.Chrome(options=opts)
wait   = WebDriverWait(driver, 20)

try:
    # 1. Đăng nhập
    driver.get("https://test.tokhaibaohiem.vn/dang-nhap")
    time.sleep(3)
    inputs = driver.find_elements(By.XPATH, "//input")
    for inp in inputs:
        t = inp.get_attribute("type") or ""
        if t in ("text", "email", ""):
            inp.send_keys(USERNAME)
            break
    for inp in driver.find_elements(By.XPATH, "//input[@type='password']"):
        inp.send_keys(PASSWORD)
        break
    driver.find_element(By.XPATH, "//button[contains(.,'Đăng nhập')]").click()
    time.sleep(4)

    # 2. Vào trang Chức vụ
    driver.get("https://test.tokhaibaohiem.vn/chuc-vu")
    time.sleep(3)

    # 3. Click Thêm mới
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[.//span[contains(.,'Thêm mới')]]")
    ))
    btn.click()
    time.sleep(2)

    # 4. Dump HTML toàn bộ dialog
    try:
        dialog = driver.find_element(By.XPATH, "//div[contains(@class,'mud-dialog')]")
        dialog_html = dialog.get_attribute("outerHTML")
    except Exception as e:
        dialog_html = f"Không tìm thấy dialog: {e}"

    with open("reports/dialog_html.txt", "w", encoding="utf-8") as f:
        f.write(dialog_html)
    print("✅ Đã ghi reports/dialog_html.txt")

    # 5. Click dropdown trạng thái
    try:
        dd = driver.find_element(
            By.XPATH,
            "//div[contains(@class,'mud-dialog')]//div[contains(@class,'mud-select-input') and @tabindex='0']"
        )
        print(f"✅ Tìm thấy dropdown: {dd.get_attribute('outerHTML')[:200]}")
        driver.execute_script("arguments[0].click();", dd)
        time.sleep(1)
    except Exception as e:
        print(f"❌ Không tìm thấy dropdown: {e}")

    # 6. Dump toàn bộ body sau khi popover mở
    body_html = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
    with open("reports/popover_html.txt", "w", encoding="utf-8") as f:
        f.write(body_html)
    print("✅ Đã ghi reports/popover_html.txt")

    # 7. In tất cả mud-list-item tìm được
    items = driver.find_elements(By.XPATH, "//div[contains(@class,'mud-list-item')]")
    print(f"\n✅ Tìm thấy {len(items)} mud-list-item:")
    for i, item in enumerate(items):
        print(f"  [{i}] outerHTML: {item.get_attribute('outerHTML')[:300]}")

finally:
    input("\n⏸ Nhấn Enter để đóng trình duyệt...")
    driver.quit()