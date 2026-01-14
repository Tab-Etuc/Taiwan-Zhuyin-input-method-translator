import pytest
from unittest.mock import patch, Mock
from bopomofo_translator.core import BopomofoService, KeyboardMapper

class TestKeyboardMapper:
    def test_basic_mapping(self):
        # su3 -> ㄋㄧˇ (ni3 -> 你)
        assert KeyboardMapper.to_bopomofo("su3") == "ㄋㄧˇ"
        # cl3 -> ㄏㄠˇ (hao3 -> 好)
        assert KeyboardMapper.to_bopomofo("cl3") == "ㄏㄠˇ"
    
    def test_mixed_input(self):
        # 1qaz -> ㄅㄆㄇㄈ
        assert KeyboardMapper.to_bopomofo("1qaz") == "ㄅㄆㄇㄈ"
        
    def test_ignore_unknown_chars(self):
        # abc!@# -> ㄇㄖㄏ!@# (assuming mapping exists for a,b,c)
        # a->ㄇ, b->ㄖ, c->ㄏ
        assert KeyboardMapper.to_bopomofo("abc!@#") == "ㄇㄖㄏ!@#"

    def test_space_mapping(self):
        # Space should be mapped to hyphen '-'
        assert KeyboardMapper.to_bopomofo("ji3 su3") == "ㄨㄛˇ-ㄋㄧˇ"

class TestBopomofoService:
    def test_normalize_input(self):
        # Full width １ (65297) -> 1 (49)
        # 65297 - 65248 = 49 ('1')
        full_width_1 = chr(65297)
        assert BopomofoService._normalize_input(full_width_1, padding=False).strip() == "1"
        
        # Space handling
        full_width_space = chr(12288)
        assert BopomofoService._normalize_input(full_width_space, padding=False).strip() == "" # normalized to space then stripped

    def test_local_decode(self):
        # The trailing space maps to '-' in offline mode, acting as a delimiter or 1st tone marker
        assert BopomofoService.local_decode("su3cl3").strip() == "ㄋㄧˇㄏㄠˇ-"

    @patch('requests.get')
    def test_recursive_translate_logic(self, mock_get):
        # Mock response for "ji3" -> "我"
        mock_response = Mock()
        mock_response.json.return_value = [
            "SUCCESS",
            [
                ["ji3", ["我"], [], {"matched_length": [3]}]
            ]
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = BopomofoService.online_translate("ji3")
        assert result == "我"

    @patch('requests.get')
    def test_comma_handling(self, mock_get):
        # input: "vu,3" -> target: "寫" (xie3)
        # We ensure that ',' is replaced by '%2C' in params so valid URL becomes ...%252C...
        mock_response = Mock()
        mock_response.json.return_value = [
            "SUCCESS",
            [
                ["vu,3", ["寫"], [], {}]
            ]
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Act
        result = BopomofoService.online_translate("vu,3")
        
        # Assert
        assert result == "寫"
        
        # Verify the params passed to requests
        # text should have used %2C for the comma
        args, kwargs = mock_get.call_args
        assert kwargs['params']['text'] == "vu%2C3"

@pytest.mark.parametrize("input_text, expected", [
    ("ji3", "ㄨㄛˇ"),   # wo3 -> 我
    ("vul3", "ㄒㄧㄠˇ"), # xiao3 -> 小
])
def test_mapper_params(input_text, expected):
    assert KeyboardMapper.to_bopomofo(input_text) == expected
