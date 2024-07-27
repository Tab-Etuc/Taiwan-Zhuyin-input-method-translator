import requests

class FullWidthConverter:
    @staticmethod
    def to_half_width(message):
        def full_width_to_half_width(char):
            # 處理空格
            if char == chr(12288):
                return chr(32)
            # 處理全形字符範圍
            code = ord(char)
            if 65281 <= code <= 65374:
                return chr(code - 65248)
            # 其他字符保持不變
            return char
        
        # 逐一轉換每個字符
        return ''.join(full_width_to_half_width(char) for char in message)

def main():
    while True:
        try:
            message = input('請輸入欲翻譯的文字\n')
            message = FullWidthConverter.to_half_width(message)
            message = message + ' '
            message = message.replace(' ', '=')            
            
            URL = f'https://www.google.com/inputtools/request?text={message}&ime=zh-hant-t-i0&cb=?'

            response = requests.get(url=URL)
            response.raise_for_status()  # 檢查 HTTP 錯誤
            
            result = response.json()
            translation = result[1][0][1][0]
            print(translation)
        except requests.RequestException as e:
            print(f"請求錯誤: {e}")
        except (IndexError, KeyError, ValueError):
            print("無法獲取翻譯結果，請重試。")
        except EOFError:
            print('感謝使用！')
            break

if __name__ == "__main__":
    main()
