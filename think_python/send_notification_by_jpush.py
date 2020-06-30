
import jpush
from jpush import alias

import json

def push_msg(message, extra_info, user_ids):
    app_key = '8851280aaabf8cd8340f9236'
    master_secret = '74ae9ad0e596407e9667f7d0'

    _jpush = jpush.JPush(app_key, master_secret)
    push = _jpush.create_push()

    android_msg = jpush.android(alert=message, extras=extra_info)
    ios_msg = jpush.ios(alert=message, extras=extra_info)

    push.notification = jpush.notification(ios=ios_msg, android=android_msg)
    #设置目标用户
    push.audience = jpush.audience( user_ids )
    push.options = {"time_to_live": 86400, "apns_production": True}
    push.platform = jpush.platform("all")
    print(push.payload)
    #push.send()

msg = "您有新的接待申请待审批"
extra_info = {
    "category": "reception_detail",
    "role": "discipline",
    "id": 5
}

user_list = [766, 768]
alais_user = alias(*user_list)
push_msg(msg, extra_info, alais_user)
