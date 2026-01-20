from .move_video import MoveVHSVideo
from .hook_and_long_gameplay_timestamps import HookAndLongGameplayTimestamps
from .json_from_llm import JSONFromLLMOutput

NODE_CLASS_MAPPINGS = {
    "MoveVHSVideo": MoveVHSVideo,
    "HookAndLongGameplayTimestamps": HookAndLongGameplayTimestamps,
    "JSONFromLLMOutput": JSONFromLLMOutput
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MoveVHSVideo": "Move VHS Video",
    "HookAndLongGameplayTimestamps": "Hook And Long Gameplay Timestamps",
    "JSONFromLLMOutput": "JSON from LLM Output"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']