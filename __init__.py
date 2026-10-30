from .nodes import (
    RandomTextLinePicker,
    RandomTextLinePicker3Folders,
    RandomTextLinePicker5Folders,
)

NODE_CLASS_MAPPINGS = {
    "RandomTextLinePicker": RandomTextLinePicker,
    "RandomTextLinePicker3Folders": RandomTextLinePicker3Folders,
    "RandomTextLinePicker5Folders": RandomTextLinePicker5Folders,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomTextLinePicker": "Random Text Line Picker (1 Folder)",
    "RandomTextLinePicker3Folders": "Random Text Line Picker (3 Folders)",
    "RandomTextLinePicker5Folders": "Random Text Line Picker (5 Folders)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
