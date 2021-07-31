#匯入模組
import requests  

#全、半形轉換
class Change():
    # 將字典的鍵-值互換，例: {'a': 1, 'b': 2}-> {1: 'a', 2: 'b'}
    def dict_key_val_reverse(convertDict):
        return dict(zip(convertDict.values(), convertDict.keys()))
    #轉換
    def strConvert(message):
        restring = ""
        convertDict = dict(zip(range(33, 127), range(65281, 65375)))
        convertDict.update({32: 12288})
        convertDict = Change.dict_key_val_reverse(convertDict)
        for uchar in message:
            u_code = ord(uchar)
            if u_code in convertDict:
                u_code = convertDict[u_code]
            restring += chr(u_code)
        return restring

#主程式
while True:
    message = str(input('請輸入欲翻譯的文字\n'))    #讓使用者輸入欲翻譯之文字
    message = Change.strConvert(message)    #將全形文字轉換成半形文字
    message = message + ' '     #防止使用者輸入如：'i '(喔) 時，誤將結尾空格捨去、少打
    message = message.replace(' ', '=')     #將所有空格轉換為 '='
    URL = f'https://www.google.com/inputtools/request?text={message}&ime=zh-hant-t-i0&cb=?'
    message = requests.post(url=URL)    #將請求post給上述連結
    print(message.json()[1][0][1][0])   #解析回傳之資料，並print出