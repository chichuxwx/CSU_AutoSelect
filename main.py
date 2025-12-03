# coding: utf-8
import configparser
from login_edge import login_with_edge_offline, export_cookie_session
from autoselect import AutoSelector


def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")

    cfg = config["config"]

    username = cfg.get("username")
    password = cfg.get("password")
    semester = cfg.get("time")

    num1 = cfg.getint("num1")
    public_ids = [
        cfg.get(f"id{i}") for i in range(1, num1 + 1)
    ]

    num2 = cfg.getint("num2")
    major_ids = [
        cfg.get(f"id_{i}") for i in range(1, num2 + 1)
    ]

    print("\n========================")
    print("配置读取成功：")
    print("账号：", username)
    print("学期：", semester)
    print("公选：", public_ids)
    print("专业课：", major_ids)
    print("========================\n")

    return username, password, semester, public_ids, major_ids


def main():
    username, password, semester, public_ids, major_ids = load_config()

    driver = login_with_edge_offline(username, password)

    session = export_cookie_session(driver)

    selector = AutoSelector(session, semester)

    for cid in public_ids:
        selector.add_public_course(cid)

    for cid in major_ids:
        selector.add_major_course(cid)

    selector.start()

    input("\n全部完成！按回车退出...")


if __name__ == "__main__":
    main()
