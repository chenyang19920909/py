#!/usr/bin/env python
# -*- coding=utf-8 -*-
import unittest
import time
from HTMLTestRunner import HTMLTestRunner
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart


#定义邮件发送
def send_mail(file_new):
    with open(file_new, 'rb') as f:
        mail_body = f.read()

        # msg = MIMEText(mail_body, 'base64', 'utf-8')
        # msg['Subject'] = Header("自动化测试报告" + now, 'utf-8')

        att = MIMEText(mail_body, 'base64', 'utf-8')
        att["Content-type"] = 'application/octet-stream'
        att['Content-Disposition'] = 'attachment; filename = "TestReport.html"'
        msg = MIMEMultipart('related')
        msg.attach(MIMEText("测试结果详见附件", 'html', 'utf-8'))
        msg['Subject'] = Header("自动化测试报告" + now, 'utf-8')
        msg.attach(att)
        print(mail_body)

        smtp = smtplib.SMTP()
        smtp.connect("smtp.1218.com.cn")
        smtp.login("chenyang@1218.com.cn", ".cyxka/Rzx123")
        smtp.sendmail("chenyang@1218.com.cn", "295568526@qq.com", msg.as_string())
        smtp.quit()
        print('email has send out')

#测试报告目录查找和生成测试报告文件
def new_report(testreport):
    lists = os.listdir(testreport)
    lists.sort(key=lambda fn: os.path.getmtime(testreport + '\\' + fn))
    file_new = os.path.join(testreport, lists[-1]).replace("\\t", "\\\\t")
    print(file_new)
    return file_new

if __name__ == '__main__':
    test_dir = "./test_case"
    test_report = "D:\py\\test_python_selenium\\test_project\\report"

    discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')

    now = time.strftime("%Y-%m-%d %H_%M_%S")
    # 生成HTML测试报告。定义报告存放路径
    file = test_report + '\\' + now + 'result.html'
    with open(file, 'wb') as fp:
        runner = HTMLTestRunner(stream=fp, title='测试报告', description='用例执行情况:')
        runner.run(discover)

        new_report = new_report(test_report)
        print(new_report)
        send_mail(new_report)