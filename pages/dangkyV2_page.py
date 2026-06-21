from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class DangKyV2Page:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://test.tokhaibaohiem.vn/dang-ky-lan-dau-v2"

        self.tax_code_input = (By.XPATH, "//input[@placeholder='Nhập mã số thuế']")
        self.search_button = (By.XPATH, "//input[@placeholder='Nhập mã số thuế']/following-sibling::div//button")

        self.province_input = (By.XPATH, "//input[@placeholder='Chọn tỉnh/thành']")
        self.district_input = (By.XPATH, "//input[@placeholder='Chọn quận/huyện']")

        self.bhxh_province_input = (By.XPATH, "//input[@placeholder='Cơ quan BHXH tỉnh']")
        self.bhxh_management_input = (By.XPATH,
                                  "//input[@placeholder='Cơ quan BHXH quản lý' or @placeholder='Chọn cơ quan BHXH tỉnh trước']")

        self.file_input = (By.XPATH, "//input[@type='file']")

        self.note_input = (By.XPATH, "//input[@placeholder='Nhập nội dung hoặc ghi chú']")

        self.captcha_input = (By.XPATH, "//input[@placeholder='Nhập mã xác thực']")

        self.register_button = (By.XPATH, "//button[contains(., 'Đăng ký sử dụng dịch vụ')]")
        self.sign_hsm_button = (By.XPATH, "//button[contains(., 'Ký bằng HSM EasyCA')]")

    def open_page(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    def enter_tax_code(self, tax_code):
        wait = WebDriverWait(self.driver, 10)
        input_element = wait.until(EC.visibility_of_element_located(self.tax_code_input))
        input_element.clear()

        for char in tax_code:
            input_element.send_keys(char)
            time.sleep(0.3)

    def click_search(self):
        wait = WebDriverWait(self.driver, 10)
        button_element = wait.until(EC.element_to_be_clickable(self.search_button))
        button_element.click()

    def select_province(self, province_name):
        wait = WebDriverWait(self.driver, 10)
        input_el = wait.until(EC.element_to_be_clickable(self.province_input))
        input_el.click()
        time.sleep(1)

        item_xpath = f"//div[contains(@class, 'mud-list-item')]//p[contains(text(), '{province_name}')]"
        wait.until(EC.element_to_be_clickable((By.XPATH, item_xpath))).click()

    def select_district(self, district_name):
        wait = WebDriverWait(self.driver, 10)
        input_el = wait.until(EC.element_to_be_clickable(self.district_input))
        input_el.click()
        time.sleep(1)

        item_xpath = f"//div[contains(@class, 'mud-list-item')]//p[contains(normalize-space(), '{district_name}')]"
        wait.until(EC.element_to_be_clickable((By.XPATH, item_xpath))).click()

    def select_bhxh_province(self, province_name):
        wait = WebDriverWait(self.driver, 10)
        input_el = wait.until(EC.presence_of_element_located(self.bhxh_province_input))

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_el)
        time.sleep(1)

        input_el.click()
        time.sleep(1)

        item_xpath = f"//div[contains(@class, 'mud-popover')]//p[contains(text(), '{province_name}')]"
        wait.until(EC.element_to_be_clickable((By.XPATH, item_xpath))).click()

    def select_bhxh_management(self, management_name):
        wait = WebDriverWait(self.driver, 10)
        input_el = wait.until(EC.element_to_be_clickable(self.bhxh_management_input))

        input_el.click()
        time.sleep(1)

        item_xpath = f"//div[contains(@class, 'mud-popover')]//p[contains(text(), '{management_name}')]"
        wait.until(EC.element_to_be_clickable((By.XPATH, item_xpath))).click()

    def upload_file(self, file_path):

        wait = WebDriverWait(self.driver, 10)
        input_el = wait.until(EC.presence_of_element_located(self.file_input))

        input_el.send_keys(file_path)

        print(f"Đang tải file: {file_path}...")
        time.sleep(5)

    def enter_note(self, note_text):
        wait = WebDriverWait(self.driver, 10)
        input_el = wait.until(EC.presence_of_element_located(self.note_input))

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_el)
        time.sleep(1)

        input_el.clear()
        input_el.send_keys(note_text)
        print(f"Đã nhập ghi chú: {note_text}")

    def wait_for_captcha_input(self):

        print("\n[HÀNH ĐỘNG] Vui lòng nhìn màn hình trình duyệt và nhập mã Captcha...")
        wait = WebDriverWait(self.driver, 120)  # Chờ tối đa 2 phút để bạn nhập

        try:
            wait.until(lambda d: len(d.find_element(*self.captcha_input).get_attribute("value")) == 6)
            print("[OK] Đã nhận đủ 6 ký tự mã xác thực.")
            time.sleep(1)  # Nghỉ 1 giây cho chắc chắn trước khi tiếp tục
        except Exception as e:
            print("[LỖI] Quá thời gian chờ nhập Captcha hoặc có lỗi xảy ra.")

    def click_final_register(self):
        wait = WebDriverWait(self.driver, 10)
        btn = wait.until(EC.presence_of_element_located(self.register_button))

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(1)

        wait.until(EC.element_to_be_clickable(self.register_button)).click()
        time.sleep(5)
        print("Đã nhấn nút Đăng ký sử dụng dịch vụ.")

    def select_sign_easyca(self):
        wait = WebDriverWait(self.driver, 15)
        btn_sign = wait.until(EC.element_to_be_clickable(self.sign_hsm_button))
        btn_sign.click()
        print("Đã chọn Ký bằng HSM EasyCA. Đang đợi load kết quả (10s)...")

        time.sleep(15)