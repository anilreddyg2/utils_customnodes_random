import json
import re

class HookAndLongGameplayTimestamps:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "json_string": ("STRING", {"default": "{\"Hook\": 0.0, \"LongGameplay\": 0.0}", "multiline": True}),
            },
        }

    RETURN_TYPES = ("FLOAT", "FLOAT")
    RETURN_NAMES = ("Hook", "LongGameplay")
    FUNCTION = "extract_floats"
    CATEGORY = "utils"

    def extract_floats(self, json_string):
        # Try to find all JSON-like substrings (non-greedy match for {})
        # This regex handles simple flat JSON objects well.
        matches = re.findall(r'\{.*?\}', json_string, re.DOTALL)
        
        # Iterate backwards to find the last valid JSON
        for match in reversed(matches):
            try:
                data = json.loads(match)
                if "Hook" in data and "LongGameplay" in data:
                    return (float(data.get("Hook", 0.0)), float(data.get("LongGameplay", 0.0)))
            except (json.JSONDecodeError, ValueError):
                continue
        
        # Fallback: Try to parse the entire string if regex missed (e.g. complex nesting or single object)
        try:
            data = json.loads(json_string)
            return (float(data.get("Hook", 0.0)), float(data.get("LongGameplay", 0.0)))
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return (0.0, 0.0)
