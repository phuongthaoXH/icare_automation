import random
import string
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class TaiKhoanPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    SPINNER_XPATH = "//div[contains(@class, 'mud-loading-indicator') or contains(@class, 'mud-wasm-loading')]"

    BTN_THEM_MOI = (By.XPATH, "//button[contains(., 'Thêm mới')]")
    INPUT_TEN_DANG_NHAP = (By.XPATH, "//input[@placeholder='Tên đăng nhập']")
    BTN_CHECK_TEN = (By.XPATH, "//input[@placeholder='Tên đăng nhập']/following-sibling::div//button")
    INPUT_EMAIL = (By.XPATH, "//input[@placeholder='Email']")
    INPUT_MAT_KHAU = (By.XPATH, "//input[@placeholder='Nhập mật khẩu']")
    BTN_SHOW_PASS = (By.XPATH, "//input[@placeholder='Nhập mật khẩu']/following-sibling::div//button")
    INPUT_RE_MAT_KHAU = (By.XPATH, "//input[@placeholder='Nhập lại mật khẩu']")
    BTN_SHOW_RE_PASS = (By.XPATH, "//input[@placeholder='Nhập lại mật khẩu']/following-sibling::div//button")
    CB_QUAN_LY_NHAN_SU = (By.XPATH, "//p[text()='Quản lý nhân sự']/preceding-sibling::span//input")
    BTN_LUU = (By.XPATH, "//button[span[text()='Lưu']]")

    LBL_LOI_TEN_TON_TAI = (By.XPATH, "//span[contains(text(), 'Tên đăng nhập đã tồn tại')]")
    LBL_LOI_EMAIL_SAI = (By.XPATH, "//div[contains(text(), 'Dữ liệu không hợp lệ.')]")
    LBL_LOI_MAT_KHAU_KHONG_KHOP = (By.XPATH, "//div[contains(text(), 'Mật khẩu nhập lại không khớp')]")
    LBL_LOI_THIEU_KY_TU_DAC_BIET = (By.XPATH, "//div[contains(text(), 'Mật khẩu phải có ít nhất 1 ký tự đặc biệt')]")
    LBL_LOI_THIEU_CHU_THUONG = (By.XPATH, "//div[contains(text(), 'Mật khẩu phải có ít nhất 1 chữ thường (a-z)')]")
    LBL_LOI_THIEU_CHU_HOA = (By.XPATH, "//div[contains(text(), 'Mật khẩu phải có ít nhất 1 chữ hoa (A-Z)')]")

    LBL_LOI_THIEU_QUYEN = (By.XPATH, "//span[contains(text(), 'Vui lòng chọn ít nhất một quyền')]")
    LBL_LOI_VUI_LONG_NHAP_USER = (By.XPATH, "//div[contains(text(), 'Vui lòng nhập tên đăng nhập')]")
    LBL_LOI_EMAIL_TRONG = (By.XPATH, "//div[contains(text(), 'Trường không được trống.')]")
    LBL_LOI_MAT_KHAU_TRONG = (By.XPATH, "//div[contains(text(), 'Mật khẩu không được để trống')]")

    LBL_LOI_DO_DAI_USER = (By.XPATH, "//div[contains(text(), 'Tên đăng nhập phải từ 6 đến 25 ký tự')]")
    LBL_LOI_DO_DAI_MAT_KHAU = (By.XPATH, "//div[contains(text(), 'Mật khẩu phải có ít nhất 6 ký tự')]")

    BTN_CAU_HINH_QUYEN = (By.XPATH,"//table//tbody//tr[1]//button[contains(@class, 'mud-icon-button') and .//*[local-name()='svg']]")
    CB_LAP_KE_KHAI_HO_SO = (By.XPATH, "//p[text()='Lập, kê khai hồ sơ']/ancestor::label")

    BTN_SUA_TAI_KHOAN = (By.XPATH, "(//table//tbody//tr)[1]//div[contains(@class,'mud-tooltip-root')][2]//button")
    CB_LAP_KE_KHAI_SUA = (By.XPATH, "//p[contains(., 'Lập, kê khai hồ sơ')]/ancestor::label//input[@type='checkbox']")

    BTN_RESET_MAT_KHAU = (By.XPATH,"(//table//tbody//tr)[1]//div[contains(@class,'mud-tooltip-root')][3]//button")

    BTN_XOA_TAI_KHOAN = (By.XPATH,"(//table//tbody//tr)[1]//div[contains(@class,'mud-tooltip-root')][4]//button")
    BTN_DONG_Y_XOA = (By.XPATH,"//button[contains(@class,'mud-button-filled-primary')]//span[text()='Đồng ý']")
    CB_CHON_DONG_1 = (By.XPATH, "(//table//tbody//tr)[1]//input[@type='checkbox']")
    CB_CHON_DONG_2 = (By.XPATH, "(//table//tbody//tr)[2]//input[@type='checkbox']")
    BTN_XOA_CHON = (By.XPATH,"//button[contains(@class,'mud-button-filled-error')]//span[contains(text(),'Xoá chọn')]")

    INPUT_TIM_KIEM_TEN = (By.XPATH, "//input[@placeholder='Tìm kiếm theo tên đăng nhập']")
    INPUT_SELECT_VAI_TRO = (By.XPATH, "//input[@placeholder='Tìm kiếm theo Vai trò']")
    DDL_TRANG_THAI = (By.XPATH, "//input[@placeholder='Tìm kiếm theo trạng thái']")

    def wait_for_spinner_gone(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.invisibility_of_element_located((By.XPATH, self.SPINNER_XPATH))
            )
        except Exception as e:
            print(f"Lưu ý: Không tìm thấy spinner hoặc chờ quá lâu: {e}")
            pass

    def click_them_moi(self):
        self.wait.until(EC.element_to_be_clickable(self.BTN_THEM_MOI)).click()

    def generate_random_username(self):
        letters_and_digits = string.ascii_lowercase + string.digits
        return "user_" + ''.join(random.choice(letters_and_digits) for i in range(8))

    def nhap_ten_dang_nhap_va_tra_cuu(self, username):
        user_input = self.wait.until(EC.visibility_of_element_located(self.INPUT_TEN_DANG_NHAP))
        user_input.clear()
        user_input.send_keys(username)
        time.sleep(2)

        self.wait.until(EC.element_to_be_clickable(self.BTN_CHECK_TEN)).click()
        time.sleep(2)

    def nhap_thong_tin_tai_khoan(self, username, email, password, re_password=None):
        self.nhap_ten_dang_nhap_va_tra_cuu(username)

        email_input = self.wait.until(EC.visibility_of_element_located(self.INPUT_EMAIL))
        email_input.clear()
        email_input.send_keys(email)
        time.sleep(2)

        self.wait.until(EC.visibility_of_element_located(self.INPUT_MAT_KHAU)).send_keys(password)
        self.driver.find_element(*self.BTN_SHOW_PASS).click()
        time.sleep(2)

        confirm_val = re_password if re_password is not None else password

        re_pass_input = self.wait.until(EC.visibility_of_element_located(self.INPUT_RE_MAT_KHAU))
        re_pass_input.clear()
        re_pass_input.send_keys(confirm_val)
        self.driver.find_element(*self.BTN_SHOW_RE_PASS).click()
        time.sleep(2)

    def chon_quyen_va_luu(self):
        cb = self.driver.find_element(*self.CB_QUAN_LY_NHAN_SU)
        if not cb.is_selected():
            self.driver.execute_script("arguments[0].click();", cb)
            time.sleep(2)

        self.driver.find_element(*self.BTN_LUU).click()
        time.sleep(2)

    def is_thong_bao_ton_tai_hien_thi(self):
        try:
            error_msg = self.wait.until(EC.visibility_of_element_located(self.LBL_LOI_TEN_TON_TAI))
            return error_msg.is_displayed()
        except:
            return False

    def is_thong_bao_email_sai_hien_thi(self):
        try:
            error_msg = self.wait.until(EC.visibility_of_element_located(self.LBL_LOI_EMAIL_SAI))
            return error_msg.is_displayed()
        except:
            return False

    def is_thong_bao_mat_khau_khong_khop_hien_thi(self):
        try:
            error_msg = self.wait.until(EC.visibility_of_element_located(self.LBL_LOI_MAT_KHAU_KHONG_KHOP))
            return error_msg.is_displayed()
        except:
            return False

    def is_thong_bao_thieu_ky_tu_dac_biet_hien_thi(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.LBL_LOI_THIEU_KY_TU_DAC_BIET)).is_displayed()
        except:
            return False

    def is_thong_bao_thieu_chu_thuong_hien_thi(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.LBL_LOI_THIEU_CHU_THUONG)).is_displayed()
        except:
            return False

    def is_thong_bao_thieu_chu_hoa_hien_thi(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.LBL_LOI_THIEU_CHU_HOA)).is_displayed()
        except:
            return False

    def is_thong_bao_thieu_quyen_hien_thi(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.LBL_LOI_THIEU_QUYEN)).is_displayed()
        except:
            return False

    def is_thong_bao_vui_long_nhap_user_hien_thi(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.LBL_LOI_VUI_LONG_NHAP_USER)).is_displayed()
        except:
            return False

    def is_thong_bao_email_trong_hien_thi(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.LBL_LOI_EMAIL_TRONG)).is_displayed()
        except:
            return False

    def is_thong_bao_mat_khau_trong_hien_thi(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.LBL_LOI_MAT_KHAU_TRONG)).is_displayed()
        except:
            return False

    def is_thong_bao_do_dai_user_hien_thi(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.LBL_LOI_DO_DAI_USER)).is_displayed()
        except:
            return False

    def is_thong_bao_do_dai_mat_khau_hien_thi(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.LBL_LOI_DO_DAI_MAT_KHAU)).is_displayed()
        except:
            return False

    def click_icon_cau_hinh_quyen(self):
        self.wait.until(EC.element_to_be_clickable(self.BTN_CAU_HINH_QUYEN)).click()

    def tich_chon_quyen_lap_ke_khai(self):
        label_element = self.wait.until(EC.element_to_be_clickable(self.CB_LAP_KE_KHAI_HO_SO))
        label_element.click()

    def click_luu_phan_quyen(self):
        self.wait.until(EC.element_to_be_clickable(self.BTN_LUU)).click()

    def phan_quyen_tai_khoan(self):
        self.click_icon_cau_hinh_quyen()
        time.sleep(2)  # Chờ modal popup render xong hoàn toàn

        self.tich_chon_quyen_lap_ke_khai()
        time.sleep(1)

        self.click_luu_phan_quyen()
        time.sleep(2)

    def click_icon_chinh_sua(self):
        print("Đang đợi bảng tài khoản tải dữ liệu...")

        ICON_PHAN_QUYEN_XANH = (By.XPATH, "(//table//tbody//tr)[1]//button[1]")
        self.wait.until(EC.visibility_of_element_located(ICON_PHAN_QUYEN_XANH))
        time.sleep(1.5)

        print("Bảng đã load xong. Đang tìm nút Chỉnh sửa (button thứ 2)...")

        btn_sua = self.wait.until(EC.presence_of_element_located(self.BTN_SUA_TAI_KHOAN))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            btn_sua
        )
        time.sleep(0.5)

        self.driver.execute_script("arguments[0].click();", btn_sua)
        print("-> Đã click thành công nút Sửa tài khoản!")

    def sua_thong_tin_email(self, email):
        email_input = self.wait.until(EC.visibility_of_element_located(self.INPUT_EMAIL))
        email_input.clear()
        email_input.send_keys(email)
        time.sleep(2)
        print(f"-> Đã nhập email mới: {email}")

    def chon_them_quyen_lap_ke_khai(self):
        print("Đang kiểm tra trạng thái checkbox 'Lập, kê khai hồ sơ'...")

        checkbox_input = self.wait.until(EC.presence_of_element_located(self.CB_LAP_KE_KHAI_SUA))

        is_checked = checkbox_input.is_selected()

        if not is_checked:
            print("-> Checkbox đang trống. Tiến hành tích chọn...")
            self.driver.execute_script("arguments[0].click();", checkbox_input)
            print("-> Đã tích chọn thành công quyền: Lập, kê khai hồ sơ.")
        else:
            print("-> Quyền 'Lập, kê khai hồ sơ' đã được tích chọn sẵn từ trước, bỏ qua không click lại.")

    def click_luu_chinh_sua(self):
        btn_luu = self.wait.until(EC.element_to_be_clickable(self.BTN_LUU))
        btn_luu.click()
        print("-> Đã nhấn nút Lưu thay đổi.")

    def chinh_sua_tai_khoan(self, email):
        self.click_icon_chinh_sua()
        time.sleep(2.5)

        self.sua_thong_tin_email(email)
        time.sleep(2)

        self.chon_them_quyen_lap_ke_khai()
        time.sleep(2)

        self.click_luu_chinh_sua()
        time.sleep(2)

    def click_icon_reset_mat_khau(self):
        print("Đang tìm nút Đặt lại mật khẩu...")
        ICON_PHAN_QUYEN = (By.XPATH, "(//table//tbody//tr)[1]//button[1]")
        self.wait.until(EC.visibility_of_element_located(ICON_PHAN_QUYEN))
        time.sleep(1.5)

        btn_reset = self.wait.until(EC.presence_of_element_located(self.BTN_RESET_MAT_KHAU))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", btn_reset
        )
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", btn_reset)
        print("-> Đã click thành công nút Đặt lại mật khẩu!")

    def click_show_mat_khau(self):
        btn_show = self.wait.until(EC.element_to_be_clickable(self.BTN_SHOW_PASS))
        self.driver.execute_script("arguments[0].click();", btn_show)
        print("-> Đã click hiện mật khẩu.")

    def click_show_nhap_lai_mat_khau(self):
        btn_show = self.wait.until(EC.element_to_be_clickable(self.BTN_SHOW_RE_PASS))
        self.driver.execute_script("arguments[0].click();", btn_show)
        print("-> Đã click hiện lại mật khẩu.")

    def nhap_mat_khau_moi(self, password_moi):
        txt_mat_khau = self.wait.until(EC.visibility_of_element_located(self.INPUT_MAT_KHAU))
        txt_mat_khau.clear()
        txt_mat_khau.send_keys(password_moi)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", txt_mat_khau)
        self.driver.execute_script("arguments[0].blur();", txt_mat_khau)
        print("-> Đã nhập mật khẩu mới.")
        time.sleep(2)
        self.click_show_mat_khau()

        txt_nhap_lai = self.wait.until(EC.visibility_of_element_located(self.INPUT_RE_MAT_KHAU))
        txt_nhap_lai.clear()
        txt_nhap_lai.send_keys(password_moi)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", txt_nhap_lai)
        self.driver.execute_script("arguments[0].blur();", txt_nhap_lai)

        print("-> Đã nhập xác nhận lại mật khẩu.")
        time.sleep(2)
        self.click_show_nhap_lai_mat_khau()

    def click_luu_reset_mat_khau(self):
        btn_luu = self.wait.until(EC.element_to_be_clickable(self.BTN_LUU))
        btn_luu.click()
        print("-> Đã nhấn nút Lưu thay đổi mật khẩu.")

    def dat_lai_mat_khau_tai_khoan(self, password_moi):
        self.click_icon_reset_mat_khau()
        time.sleep(2)

        self.nhap_mat_khau_moi(password_moi)
        time.sleep(2)

        self.click_luu_reset_mat_khau()
        time.sleep(2)

    def click_icon_xoa_tai_khoan(self):
        print("Đang tìm nút Xóa tài khoản...")
        ICON_PHAN_QUYEN = (By.XPATH, "(//table//tbody//tr)[1]//button[1]")
        self.wait.until(EC.visibility_of_element_located(ICON_PHAN_QUYEN))
        time.sleep(1.5)

        btn_xoa = self.wait.until(EC.presence_of_element_located(self.BTN_XOA_TAI_KHOAN))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", btn_xoa
        )
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", btn_xoa)
        print("-> Đã click nút Xóa tài khoản!")

    def click_dong_y_xoa(self):
        btn_dong_y = self.wait.until(EC.element_to_be_clickable(self.BTN_DONG_Y_XOA))
        self.driver.execute_script("arguments[0].click();", btn_dong_y)
        print("-> Đã nhấn Đồng ý xóa tài khoản!")

    def xoa_tai_khoan(self):
        self.click_icon_xoa_tai_khoan()
        time.sleep(1.5)

        self.click_dong_y_xoa()
        time.sleep(2)

    def click_checkbox_dong(self, locator):
        cb = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", cb
        )
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", cb)
        print(f"-> Đã tích checkbox dòng.")

    def click_nut_xoa_chon(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.BTN_XOA_CHON))
        self.driver.execute_script("arguments[0].click();", btn)
        print("-> Đã click nút Xoá chọn.")

    def xoa_nhieu_tai_khoan(self):
        self.click_checkbox_dong(self.CB_CHON_DONG_1)
        time.sleep(0.5)

        self.click_checkbox_dong(self.CB_CHON_DONG_2)
        time.sleep(0.5)

        self.click_nut_xoa_chon()
        time.sleep(1.5)

        self.click_dong_y_xoa()
        time.sleep(2)

    def tim_kiem_theo_ten(self, tu_khoa):
        print(f"-> Đang tìm kiếm với từ khóa: {tu_khoa}")
        # Dùng self.wait đã có sẵn trong class Page
        search_input = self.wait.until(EC.visibility_of_element_located(self.INPUT_TIM_KIEM_TEN))
        search_input.clear()
        search_input.send_keys(tu_khoa)
        search_input.send_keys(Keys.ENTER)
        time.sleep(2)

    def chon_vai_tro(self, ten_vai_tro):
        print(f"-> Đang chọn vai trò: {ten_vai_tro}")
        select_box = self.wait.until(EC.element_to_be_clickable(self.INPUT_SELECT_VAI_TRO))
        select_box.click()
        time.sleep(1)
        item_xpath = f"//div[contains(@class, 'mud-list-item')]//p[text()='{ten_vai_tro}']"
        try:
            item = self.wait.until(EC.visibility_of_element_located((By.XPATH, item_xpath)))
            item.click()
            print(f"-> Đã chọn xong vai trò: {ten_vai_tro}")
        except Exception as e:
            print(f"-> Không tìm thấy vai trò {ten_vai_tro}. Lỗi: {e}")
            raise
        time.sleep(3)

    def chon_trang_thai(self, ten_trang_thai):
        print(f"-> Đang chọn trạng thái: {ten_trang_thai}")
        select_box = self.wait.until(EC.element_to_be_clickable(self.DDL_TRANG_THAI))
        select_box.click()
        time.sleep(1)
        item_xpath = f"//div[contains(@class, 'mud-list-item')]//p[text()='{ten_trang_thai}']"
        try:
            item = self.wait.until(EC.visibility_of_element_located((By.XPATH, item_xpath)))
            item.click()
            print(f"-> Đã chọn xong trạng thái: {ten_trang_thai}")
        except Exception as e:
            print(f"-> Không tìm thấy trạng thái {ten_trang_thai}. Lỗi: {e}")
            raise
        time.sleep(3)