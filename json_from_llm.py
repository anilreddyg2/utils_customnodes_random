import json
import re

class JSONFromLLMOutput:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "string": ("STRING", {"default": "{}", "multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING", "FLOAT", "INT")
    RETURN_NAMES = ("strings", "floats", "ints")
    OUTPUT_IS_LIST = (True, True, True)
    FUNCTION = "extract_values"
    CATEGORY = "utils"

    def extract_values(self, string):
        # Try to find all JSON-like substrings (non-greedy match for {})
        matches = re.findall(r'\{.*?\}', string, re.DOTALL)
        
        valid_data = {}
        found_valid = False

        # Iterate backwards to find the last valid JSON
        for match in reversed(matches):
            try:
                data = json.loads(match)
                valid_data = data
                found_valid = True
                break
            except (json.JSONDecodeError, ValueError):
                continue
        
        # Fallback: Try to parse the entire string if regex missed
        if not found_valid:
            try:
                valid_data = json.loads(string)
            except Exception:
                pass 

        strings = []
        floats = []
        ints = []

        def recurse(data):
            if isinstance(data, dict):
                for v in data.values():
                    recurse(v)
            elif isinstance(data, list):
                for v in data:
                    recurse(v)
            elif isinstance(data, str):
                strings.append(data)
            elif isinstance(data, bool):
                pass 
            elif isinstance(data, int):
                ints.append(data)
                floats.append(float(data))
            elif isinstance(data, float):
                floats.append(data)

        recurse(valid_data)
        
        return (strings, floats, ints)