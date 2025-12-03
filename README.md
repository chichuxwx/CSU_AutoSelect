# CSUAutoSelect-Selenium

中南大学自动选课工具

原始作者：[@DavidHuang](https://github.com/CrazyDaveHDY)

更新：[@chichuxwx](https://github.com/chichuxwx)

本项目使用 Selenium 完成 CSU 统一认证登录，再将 Cookies 注入 requests，实现高速抢课。

---

## 功能特性

- 使用 Selenium 自动登录 CSU 统一认证平台
- 支持验证码（若出现则手动输入）
- 登录成功后自动跳转到教务系统主页
- 自动导出浏览器 Cookies 注入 requests.Session
- 支持公选课与体育/专业课两种选课接口
- 配置文件化（config.ini）
- 自动循环抢课，直到成功

---

## 环境要求

Python 3.9（Selenium 4）

必须安装依赖：

```Shell
pip install selenium requests
```

## Edge 浏览器驱动

1. 打开 Edge → 地址栏输入：
```Shell
edge://version/
```

2. 查看浏览器版本（如 142.x.x）
3. 前往[官方](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)下载对应版本 EdgeDriver：


4. 下载后将 `msedgedriver.exe` 放到项目目录  
并在 login_edge.py 中设置EDGEDRIVER_PATH

## 运行 

首先修改config.ini，根据config中内容修改账号密码，以及填写要抢课的ID，下面展示了如何找到课程ID 

按照提示输入学号，教务系统密码，课程 ID 后，进入项目根目录，命令行中运行

```Shell
 python3 main.py
```

## 如何找到6位课程ID 

1. 课程 ID 查找方法：在 [中南大学教务系统课表查询页面](http://csujwc.its.csu.edu.cn/jiaowu/pkgl/llsykb/llsykb_find_jg0101.jsp?xnxq01id=2022-2023-2&init=1&isview=0) 中点击「按教师」按钮，输入学年学期、教师名称后点击「查询」，格子中央的 6 位数字编号即为课程 ID，这样可以找到公选和体育的ID、 ![课程 ID.png](https://i.loli.net/2021/01/13/G7mN9BUzpaHRtkw.png) 

2.在查询页面按照时间查询，里面课表都有id 

## 声明 

因为每学期选课的包可能都会发生变化，当前代码仅能在上传时的学期抢课，不保证抢课成功 该程序仅保存账户密码在本地，不会危害到你的账户安全  

使用时注意不要对中南大学服务器造成太大负担，本程序仅做技术交流，一切后果使用者自负。

## 许可协议 

CSUAutoSelect [GPL-3.0 License](https://github.com/CrazyDaveHDY/CSUAutoSelect/blob/master/LICENSE)