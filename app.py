# app.py
import os
import time
import hashlib
import xml.etree.ElementTree as ET
from flask import Flask, request
from doubao import get_doubao_reply

app = Flask(__name__)
WECHAT_TOKEN = os.getenv("WECHAT_TOKEN")

@app.route("/", methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        # 微信验证服务器合法性
        signature = request.args.get("signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        echostr = request.args.get("echostr")

        tmp_list = [WECHAT_TOKEN, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "".join(tmp_list)
        hash_str = hashlib.sha1(tmp_str.encode("utf-8")).hexdigest()

        if hash_str == signature:
            return echostr
        else:
            return ""

    if request.method == "POST":
        xml_data = request.data
        xml_tree = ET.fromstring(xml_data)
        from_user = xml_tree.find("FromUserName").text
        to_user = xml_tree.find("ToUserName").text
        user_msg = xml_tree.find("Content").text.strip()

        reply_content = get_doubao_reply(user_msg)

        reply_xml = f"""
        <xml>
          <ToUserName><![CDATA[{from_user}]]></ToUserName>
          <FromUserName><![CDATA[{to_user}]]></FromUserName>
          <CreateTime>{int(time.time())}</CreateTime>
          <MsgType><![CDATA[text]]></MsgType>
          <Content><![CDATA[{reply_content}]]></Content>
        </xml>
        """
        return reply_xml, 200, {'Content-Type': 'application/xml'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
