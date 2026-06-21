import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage

class ChucNang600Page(BasePage):
    THU_TUC_600_XPATH = "//div[contains(@class, 'mud-list-item')]//span[text()='600']/ancestor::div[contains(@class, 'mud-list-item')]"
    BTN_TAO_DOT_XPATH = "//button[contains(., 'Tạo đợt kê khai')]"
    SPINNER_XPATH = "//div[contains(@class, 'mud-wasm-loading-progress')]|//div[contains(@class, 'mud-overlay')]"

    BTN_NAP_EXCEL_XPATH = "//button[contains(., 'Nạp excel')]"
    INPUT_FILE_HIDDEN_XPATH = "//input[@type='file']"
    BTN_TAI_DU_LIEU_XPATH = "//button[.//span[contains(text(),'Tải lên')]]"

    BTN_TAI_EXCEL_XPATH = "//button[contains(., 'Tải excel')]"

    BTN_XEM_TRUOC_XPATH = "//button[contains(., 'Xem trước')]"
    BTN_TAI_EXCEL_PREVIEW_XPATH = "//button[contains(@class, 'btn-primary-core') and contains(., 'Tải Excel')]"
    BTN_TAI_XML_PREVIEW_XPATH = "//button[contains(@class, 'btn-primary-core') and contains(., 'Tải Xml')]"
    BTN_DONG_PREVIEW_XPATH = "//button[contains(@class, 'btn-secondary') and contains(., 'Đóng')]"

    BTN_KY_GUI_XPATH = "//button[contains(., 'Ký/gửi hồ sơ')]"
    BTN_DONG_Y_XPATH = "//button[contains(., 'Đồng ý')]"
    BTN_KY_HSM_XPATH = "//button[contains(., 'Ký bằng HSM EasyCA')]"
    BTN_TRA_CUU_HS_XPATH = "//button[contains(., 'Tra cứu hồ sơ')]"
    LINK_TRA_CUU_DAU_DONG_XPATH = "//a[contains(@class, 'mud-link') and contains(., 'Tra cứu')]"

    BTN_THEM_TU_HSNS_XPATH = "//button[contains(., 'Thêm từ HSNS')]"
    INPUT_TIM_KIEM_HSNS_XPATH = "//input[contains(@placeholder, 'Nhập tên, BHXH, CMND')]"
    BTN_ICON_SEARCH_HSNS_XPATH = "//button[contains(@class, 'mud-input-adornment-icon-button')]"
    LIST_CHECKBOX_HSNS_XPATH = "//tbody//input[@type='checkbox']"
    BTN_CHON_QUYET_DINH_XPATH = "//button[contains(., 'Chọn')]"

    SELECT_TRANG_THAI_XPATH = "//input[@placeholder='Trạng thái công việc']/.."
    ITEM_DANG_LAM_VIEC_XPATH = "//p[text()='Đang làm việc']/ancestor::div[@role='button' or contains(@class, 'mud-list-item')]"

    BTN_SAO_CHEP_MAIN_XPATH = "//button[contains(., 'Sao chép')]"
    BTN_ICON_SAO_CHEP_ROW_XPATH = "(//td[@data-label='Sao chép']//button)[1]"

    def wait_for_spinner_gone(self):
        time.sleep(0.5)
        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located((By.XPATH, self.SPINNER_XPATH))
        )
        time.sleep(0.8)

    def select_thu_tuc_600(self):
        wait = WebDriverWait(self.driver, 10)
        el = wait.until(EC.presence_of_element_located((By.XPATH, self.THU_TUC_600_XPATH)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(1.5)
        self.driver.execute_script("arguments[0].click();", el)
        time.sleep(1)

    def click_tao_dot_ke_khai(self):
        wait = WebDriverWait(self.driver, 10)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, self.BTN_TAO_DOT_XPATH)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(3)

    def click_nap_excel(self):
        wait = WebDriverWait(self.driver, 10)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, self.BTN_NAP_EXCEL_XPATH)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(1.5)

    def upload_excel_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Không tìm thấy file tại: {file_path}")

        input_file = self.driver.find_element(By.XPATH, self.INPUT_FILE_HIDDEN_XPATH)
        input_file.send_keys(file_path)
        print(f"Đã chọn file: {file_path}")
        time.sleep(2)

    def click_tai_du_lieu_len(self):
        wait = WebDriverWait(self.driver, 10)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, self.BTN_TAI_DU_LIEU_XPATH)))
        self.driver.execute_script("arguments[0].click();", btn)
        print("Đã nhấn nút 'Tải dữ liệu lên'")
        time.sleep(3)

    def click_tai_excel(self):
        wait = WebDriverWait(self.driver, 10)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, self.BTN_TAI_EXCEL_XPATH)))

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(1)

        self.driver.execute_script("arguments[0].click();", btn)
        print("Đã nhấn nút 'Tải excel'")
        time.sleep(3)

    def click_xem_truoc(self):
        wait = WebDriverWait(self.driver, 10)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, self.BTN_XEM_TRUOC_XPATH)))
        self.driver.execute_script("arguments[0].click();", btn)
        print("Đã nhấn nút 'Xem trước'")
        time.sleep(2)  # Chờ modal hiện lên hẳn

    def click_tai_excel_preview(self):
        btn = self.driver.find_element(By.XPATH, self.BTN_TAI_EXCEL_PREVIEW_XPATH)
        self.driver.execute_script("arguments[0].click();", btn)
        print("Đã nhấn 'Tải Excel' trong Preview")
        time.sleep(2)

    def click_tai_xml_preview(self):
        btn = self.driver.find_element(By.XPATH, self.BTN_TAI_XML_PREVIEW_XPATH)
        self.driver.execute_script("arguments[0].click();", btn)
        print("Đã nhấn 'Tải Xml' trong Preview")
        time.sleep(2)

    def click_dong_preview(self):
        btn = self.driver.find_element(By.XPATH, self.BTN_DONG_PREVIEW_XPATH)
        self.driver.execute_script("arguments[0].click();", btn)
        print("Đã đóng modal Xem trước")
        time.sleep(1)

    def click_ky_gui_ho_so(self):
        wait = WebDriverWait(self.driver, 10)

        btn_ky = wait.until(EC.element_to_be_clickable((By.XPATH, self.BTN_KY_GUI_XPATH)))
        self.driver.execute_script("arguments[0].click();", btn_ky)
        time.sleep(1.5)

        btn_ok = wait.until(EC.element_to_be_clickable((By.XPATH, self.BTN_DONG_Y_XPATH)))
        self.driver.execute_script("arguments[0].click();", btn_ok)
        print("Đã nhấn Ký/Gửi và Đồng ý")
        time.sleep(2)

    def click_ky_hsm(self):
        wait = WebDriverWait(self.driver, 10)
        btn_hsm = wait.until(EC.element_to_be_clickable((By.XPATH, self.BTN_KY_HSM_XPATH)))
        self.driver.execute_script("arguments[0].click();", btn_hsm)
        print("Đã nhấn 'Ký bằng HSM EasyCA'")
        time.sleep(10)

    def click_tra_cuu_ho_so_button(self):
        btn = self.driver.find_element(By.XPATH, self.BTN_TRA_CUU_HS_XPATH)
        self.driver.execute_script("arguments[0].click();", btn)
        print("Đã nhấn nút 'Tra cứu hồ sơ'")
        time.sleep(15)

    def click_link_tra_cuu_ket_qua(self):
        link = self.driver.find_element(By.XPATH, self.LINK_TRA_CUU_DAU_DONG_XPATH)
        self.driver.execute_script("arguments[0].click();", link)
        print("Đã nhấn link 'Tra cứu' để kiểm tra kết quả cuối cùng")
        time.sleep(3)

    def click_them_tu_hsns(self):
        wait = WebDriverWait(self.driver, 10)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, self.BTN_THEM_TU_HSNS_XPATH)))
        self.driver.execute_script("arguments[0].click();", btn)
        print("Đã nhấn 'Thêm từ HSNS'")
        time.sleep(2)


    def search_nhan_vien_hsns(self, name):
        wait = WebDriverWait(self.driver, 10)
        input_search = wait.until(EC.visibility_of_element_located((By.XPATH, self.INPUT_TIM_KIEM_HSNS_XPATH)))

        self.driver.execute_script("arguments[0].click();", input_search)
        input_search.clear()
        time.sleep(0.5)

        input_search.send_keys(name)
        time.sleep(1)

        input_search.send_keys(Keys.ENTER)
        print(f"Đã nhập '{name}' và nhấn Enter")
        time.sleep(1)
        try:
            self.wait_for_spinner_gone()
        except:
            pass

        time.sleep(2)

    def chon_nhieu_nhan_vien_hsns(self, so_luong=5):
        checkboxes = self.driver.find_elements(By.XPATH, "//tbody//input[@type='checkbox']")

        count = 0
        for i in range(min(so_luong, len(checkboxes))):
            self.driver.execute_script("arguments[0].click();", checkboxes[i])
            count += 1
            time.sleep(0.2)

        btn_chon_xpath = "//div[contains(@class, 'mud-dialog-actions')]//button[contains(@class, 'mud-button-filled-primary')]"

        btn_chon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, btn_chon_xpath))
        )
        btn_chon.click()
        print(f"Đã nhấn đúng nút Chọn cho {count} nhân sự.")

    def click_sao_chep_ho_so(self):
        wait = WebDriverWait(self.driver, 10)

        btn_main = wait.until(EC.element_to_be_clickable((By.XPATH, self.BTN_SAO_CHEP_MAIN_XPATH)))
        self.driver.execute_script("arguments[0].click();", btn_main)
        print("Đã nhấn nút 'Sao chép' chính")
        time.sleep(3)

        btn_row = wait.until(EC.element_to_be_clickable((By.XPATH, self.BTN_ICON_SAO_CHEP_ROW_XPATH)))
        self.driver.execute_script("arguments[0].click();", btn_row)
        print("Đã nhấn icon sao chép trên dòng dữ liệu")
        time.sleep(3)