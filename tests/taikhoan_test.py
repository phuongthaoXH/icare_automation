import pytest
import time

from selenium.webdriver.common.by import By
from pages.taikhoan_page import TaiKhoanPage
from pages.login_page import LoginPage
from selenium.webdriver.support import expected_conditions as EC


class TestTaiKhoan:
    @pytest.fixture(autouse=True)
    def setup(self, driver):  # Sử dụng fixture driver chung của dự án
        self.driver = driver
        self.page = TaiKhoanPage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.driver.get("https://test.tokhaibaohiem.vn/dang-nhap")
        self.login_page.login("0107489961_ICARE01", "12345678aA@")  # Thay bằng acc của bạn
        time.sleep(2)

        self.driver.get("https://test.tokhaibaohiem.vn/quan-ly-tai-khoan")
        self.page.wait_for_spinner_gone()
        time.sleep(2)

    def test_01_them_moi_tai_khoan_thanhcong(self):
        self.page.wait_for_spinner_gone()  # Đợi load trang
        time.sleep(2)

        self.page.click_them_moi()
        time.sleep(3)

        random_user = self.page.generate_random_username()
        pass_test = "Password123!"

        self.page.nhap_thong_tin_tai_khoan(random_user, "test@gmail.com", pass_test)
        time.sleep(3)

        self.page.chon_quyen_va_luu()

        time.sleep(3)
        print(f"TC PASSED: Đã tạo thành công tài khoản: {random_user}")

    def test_them_tai_khoan_da_ton_tai(self):
        self.page.wait_for_spinner_gone()

        self.page.click_them_moi()

        username_ton_tai = "thao03"
        self.page.nhap_ten_dang_nhap_va_tra_cuu(username_ton_tai)

        assert self.page.is_thong_bao_ton_tai_hien_thi() == True
        print(f"PASSED: Đã hiển thị lỗi cho tài khoản trùng: {username_ton_tai}")

    def test_03_them_tai_khoan_email_khong_hop_le(self):
        self.page.click_them_moi()
        time.sleep(2)

        random_user = self.page.generate_random_username()
        email_sai = "test_email_khong_hop_le@@.com"  # Email sai định dạng

        self.page.nhap_thong_tin_tai_khoan(random_user, email_sai, "Password123!")

        self.page.chon_quyen_va_luu()
        time.sleep(2)

        assert self.page.is_thong_bao_email_sai_hien_thi() == True, f"Lỗi: Email {email_sai} sai mà hệ thống không báo 'Dữ liệu không hợp lệ.'"
        print(f"TC03 PASSED: Hệ thống đã chặn thành công Email sai: {email_sai}")

    def test_04_them_tai_khoan_mat_khau_khong_khop(self):
        self.page.click_them_moi()
        time.sleep(2)

        random_user = self.page.generate_random_username()
        pass_chinh = "Password123!"
        pass_nhap_lai_sai = "Password999!"  # Cho sai hoàn toàn

        self.page.nhap_thong_tin_tai_khoan(random_user, "test_repass@gmail.com", pass_chinh, pass_nhap_lai_sai)

        self.page.chon_quyen_va_luu()
        time.sleep(2)

        check_loi = self.page.is_thong_bao_mat_khau_khong_khop_hien_thi()
        assert check_loi == True, "Lỗi: Hệ thống không hiển thị 'Mật khẩu nhập lại không khớp'"

        print(
            f"TC04 PASSED: Hệ thống đã chặn đúng khi mật khẩu nhập lại ({pass_nhap_lai_sai}) không khớp với ({pass_chinh})")

    def test_05_them_tai_khoan_mat_khau_thieu_ky_tu_dac_biet(self):
        self.page.click_them_moi()
        time.sleep(2)

        random_user = self.page.generate_random_username()
        pass_khong_dac_biet = "Password123"

        self.page.nhap_thong_tin_tai_khoan(random_user, "test_pass@gmail.com", pass_khong_dac_biet)

        self.page.chon_quyen_va_luu()
        time.sleep(2)

        check_loi = self.page.is_thong_bao_thieu_ky_tu_dac_biet_hien_thi()
        assert check_loi == True, "Lỗi: Hệ thống không báo 'Mật khẩu phải có ít nhất 1 ký tự đặc biệt'"

        print(f"TC05 PASSED: Hệ thống đã chặn thành công mật khẩu yếu: {pass_khong_dac_biet}")

    def test_06_them_tai_khoan_mat_khau_thieu_chu_thuong(self):
        self.page.click_them_moi()
        time.sleep(2)

        random_user = self.page.generate_random_username()
        pass_thieu_chu_thuong = "PASSWORD123!"

        self.page.nhap_thong_tin_tai_khoan(random_user, "test_lowercase@gmail.com", pass_thieu_chu_thuong)

        self.page.chon_quyen_va_luu()
        time.sleep(2)

        check_loi = self.page.is_thong_bao_thieu_chu_thuong_hien_thi()
        assert check_loi == True, f"Lỗi: Hệ thống không báo 'Mật khẩu phải có ít nhất 1 chữ thường (a-z)' khi nhập {pass_thieu_chu_thuong}"

        print(f"TC06 PASSED: Hệ thống đã chặn thành công mật khẩu thiếu chữ thường.")

    def test_07_them_tai_khoan_mat_khau_thieu_chu_hoa(self):
        self.page.click_them_moi()
        time.sleep(2)

        random_user = self.page.generate_random_username()
        pass_thieu_chu_hoa = "password123!"

        self.page.nhap_thong_tin_tai_khoan(random_user, "test_uppercase@gmail.com", pass_thieu_chu_hoa)

        self.page.chon_quyen_va_luu()
        time.sleep(2)

        check_loi = self.page.is_thong_bao_thieu_chu_hoa_hien_thi()
        assert check_loi == True, f"Lỗi: Hệ thống không báo 'Mật khẩu phải có ít nhất 1 chữ hoa (A-Z)' khi nhập {pass_thieu_chu_hoa}"

        print(f"TC07 PASSED: Hệ thống đã chặn thành công mật khẩu thiếu chữ hoa.")

    def test_08_them_tai_khoan_khong_chon_quyen(self):
        self.page.click_them_moi()
        time.sleep(2)

        random_user = self.page.generate_random_username()

        self.page.nhap_thong_tin_tai_khoan(random_user, "test_permission@gmail.com", "Password123!")

        self.page.wait.until(EC.element_to_be_clickable(self.page.BTN_LUU)).click()
        time.sleep(2)

        check_loi = self.page.is_thong_bao_thieu_quyen_hien_thi()
        assert check_loi == True, "Lỗi: Không hiển thị thông báo 'Vui lòng chọn ít nhất một quyền'"

        print(f"TC08 PASSED: Hệ thống đã chặn thành công khi không chọn quyền quản trị.")

    def test_09_them_tai_khoan_de_trong_ten_dang_nhap(self):
        self.page.click_them_moi()
        time.sleep(2)

        self.page.nhap_thong_tin_tai_khoan("", "test_empty@gmail.com", "Password123!")
        time.sleep(1)

        check_loi = self.page.is_thong_bao_vui_long_nhap_user_hien_thi()
        assert check_loi == True, "Lỗi: Hệ thống không hiển thị 'Vui lòng nhập tên đăng nhập' khi nhấn tra cứu ô trống!"

        print("TC09 PASSED: Hệ thống đã chặn và hiển thị đúng lỗi 'Vui lòng nhập tên đăng nhập' sau khi nhấn tra cứu.")

    def test_10_them_tai_khoan_de_trong_email(self):
        self.page.click_them_moi()
        time.sleep(2)

        random_user = self.page.generate_random_username()
        self.page.nhap_thong_tin_tai_khoan(random_user, "", "Password123!")

        self.page.chon_quyen_va_luu()
        time.sleep(2)

        assert self.page.is_thong_bao_email_trong_hien_thi() == True, "Lỗi: Không hiển thị 'Trường không được trống.' tại ô Email"
        print("TC10 PASSED: Kiểm tra trống Email thành công.")

    def test_11_them_tai_khoan_de_trong_mat_khau(self):
        self.page.click_them_moi()
        time.sleep(2)

        random_user = self.page.generate_random_username()
        self.page.nhap_thong_tin_tai_khoan(random_user, "test_nopass@gmail.com", "")

        self.page.chon_quyen_va_luu()
        time.sleep(2)

        assert self.page.is_thong_bao_mat_khau_trong_hien_thi() == True, "Lỗi: Không hiển thị 'Mật khẩu không được để trống' tại ô Mật khẩu"
        print("TC11 PASSED: Kiểm tra trống Mật khẩu thành công.")

    def test_12_them_tai_khoan_ten_dang_nhap_sai_do_dai(self):
        self.page.click_them_moi()
        time.sleep(2)

        user_ngan = "abc"
        self.page.nhap_thong_tin_tai_khoan(user_ngan, "test_length@gmail.com", "Password123!")
        time.sleep(1)

        check_loi = self.page.is_thong_bao_do_dai_user_hien_thi()
        assert check_loi == True, f"Lỗi: Hệ thống không báo 'Tên đăng nhập phải từ 6 đến 25 ký tự' khi nhập {user_ngan}"

        print("TC12 PASSED: Kiểm tra độ dài Tên đăng nhập thành công.")

    def test_13_them_tai_khoan_mat_khau_sai_do_dai(self):
        time.sleep(2)
        self.page.click_them_moi()
        time.sleep(2)

        random_user = self.page.generate_random_username()
        pass_ngan = "Abc1!"

        self.page.nhap_thong_tin_tai_khoan(random_user, "test_pass_length@gmail.com", pass_ngan)

        self.page.chon_quyen_va_luu()
        time.sleep(2)

        check_loi = self.page.is_thong_bao_do_dai_mat_khau_hien_thi()
        assert check_loi == True, f"Lỗi: Hệ thống không báo 'Mật khẩu phải có ít nhất 6 ký tự' when nhập {pass_ngan}"

        print("TC13 PASSED: Hệ thống đã chặn thành công mật khẩu quá ngắn.")

    def test_14_cau_hinh_phan_quyen_tai_khoan(self):
        time.sleep(2)
        self.page.phan_quyen_tai_khoan()
        print("TC14 PASSED: Thao tác cấu hình phân quyền thành công!")

    def test_15_chinh_sua_tai_khoan(self):
        time.sleep(2)

        email_random = f"edit_test_{int(time.time())}@gmail.com"

        self.page.chinh_sua_tai_khoan(email_random)

        print(f"TC15 PASSED: Đã sửa thành công tài khoản dòng đầu sang email: {email_random} và tích quyền.")

    def test_16_dat_lai_mat_khau(self):
        mat_khau_test = "NewPassword123@"
        self.page.dat_lai_mat_khau_tai_khoan(mat_khau_test)

    def test_17_xoa_tai_khoan(self):
        time.sleep(2)
        ten_tk = self.driver.find_element(
            By.XPATH, "(//table//tbody//tr)[1]//td[1]").text
        print(f"Đang xóa tài khoản: {ten_tk}")

        self.page.xoa_tai_khoan()

        print(f"TC16 PASSED: Đã xóa thành công tài khoản '{ten_tk}'.")

    def test_18_xoa_nhieu_tai_khoan(self):
        time.sleep(2)

        ten_tk_1 = self.driver.find_element(
            By.XPATH, "(//table//tbody//tr)[1]//td[2]"
        ).text
        ten_tk_2 = self.driver.find_element(
            By.XPATH, "(//table//tbody//tr)[2]//td[2]"
        ).text
        print(f"Đang xóa 2 tài khoản: '{ten_tk_1}' và '{ten_tk_2}'")
        self.page.xoa_nhieu_tai_khoan()
        print(f"TC18 PASSED: Đã xóa thành công 2 tài khoản '{ten_tk_1}' và '{ten_tk_2}'.")

    def test_19_tim_kiem_theo_ten(self):
        tu_khoa = "q"
        print(f"Bắt đầu test tìm kiếm với từ khóa: {tu_khoa}")
        self.page.tim_kiem_theo_ten(tu_khoa)
        print("-> Test tìm kiếm hoàn thành.")

    def test_20_tim_kiem_theo_vai_tro(self):
        print("\n--- Đang chạy Test 20: Tìm kiếm theo Vai trò ---")
        vai_tro = "Quản lý nhân sự"
        self.page.chon_vai_tro(vai_tro)
        print("-> Test 20 hoàn thành.")

    def test_21_tim_kiem_theo_trang_thai(self):
        print("\n--- Đang chạy Test 21: Tìm kiếm theo Trạng thái ---")
        trang_thai = "Ngưng"
        self.page.chon_trang_thai(trang_thai)
        print("-> Test 21 hoàn thành.")