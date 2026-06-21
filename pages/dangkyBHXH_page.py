import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage, logger


class DangKyBHXHPage(BasePage):
    BTN_CAP_NHAT_CKS = (By.XPATH, "//button[.//span[normalize-space()='Cập nhật thông tin chữ ký số']]")
    BTN_CAP_NHAT_THONG_TIN = (By.XPATH, "//button[.//span[contains(text(), 'Cập nhật thông tin')]]")
    BTN_DANG_KY_SU_DUNG = (By.XPATH, "//button[.//span[normalize-space(.)='Đăng ký sử dụng']]")

    BTN_NGUNG_SU_DUNG_DV = (By.XPATH, "//button[.//span[normalize-space()='Ngừng sử dụng DV GDĐT']]")
    INPUT_LY_DO = (By.XPATH, "//div[contains(., 'Lý do')]//textarea")
    BTN_XAC_NHAN_NGUNG_POPUP = (By.XPATH, "//button[.//span[normalize-space(.)='Ngừng dịch vụ']]")

    BTN_KY_HSM = (By.XPATH, "//button[.//span[contains(text(), 'Ký bằng HSM EasyCA')]]")

    BTN_XAC_NHAN = (By.XPATH, "//button[.//span[contains(text(), 'Xác nhận')]]")

    BTN_TRA_CUU = (By.XPATH, "//button[.//span[text()='Tra cứu']]")


    def click_cap_nhat_cks(self):
        self.wait_and_click(self.BTN_CAP_NHAT_CKS)
        print("[INFO] Đã nhấn nút Cập nhật thông tin chữ ký số")

    def click_cap_nhat_thong_tin(self):
        self.wait_and_click(self.BTN_CAP_NHAT_THONG_TIN)
        print("[INFO] Đã nhấn nút Cập nhật thông tin")

    def click_dang_ky_su_dung(self):
        self.wait_and_click(self.BTN_DANG_KY_SU_DUNG)
        print("[INFO] Đã nhấn nút Đăng ký sử dụng")

    def click_ngung_su_dung_dv_ngoai(self):
        self.wait_and_click(self.BTN_NGUNG_SU_DUNG_DV)
        print("[INFO] Đã nhấn nút Ngừng sử dụng DV GDDT")

    def nhap_ly_do_ngung(self, ly_do="Kết thúc hợp đồng thử nghiệm"):
        el = self.wait_for_element(self.INPUT_LY_DO)
        el.click()
        el.send_keys(ly_do)
        print(f"[INFO] Đã nhập lý do: {ly_do}")

    def click_xac_nhan_ngung_popup(self):
        # Đợi 1s để chắc chắn popup đã render xong hoàn toàn
        time.sleep(1)
        # Sử dụng JS click nếu click thông thường vẫn bị báo lỗi không tìm thấy hoặc bị che
        try:
            el = self.wait_for_element(self.BTN_XAC_NHAN_NGUNG_POPUP)
            self.driver.execute_script("arguments[0].click();", el)
            print("[INFO] Đã nhấn nút xác nhận Ngừng dịch vụ bằng JS")
            time.sleep(3)

        except Exception as e:
            print(f"[ERROR] Không thể nhấn nút xác nhận: {e}")
            raise

    def click_ky_hsm(self):
        self.wait_and_click(self.BTN_KY_HSM)
        print("[INFO] Đã nhấn nút Ký bằng HSM EasyCA")

    def click_xac_nhan(self):
        self.wait_and_click(self.BTN_XAC_NHAN)
        print("[INFO] Đã nhấn nút Xác nhận")

    def click_tra_cuu(self):
        print("[INFO] Đợi 5s trước khi nhấn Tra cứu...")
        time.sleep(5)

        self.wait_and_click(self.BTN_TRA_CUU)
        print("[INFO] Đã nhấn nút Tra cứu. Đợi 5s để load xong kết quả...")
        time.sleep(5)