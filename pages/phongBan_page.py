from pages.base_page import BasePage, logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class PhongBanPage(BasePage):
    BTN_THEM_MOI = (By.XPATH, "//button[.//span[contains(@class,'mud-button-label')][contains(.,'Thêm mới')]]")
    BTN_LUU = (By.XPATH, "//button[normalize-space(.)='Lưu']")
    BTN_DONG = (By.XPATH, "//button[normalize-space(.)='Đóng']")

    INPUT_TEN_PB = (By.XPATH, "//input[@placeholder='Nhập tên phòng ban']")
    INPUT_MA_PB = (By.XPATH, "//input[@placeholder='Nhập mã phòng ban']")
    DROPDOWN_PB_TRUC_THUOC = (By.XPATH, "//input[@placeholder='Nhập phòng ban cha']")

    INPUT_SEARCH = (By.XPATH, "//input[contains(@placeholder, 'Nhập tên/mã phòng ban')]")

    BTN_EDIT_ICON = (By.XPATH, "//button[@title='Chỉnh sửa']")
    BTN_DELETE_ICON = (By.XPATH, "//button[@title='Xóa']")

    CHECKBOX_DAU_TIEN = (By.XPATH, "(//input[@type='checkbox'])[2]")
    BTN_XOA_CHON = (By.XPATH, "//button[contains(., 'Xoá chọn')]")
    BTN_DONG_Y_XOA = (By.XPATH, "//button[contains(., 'Đồng ý')]")

    BTN_XUAT_EXCEL = (By.XPATH, "//button[.//span[normalize-space()='Tải Excel']]")

    BTN_NAP_EXCEL = (By.XPATH, "//button[.//span[normalize-space()='Nạp excel']]")
    FILE_INPUT = (By.XPATH, "//input[@type='file']")
    BTN_TAI_DU_LIEU_LEN = (By.XPATH, "//button[.//span[contains(text(), 'Tải lên')]]")

    def click_them_moi(self):
        self.wait_and_click(self.BTN_THEM_MOI)

    def nhap_form_them_moi(self, ten, ma=None, ten_cha=None):
        self.wait_for_element(self.INPUT_TEN_PB, 10000)

        self.send_keys(self.INPUT_TEN_PB, ten)

        if ma:
            self.send_keys(self.INPUT_MA_PB, ma)

        if ten_cha:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.mud-overlay"))
                )
            except:
                pass

            el = self.driver.find_element(*self.DROPDOWN_PB_TRUC_THUOC)
            self.driver.execute_script("arguments[0].click();", el)
            self.driver.execute_script("arguments[0].value = '';", el)
            el.send_keys(ten_cha)

            time.sleep(0.5)
            ten_cha_safe = ten_cha.split("&")[0].strip()
            xpath_item = (By.XPATH, f"//div[contains(@class,'mud-list-item') and contains(.,'{ten_cha_safe}')]")
            self.wait_and_click(xpath_item)

    def nhan_luu(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.mud-overlay"))
            )
        except:
            pass

        try:
            el = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.BTN_LUU)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            self.driver.execute_script("arguments[0].click();", el)
        except Exception as e:
            logger.error(f"Không thể click nút Lưu: {e}")
            raise

    def nhan_dong(self):
        self.wait_and_click(self.BTN_DONG)

    def tim_kiem(self, tu_khoa):
        self.send_keys(self.INPUT_SEARCH, tu_khoa)

    def xoa_phong_ban_dau_tien(self):
        self.wait_and_click(self.BTN_DELETE_ICON)
        self.wait_and_click(self.BTN_DONG_Y_XOA)

    def click_nap_excel(self):
        self.wait_and_click(self.BTN_NAP_EXCEL)

    def upload_file(self, file_path):
        wait = WebDriverWait(self.driver, 15)
        input_el = wait.until(EC.presence_of_element_located(self.FILE_INPUT))

        self.driver.execute_script("arguments[0].removeAttribute('disabled')", input_el)

        input_el.send_keys(file_path)
        print(f"[INFO] Đang thực hiện tải file đính kèm: {file_path}")
        time.sleep(5)

    def click_tai_du_lieu_len(self):
        self.wait_and_click(self.BTN_TAI_DU_LIEU_LEN)