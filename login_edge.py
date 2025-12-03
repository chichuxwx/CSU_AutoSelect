import time
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



EDGEDRIVER_PATH = "msedgedriver.exe"  # 你的 msedgedriver.exe
LOGIN_URL = "https://ca.csu.edu.cn/authserver/login?service=http%3A%2F%2Fcsujwc.its.csu.edu.cn%2Fsso.jsp"

USERNAME = ""
PASSWORD = ""

JWC_MAIN_URL = "http://csujwc.its.csu.edu.cn/jsxsd/framework/xsMain.jsp"



def login_with_edge_offline(username, password):
    print("[*] 启动 Microsoft Edge...")

    options = Options()
    options.use_chromium = True
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(executable_path=EDGEDRIVER_PATH)
    driver = webdriver.Edge(service=service, options=options)

    print("[*] 打开 CSU 登录页...")
    driver.get(LOGIN_URL)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "username")))

    print("[*] 填写账号密码...")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)

    try:
        captcha_area = driver.find_element(By.ID, "captchaDiv")
        if captcha_area.is_displayed():
            print("[!] 检测到验证码，请手动输入后点击登录")
            input("完成验证码后按回车继续...")
    except:
        pass

    btn = wait.until(EC.element_to_be_clickable((By.ID, "login_submit")))
    btn.click()

    print("[*] 已提交登录，等待跳转...")
    time.sleep(3)
    return driver



def export_cookie_session(driver):
    session = requests.Session()
    session.trust_env = False

    for c in driver.get_cookies():
        session.cookies.set(c["name"], c["value"], domain=c.get("domain"))

    print("[*] 用 session 访问教务系统测试...")
    r = session.get(JWC_MAIN_URL)
    print("状态码:", r.status_code)
    print("页面前200字符：\n", r.text[:200])

    return session


if __name__ == "__main__":
    driver = login_with_edge_offline()
    session = export_cookie_session(driver)

    print("\n🎉 离线版登录成功！接下来可以继续自动抢课。")
    input("按回车退出...")
