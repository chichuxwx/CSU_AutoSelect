# coding=utf-8
import re
import time
import requests


JWC_ROOT = "http://csujwc.its.csu.edu.cn"
XKLC_LIST = JWC_ROOT + "/jsxsd/xsxk/xklc_list"


class AutoSelector:
    def __init__(self, session: requests.Session, semester: str):
        self.session = session
        self.semester = semester

        self.course_ids = []     
        self.course_urls = []    


    def add_public_course(self, short_id: str):
        """公选课"""
        cid = self.semester + short_id
        url = (
            f"{JWC_ROOT}/jsxsd/xsxkkc/ggxxkxkOper?jx0404id={cid}&xkzy=&trjf="
        )
        self.course_ids.append(cid)
        self.course_urls.append(url)

    def add_major_course(self, short_id: str):
        """体育与专业课"""
        cid = self.semester + short_id
        url = (
            f"{JWC_ROOT}/jsxsd/xsxkkc/bxqjhxkOper?jx0404id={cid}&xkzy=&trjf="
        )
        self.course_ids.append(cid)
        self.course_urls.append(url)

    # def enter_xk_page(self):
    #     print("[*] 寻找选课入口...")

    #     while True:
    #         r = self.session.get(XKLC_LIST)
    #         key = re.findall('href="(.+?)" target="blank">进入选课', r.text)

    #         if key:
    #             print("[+] 找到入口：", key[0])
    #             full = JWC_ROOT + key[0]
    #             self.session.get(full)
    #             print("[+] 成功进入选课页面")
    #             return

    #         print("… 未开放，请稍后重试")
    #         time.sleep(20)

    def enter_xk_page(self):
        print("[*] 寻找选课入口...")

        while True:
            r = self.session.get(XKLC_LIST)

            with open("debug_xk_page.html", "w", encoding="utf-8") as f:
                f.write(r.text)

            key = re.findall('href="(.+?)" target="blank">进入选课', r.text)

            if key:
                print("[+] 找到入口：", key[0])
                full = JWC_ROOT + key[0]
                self.session.get(full)
                print("[+] 成功进入选课页面")
                return

            print("… 未开放，请稍后重试")
            time.sleep(20)

    def try_select(self, url, index):
        cid = self.course_ids[index]
        r = self.session.get(url)
        text = r.text

        if "true" in text:
            print(f"[✓] 成功抢到第 {index+1} 门课（ID: {cid}）")
            return True

        if "冲突" in text:
            msg = re.search('"选课失败：(.+)"', text)
            print(f"[!] 课程冲突：{msg.group(1) if msg else ''}")
            return True

        if "null" in text:
            print(f"[x] 课程 ID {cid} 无效")
            return True

        msg = re.search('"选课失败：(.+)"', text)
        print(f"[x] 抢课失败：{msg.group(1) if msg else ''}")
        return False


    def start(self):
        print("[*] 正在准备进入选课系统...")
        self.enter_xk_page()

        print("[*] 开始轮询抢课，共", len(self.course_urls), "门课")

        while self.course_urls:
            index = 0
            for i in range(len(self.course_urls)):
                url = self.course_urls[index]
                cid = self.course_ids[index]

                print(f"[→] 尝试抢课，课程 ID: {cid}")

                ok = self.try_select(url, index)
                if ok:
                    self.course_urls.pop(index)
                    self.course_ids.pop(index)
                else:
                    index += 1 

                time.sleep(20)

        print("\n 所有课程均已处理完毕！")
