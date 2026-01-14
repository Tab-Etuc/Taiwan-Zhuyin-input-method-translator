import requests
import logging
from .config import config

logger = logging.getLogger(__name__)

class KeyboardMapper:
    """
    Handles the mapping between standard QWERTY keyboard and 
    Standard Daqian (Ta-Chien) Bopomofo layout.
    """
    
    # Standard Daqian Layout Mapping
    KEY_MAP = {
        '1': 'ㄅ', 'q': 'ㄆ', 'a': 'ㄇ', 'z': 'ㄈ',
        '2': 'ㄉ', 'w': 'ㄊ', 's': 'ㄋ', 'x': 'ㄌ',
        '3': 'ˇ', 'e': 'ㄍ', 'd': 'ㄎ', 'c': 'ㄏ',
        '4': 'ˋ', 'r': 'ㄐ', 'f': 'ㄑ', 'v': 'ㄒ',
        '5': 'ㄓ', 't': 'ㄔ', 'g': 'ㄕ', 'b': 'ㄖ',
        '6': 'ˊ', 'y': 'ㄗ', 'h': 'ㄘ', 'n': 'ㄙ',
        '7': '˙', 'u': 'ㄧ', 'j': 'ㄨ', 'm': 'ㄩ',
        '8': 'ㄚ', 'i': 'ㄛ', 'k': 'ㄜ', ',': 'ㄝ',
        '9': 'ㄞ', 'o': 'ㄟ', 'l': 'ㄠ', '.': 'ㄡ',
        '0': 'ㄢ', 'p': 'ㄣ', ';': 'ㄤ', '/': 'ㄥ',
        '-': 'ㄦ', ' ': '-'
    }

    @classmethod
    def to_bopomofo(cls, text):
        """Converts Latin characters into Bopomofo symbols locally."""
        result = []
        for char in text.lower():
            result.append(cls.KEY_MAP.get(char, char))
        return ''.join(result)


class BopomofoService:
    """Service facade for translation modes."""
    
    GOOGLE_API_URL = config.GOOGLE_API_URL
    
    _FULL_WIDTH_SPACE = 12288
    _HALF_WIDTH_SPACE = 32
    _FULL_WIDTH_START = 65281
    _FULL_WIDTH_END = 65374
    _FULL_WIDTH_OFFSET = 65248

    @classmethod
    def _normalize_input(cls, text, padding=True):
        """Pre-processes input text (Full-width to Half-width)."""
        result = []
        for char in text:
            code = ord(char)
            if code == cls._FULL_WIDTH_SPACE:
                result.append(chr(cls._HALF_WIDTH_SPACE))
            elif cls._FULL_WIDTH_START <= code <= cls._FULL_WIDTH_END:
                result.append(chr(code - cls._FULL_WIDTH_OFFSET))
            else:
                result.append(char)
        
        # Ensure a trailing space exists to help flush the last character buffer
        ret = "".join(result)
        if padding:
            ret += " "
        return ret

    @classmethod
    def online_translate(cls, text):
        """Uses Google Input Tools API for high-accuracy phrase selection."""
        normalized = cls._normalize_input(text, padding=True)
        result = cls._recursive_translate(normalized)
        if result and result.endswith('='):
            return result[:-1]
        return result

    @classmethod
    def _recursive_translate(cls, text):
        if not text:
            return ""

        params = {
            # Replace spaces with '=' as separator.
            # Replace ',' with '%2C'. 'requests' library will encode '%' to '%25', 
            # resulting in '%252C' sent to API. This prevents the API from interpreting 
            # ',' as a delimiter.
            'text': text.replace(' ', '=').replace(',', '%2C'),
            'ime': 'zh-hant-t-i0',
            'cb': '?'
        }

        try:
            response = requests.get(cls.GOOGLE_API_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            # Response format: [status, [[source, [candidates], [], metadata], ...]]
            if data and len(data) > 1 and data[1]:
                result_parts = []
                for segment in data[1]:
                    source = segment[0]
                    candidates = segment[1]
                    metadata = segment[3] if len(segment) > 3 else {}
                    
                    if not candidates:
                        # No translation found; keep first char and recurse on remainder
                        result_parts.append(source[0])
                        if len(source) > 1:
                            result_parts.append(cls._recursive_translate(source[1:]))
                    else:
                        chosen_candidate = candidates[0]
                        matched_len = len(source)
                        
                        # Check metadata for partial match (e.g., "ji3ggo6" -> matched "ji3")
                        if 'matched_length' in metadata and metadata['matched_length']:
                            matched_len = int(metadata['matched_length'][0])
                        
                        result_parts.append(chosen_candidate)
                        
                        if matched_len < len(source):
                            remainder = source[matched_len:]
                            result_parts.append(cls._recursive_translate(remainder))
                            
                return "".join(result_parts)
                
        except Exception as e:
            logger.warning(f"Online translation failed: {e}. Falling back to local decoding.")
            # On network failure, fallback to raw bopomofo keys
            return cls.local_decode(text)
        
        return text

    @classmethod
    def local_decode(cls, text):
        """Offline mode: Direct keyboard mapping without phrase selection."""
        # _normalize_input adds specific padding space, which maps to '-' (1st tone) in offline mode
        normalized = cls._normalize_input(text, padding=True)
        return KeyboardMapper.to_bopomofo(normalized)
