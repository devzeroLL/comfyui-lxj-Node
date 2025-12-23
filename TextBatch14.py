
class TextBatch14:
    @classmethod
    def INPUT_TYPES(s):
        # 动态生成 text_2 到 text_14 的可选输入
        optional_texts = {f"text_{i}": ("STRING", {"multiline": True}) for i in range(2, 15)}
        
        return {
            "required": {
                "text_1": ("STRING", {"multiline": True}),
                "delimiter": ("STRING", {"default": ",", "multiline": False}),
            },
            "optional": optional_texts,
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    CATEGORY = "lxj"

    def execute(self, text_1, delimiter, **kwargs):
        # 结果列表，先放入第一段文本
        text_list = [text_1]

        for i in range(2, 15):
            text = kwargs.get(f"text_{i}")
            if text is not None and text != "":
                 text_list.append(text)
        
        # 处理转义字符，比如用户输入 \n 实际上是希望换行
        real_delimiter = delimiter.replace("\\n", "\n")

        # 拼接
        result = real_delimiter.join(text_list)
        return (result,)
