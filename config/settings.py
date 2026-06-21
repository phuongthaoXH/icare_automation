
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL   = os.getenv("BASE_URL",  "https://test.tokhaibaohiem.vn")
LOGIN_URL  = f"{BASE_URL}/dang-nhap"

VALID_USER     = os.getenv("TEST_USER",     "0107489961_ICARE01")
VALID_PASSWORD = os.getenv("TEST_PASSWORD", "12345678aA@")


DEFAULT_TIMEOUT   = 30
ELEMENT_TIMEOUT   = 15
ACTION_TIMEOUT    = 5
SLOW_TIMEOUT      = 60

HEADLESS      = os.getenv("HEADLESS", "false").lower() == "true"


SLOW_MO       = int(os.getenv("SLOW_MO", "0"))

VIEWPORT      = {"width": 1366, "height": 768}

THANG_NAM_TEST = "01/2025"

VALID_LAO_DONG = {
    "ho_ten":          "Nguyễn Thị Lan Test",
    "loai_phuong_an":  "Tham gia BHXH, BHYT, BHTN",
    "phuong_an":       "Tăng mới",
    "loai_ngay_sinh":  "Ngày/Tháng/Năm",
    "ngay_sinh":       "15/03/1990",
    "gioi_tinh":       "Nữ",
    "cmnd":            "034090012345",
    "chuc_vu":         "Nhân viên",
    "so_hdld":         "HD-AUTO-001",
    "ngay_ky":         "01/01/2025",
    "tu_thang":        "01/2025",
    "den_thang":       "12/2025",
    "noi_lam_viec":    "Hà Nội",
    "ty_le_dong":      "8",
    "tien_luong":      "5000000",
}

BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
REPORT_DIR     = os.path.join(BASE_DIR, "reports")
EXCEL_RESULT   = os.path.join(REPORT_DIR, "TestCase_D02_Results.xlsx")

for path in [SCREENSHOT_DIR, REPORT_DIR]:
    os.makedirs(path, exist_ok=True)

