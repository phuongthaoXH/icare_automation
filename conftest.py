"""
conftest.py – Đã tối ưu hóa để xử lý Popup và ổn định fixture
"""
import logging
import os
import pytest
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import (
    BASE_URL, VALID_USER, VALID_PASSWORD,
    HEADLESS, VIEWPORT, SCREENSHOT_DIR, REPORT_DIR,
    ELEMENT_TIMEOUT
)
from pages.login_page import LoginPage
from pages.d02_page import D02Page

logger = logging.getLogger(__name__)

@pytest.fixture
def login_page(driver) -> LoginPage:
    """Fixture cung cấp object LoginPage cho các bài test đăng nhập."""
    return LoginPage(driver)

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument(f"--window-size={VIEWPORT['width']},{VIEWPORT['height']}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--lang=vi-VN")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.exclude_switches = ["enable-automation"]

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(ELEMENT_TIMEOUT / 1000)

    yield driver
    driver.quit()


@pytest.fixture
def logged_in_driver(driver):
    """Fixture xử lý login và dọn dẹp các popup cản trở."""
    lp = LoginPage(driver)
    lp.open()
    lp.login(VALID_USER, VALID_PASSWORD)

    # --- XỬ LÝ POPUP MẬT KHẨU (Như trong video của bạn) ---
    try:
        # Chờ tối đa 5s xem có popup "Thay đổi mật khẩu" hoặc thông báo bảo mật không
        popup_close_xpath = "//button[contains(., 'Để sau')] | //button[contains(., 'Đóng')] | //button[contains(@class, 'mud-button-close')]"
        wait = WebDriverWait(driver, 5)
        close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, popup_close_xpath)))
        close_btn.click()
        logger.info("Đã đóng popup cảnh báo hệ thống.")
    except:
        # Nếu không có popup thì bỏ qua
        pass

    return driver


@pytest.fixture
def d02_page(logged_in_driver) -> D02Page:
    dp = D02Page(logged_in_driver)

    # Bước 1: Nhấn menu 600
    dp.navigate_to_d02()

    # Bước 2: Nhấn Tạo đợt (SỬA Ở ĐÂY)
    dp.click_tao_dot_moi()

    return dp

# (Các phần hook makereport và excel giữ nguyên như cũ của bạn)