from .ImageBatch14 import ImageBatch14
from .TextBatch14 import TextBatch14

# 节点内部名称 : 类名
NODE_CLASS_MAPPINGS = {
    "lxj_ImageBatch14": ImageBatch14,
    "lxj_TextBatch14": TextBatch14
}

# 节点在 UI 界面显示的名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "lxj_ImageBatch14": "lxj_ImageBatch14",
    "lxj_TextBatch14": "lxj_TextBatch14"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']