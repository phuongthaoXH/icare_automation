from pages.base_page import BasePage, logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class ChucVuPage(BasePage):

    BTN_THEM_MOI    = (By.XPATH, "//button[.//span[contains(@class,'mud-button-label')][contains(.,'Thêm mới')]]")
    BTN_LUU         = (By.XPATH, "//button[normalize-space(.)='Lưu']")
    BTN_DONG        = (By.XPATH, "//button[normalize-space(.)='Đóng']")

    INPUT_TEN_CV    = (By.XPATH, "//div[contains(@class,'mud-dialog')]//input[@placeholder='Nhập tên chức vụ']")

    DROPDOWN_TRANG_THAI = (By.XPATH,
        "//div[contains(@class,'mud-dialog')]"
        "//div[contains(@class,'mud-select-input') and @tabindex='0']"
    )

    DROPDOWN_FILTER_TRANG_THAI = (By.XPATH,
                                  "(//div[contains(@class,'mud-select')])[1]"
                                  "//div[contains(@class,'mud-select-input')]"
    )

    MSG_TEN_TRONG   = (By.XPATH,
        "//div[contains(@class,'mud-dialog')]"
        "//*[contains(text(),'Trường không được trống')]"
    )

    BTN_EDIT_ICON   = (By.XPATH, "//button[@title='Chỉnh sửa']")
    BTN_DELETE_ICON = (By.XPATH, "//button[@title='Xóa']")
    BTN_DONG_Y_XOA  = (By.XPATH, "//button[contains(.,'Đồng ý')]")

    CHECKBOX_DAU_TIEN = (By.XPATH, "(//input[@type='checkbox'])[2]")
    BTN_XOA_CHON    = (By.XPATH, "//button[contains(.,'Xoá chọn')]")

    INPUT_SEARCH    = (By.XPATH, "//input[contains(@placeholder,'Nhập tên chức vụ') and not(ancestor::*[contains(@class,'mud-dialog')])]")

    BTN_XUAT_EXCEL = (By.XPATH, "//button[.//span[normalize-space()='Tải Excel']]")

    BTN_NAP_EXCEL = (By.XPATH, "//button[.//span[normalize-space()='Nạp excel']]")
    FILE_INPUT = (By.XPATH, "//input[@type='file']")
    BTN_TAI_DU_LIEU_LEN = (By.XPATH, "//button[.//span[contains(text(), 'Tải lên')]]")

    def _wait_overlay_gone(self, timeout: int = 5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.mud-overlay"))
            )
        except Exception:
            pass

    def click_them_moi(self):
        self.wait_and_click(self.BTN_THEM_MOI)
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.INPUT_TEN_CV)
        )
        time.sleep(0.3)

    def nhap_ten(self, ten: str):
        inp = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.INPUT_TEN_CV)
        )
        inp.clear()
        inp.send_keys(ten)

    def chon_trang_thai(self, trang_thai: str):
        self._wait_overlay_gone()

        dd = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.DROPDOWN_TRANG_THAI)
        )
        ActionChains(self.driver).move_to_element(dd).click().perform()
        time.sleep(1.5)

        xpaths_option = [
            f"//*[contains(@class,'mud-list-item')]//p[normalize-space()='{trang_thai}']",
            f"//*[contains(@class,'mud-list-item')]//span[normalize-space()='{trang_thai}']",
            f"//*[contains(@class,'mud-list-item') and normalize-space(.)='{trang_thai}']",
            f"//*[normalize-space(.)='{trang_thai}' and @tabindex='0']",
        ]
        for xp in xpaths_option:
            try:
                opt = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, xp))
                )
                self.driver.execute_script("arguments[0].click();", opt)
                logger.info(f"✅ Chọn trạng thái '{trang_thai}' thành công")
                return
            except Exception:
                continue

        raise Exception(f"❌ Không tìm thấy option '{trang_thai}' trong dropdown!")

    def nhan_luu(self):
        self._wait_overlay_gone()
        try:
            el = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.BTN_LUU)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            self.driver.execute_script("arguments[0].click();", el)
        except Exception as e:
            logger.error(f"Không thể click nút Lưu: {e}")
            raise

    def nhan_dong(self):
        self.wait_and_click(self.BTN_DONG)

    def is_msg_ten_trong_hien(self, timeout: int = 5) -> bool:
        return self.is_element_visible(self.MSG_TEN_TRONG, timeout * 1000)

    def tim_kiem(self, tu_khoa: str):
        self.send_keys(self.INPUT_SEARCH, tu_khoa)

    def xoa_chuc_vu_dau_tien(self):
        self.wait_and_click(self.BTN_DELETE_ICON)
        self.wait_and_click(self.BTN_DONG_Y_XOA)

    def click_nap_excel(self):
        self.wait_and_click(self.BTN_NAP_EXCEL)

    def upload_file(self, file_path):
        """Logic tải file đính kèm (giống dangkyV2 và PhongBan)"""
        wait = WebDriverWait(self.driver, 15)
        input_el = wait.until(EC.presence_of_element_located(self.FILE_INPUT))

        self.driver.execute_script("arguments[0].removeAttribute('disabled')", input_el)

        input_el.send_keys(file_path)
        print(f"[INFO] Đang thực hiện tải file đính kèm: {file_path}")
        time.sleep(5)

    def click_tai_du_lieu_len(self):
        self.wait_and_click(self.BTN_TAI_DU_LIEU_LEN)
        print("[INFO] Đã nhấn nút Tải dữ liệu lên")