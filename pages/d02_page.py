import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class D02Page(BasePage):
    SEL_THU_TUC_600 = (By.XPATH, "//div[contains(@class, 'item-thutuc')]//span[text()='600']")
    BTN_TAO_DOT_MOI = (By.XPATH, "//button[contains(., 'Tạo đợt kê khai')]")
    BTN_THEM_MOI_DONG = (By.XPATH, "//button[contains(., 'Thêm mới')]")
    SEL_TABLE = (By.CSS_SELECTOR, ".mud-table-container")
    SEL_TABLE_ROWS = (By.XPATH, "//tr[contains(@class, 'mud-table-row')]")

    BTN_XOA_TAT_CA = (By.XPATH, "//button[contains(., 'Xoá tất cả')]")
    BTN_XOA_CHON = (By.XPATH, "//button[contains(., 'Xoá chọn')]")
    BTN_LUU = (By.XPATH, "//button[contains(., 'Lưu')]")
    BTN_KY_GUI = (By.XPATH, "//button[contains(., 'Ký/gửi hồ sơ')]")
    BTN_THEM_HSNS = (By.XPATH, "//button[contains(., 'Thêm từ HSNS')]")
    BTN_NAP_EXCEL = (By.XPATH, "//button[contains(., 'Nạp excel')]")
    BTN_TAI_EXCEL = (By.XPATH, "//button[contains(., 'Tải excel')]")
    BTN_XEM_TRUOC = (By.XPATH, "//button[contains(., 'Xem trước')]")

    FLD_HO_TEN = (By.XPATH, "//div[@data-column-key='HoTen']//input")
    FLD_SO_SO = (By.XPATH, "//div[@data-column-key='SoSo']//input")
    FLD_MA_SO_BHXH = (By.XPATH, "//div[@data-column-key='MaSoBhxh']//input")
    FLD_NGAY_SINH = (By.XPATH, "//div[@data-column-key='NgaySinh']//input")
    FLD_GIOI_TINH = (By.XPATH, "//div[@data-column-key='GioiTinh']//input")

    FLD_LOAI_NGAY_SINH = (By.XPATH, "//div[@data-column-key='ChiCoNamSinh']//div[@tabindex='0']")
    FLD_SO_CMT = (By.XPATH, "//div[@data-column-key='SoCmt']//input")
    FLD_DIEN_THOAI = (By.XPATH, "//div[@data-column-key='DienThoai']//input")

    FLD_TIEN_LUONG = (By.XPATH, "//div[@data-column-key='TienLuong']//input")
    FLD_HE_SO_LUONG = (By.XPATH, "//div[@data-column-key='HeSoLuong']//input")
    FLD_PHU_CAP_CV = (By.XPATH, "//div[@data-column-key='PhuCapCv']//input")
    FLD_PHU_CAP_TN = (By.XPATH, "//div[@data-column-key='PhuCapTn']//input")
    FLD_PHU_CAP_TNN = (By.XPATH, "//div[@data-column-key='PhuCapTnn']//input")
    FLD_PHU_CAP_KHAC = (By.XPATH, "//div[@data-column-key='PhuCapKhac']//input")

    FLD_TU_THANG = (By.XPATH, "//div[@data-column-key='TuThang']//input")
    FLD_DEN_THANG = (By.XPATH, "//div[@data-column-key='DenThang']//input")
    FLD_TY_LE_DONG = (By.XPATH, "//div[@data-column-key='TyLeDong']//input")
    FLD_NGAY_NOP_TRA = (By.XPATH, "//div[@data-column-key='NgayNopTra']//input")

    FLD_PHU_LUC = (By.XPATH, "//div[@data-column-key='LoaiHoSo']//input")
    FLD_PHUONG_AN = (By.XPATH, "//div[@data-column-key='PhuongAnId']//input")
    LBL_ERROR_PHUONG_AN = (By.XPATH,"//div[@data-column-key='PhuongAnId']//div[contains(@class, 'mud-input-helper-text')]")
    FLD_GHI_CHU = (By.XPATH, "//div[@data-column-key='GhiChu']//input")

    FLD_CHUC_VU = (By.XPATH, "//div[@data-column-key='ChucVu']//input")
    FLD_NOI_LAM_VIEC = (By.XPATH, "//div[@data-column-key='NoiLamViec']//input")
    FLD_TINH_THANH = (By.XPATH, "//div[@data-column-key='TinhThanh']//input")
    FLD_QUAN_HUYEN = (By.XPATH, "//div[@data-column-key='QuanHuyen']//input")

    FLD_SO_TAI_KHOAN = (By.XPATH, "//div[@data-column-key='SoTaiKhoan']//input")
    FLD_TINH_NGAN_HANG = (By.XPATH, "//div[@data-column-key='MaTinh_NH']//input")
    FLD_TEN_NGAN_HANG = (By.XPATH, "//div[@data-column-key='MaNganHang']//input")

    FLD_SO_HOP_DONG = (By.XPATH, "//div[@data-column-key='SoHopDong']//input")
    FLD_NGAY_KY_HD = (By.XPATH, "//div[@data-column-key='NgayKyHd']//input")
    FLD_LOAI_HOP_DONG = (By.XPATH, "//div[@data-column-key='LoaiHopDong']//input")
    FLD_XUAT_TK1 = (By.XPATH, "//div[@data-column-key='XuatTk1']//input")

    def navigate_to_d02(self):
        logger.info("Đang điều hướng tới thủ tục 600")
        self.wait_for_load()
        self.wait_for_spinner_gone()

        try:
            self.wait_and_click(self.SEL_THU_TUC_600)
            popup_close_xpath = "//button[contains(., 'Để sau')] | //button[contains(., 'Đóng')] | //button[contains(@class, 'mud-button-close')]"
            btns = self.driver.find_elements(By.XPATH, popup_close_xpath)
            for btn in btns:
                if btn.is_displayed():
                    btn.click()
        except Exception as e:
            logger.error(f"Lỗi điều hướng hoặc không có popup: {e}")

        self.wait_for_spinner_gone()

    def click_tao_dot_moi(self):
        self.wait_for_spinner_gone()

        btn_tao = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.BTN_TAO_DOT_MOI))
        self.driver.execute_script("arguments[0].click();", btn_tao)
        logger.info("Đã nhấn 'Tạo đợt kê khai'")

        self.wait_for_spinner_gone()
        time.sleep(2)

        try:
            btn_them = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.BTN_THEM_MOI_DONG))
            # Dùng JavaScript click để tránh lỗi bị che bởi các tooltip/spinner
            self.driver.execute_script("arguments[0].click();", btn_them)
            logger.info("Đã nhấn nút 'Thêm mới' dòng")
        except Exception as e:
            logger.error(f"Không tìm thấy nút Thêm mới dòng: {e}")
            raise

        self.wait_for_spinner_gone()

        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(self.FLD_HO_TEN))

    def select_mud_dropdown(self, locator, value):
        try:
            logger.info(f"Đang chọn giá trị '{value}' tại {locator}")

            wait = WebDriverWait(self.driver, 10)
            el = wait.until(EC.presence_of_element_located(locator))

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            self.driver.execute_script("arguments[0].click();", el)
            time.sleep(0.5)

            from selenium.webdriver.common.keys import Keys
            el.send_keys(Keys.CONTROL + "a")
            el.send_keys(Keys.DELETE)
            time.sleep(0.2)
            el.send_keys(value)
            time.sleep(1.2)
            el.send_keys(Keys.ENTER)

            el.send_keys(Keys.TAB)

            self.wait_for_spinner_gone()
            logger.info(f"Đã chọn thành công: {value}")

        except Exception as e:
            logger.error(f"LỖI TẠI DROPDOWN '{value}': {str(e)}")
            raise e

    def fill_lao_dong(self, data):
        logger.info(f"Đang điền dữ liệu cho lao động: {data.get('ho_ten', 'N/A')}")

        self.driver.execute_script(
            "var el = document.querySelector('.mud-table-container');"
            "if(el) { el.scrollLeft = el.scrollWidth; }"  # Cuộn kịch sàn sang phải
        )
        time.sleep(1.5)

        if "ho_ten" in data: self.send_keys(self.FLD_HO_TEN, data["ho_ten"])
        if "so_so" in data: self.send_keys(self.FLD_SO_SO, data["so_so"])
        if "ma_so_bhxh" in data: self.send_keys(self.FLD_MA_SO_BHXH, data["ma_so_bhxh"])
        if "ngay_sinh" in data: self.send_keys(self.FLD_NGAY_SINH, data["ngay_sinh"])

        if "gioi_tinh" in data:
            self.select_mud_dropdown(self.FLD_GIOI_TINH, data["gioi_tinh"])

        if "tien_luong" in data: self.send_keys(self.FLD_TIEN_LUONG, str(data["tien_luong"]))
        if "phu_cap_cv" in data: self.send_keys(self.FLD_PHU_CAP_CV, str(data["phu_cap_cv"]))
        if "phu_cap_tn" in data: self.send_keys(self.FLD_PHU_CAP_TN, str(data["phu_cap_tn"]))
        if "phu_cap_tnn" in data: self.send_keys(self.FLD_PHU_CAP_TNN, str(data["phu_cap_tnn"]))

        if "tu_thang" in data: self.send_keys(self.FLD_TU_THANG, data["tu_thang"])
        if "den_thang" in data: self.send_keys(self.FLD_DEN_THANG, data["den_thang"])

        if "phu_luc" in data:
            self.select_mud_dropdown(self.FLD_PHU_LUC, data["phu_luc"])
        if "loai_doi_tuong" in data:
            self.select_mud_dropdown(self.FLD_LOAI_DOI_TUONG, data["loai_doi_tuong"])

        if "phu_chu" in data: self.send_keys(self.FLD_PHU_CHU, data["phu_chu"])
        if "ghi_chu" in data: self.send_keys(self.FLD_GHI_CHU, data["ghi_chu"])

        if "so_hop_dong" in data:
            self.send_keys(self.FLD_SO_HOP_DONG, data["so_hop_dong"])

        if "ngay_ky_hd" in data:
            self.send_keys(self.FLD_NGAY_KY_HD, data["ngay_ky_hd"])

        if "tinh_ngan_hang" in data:
            self.select_mud_dropdown(self.FLD_TINH_NGAN_HANG, data["tinh_ngan_hang"])

        if "ten_ngan_hang" in data:
            self.select_mud_dropdown(self.FLD_TEN_NGAN_HANG, data["ten_ngan_hang"])

    def click_save(self):
        self.wait_and_click(self.BTN_LUU)
        self.wait_for_spinner_gone()
        time.sleep(1)

    def delete_all(self):
        el = self.driver.find_element(*self.BTN_XOA_TAT_CA)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)

        self.wait_and_click(self.BTN_XOA_TAT_CA)

        btn_confirm = (By.XPATH,
                       "//div[contains(@class, 'mud-dialog')]//button[contains(@class, 'mud-button-filled-primary')] | //button[contains(., 'Đồng ý')]")

        self.wait_and_click(btn_confirm, timeout=5000)
        self.wait_for_spinner_gone()

