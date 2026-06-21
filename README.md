# iCare BHXH – Automated Test Suite

Bộ kiểm thử tự động cho hệ thống **iCare** | Màn hình: **Tờ khai D02 (Thủ tục 600)**

## 📂 Cấu trúc

```
icare_automation/
├── config/settings.py       # URL, credentials, timeout, test data
├── pages/
│   ├── base_page.py         # Lớp cơ sở: click, fill, wait, screenshot
│   ├── login_page.py        # Trang đăng nhập
│   ├── dashboard_page.py    # Navigation
│   └── d02_page.py          # Tờ khai D02 (core POM)
├── tests/
│   ├── test_01_login.py     # Đăng nhập (8 TC)
│   ├── test_02_giao_dien.py # Giao diện UI (13 TC)
│   ├── test_03_chuc_nang.py # Chức năng + Edge case (15 TC)
│   ├── test_04_validate.py  # Validate fields (25 TC)
│   ├── test_05_phan_quyen.py# Phân quyền + Bảo mật (11 TC)
│   └── test_06_exploratory.py # Exploratory (7 TC)
├── utils/helpers.py         # Excel generator, reporter, retry
├── conftest.py              # Fixtures: browser, login, d02_page
├── pytest.ini               # Config pytest + markers
├── requirements.txt
├── run_tests.sh             # Script chạy nhanh
└── .env.example             # Template biến môi trường
```

## 🚀 Cài đặt

```bash
pip install -r requirements.txt
python -m playwright install chromium
cp .env.example .env
```

## ▶️ Chạy test

```bash
# Tất cả
python -m pytest

# Theo nhóm
python -m pytest -m smoke          # Nhanh, cover luồng chính
python -m pytest -m giao_dien      # UI tests
python -m pytest -m chuc_nang      # Functional tests
python -m pytest -m validate       # Validate fields
python -m pytest -m phan_quyen     # Phân quyền & bảo mật
python -m pytest -m exploratory    # Exploratory

# Debug – xem browser
HEADLESS=false SLOW_MO=600 python -m pytest -s tests/login_test.py

# Song song (nhanh hơn)
python -m pytest -n 4 --dist=loadfile
```

## 📊 Báo cáo

| Loại | Đường dẫn |
|------|-----------|
| HTML report | `reports/report_<timestamp>.html` |
| Excel kết quả | `reports/results_<timestamp>.xlsx` |
| Screenshot lỗi | `screenshots/FAIL_<test>.png` |

## 📋 Tổng hợp TC

| Module | TC | Markers |
|--------|----|---------|
| Đăng nhập | 8 | smoke |
| Giao diện | 13 | giao_dien |
| Chức năng chính | 15 | chuc_nang |
| Validate fields | 25 | validate |
| Phân quyền & bảo mật | 11 | phan_quyen |
| Exploratory | 7 | exploratory |
| **Tổng** | **~79** | |

## 🔧 Troubleshooting

| Lỗi | Giải pháp |
|-----|-----------|
| `TimeoutError` | Tăng `DEFAULT_TIMEOUT` trong `config/settings.py` |
| `Login failed` | Kiểm tra credentials trong `.env` |
| Selector không tìm thấy | Cập nhật selector trong `pages/d02_page.py` |
| Tests pass local, fail CI | Thêm `--no-sandbox` vào browser args trong `conftest.py` |
