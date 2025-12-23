import torch
import torch.nn.functional as F
import comfy.utils

class ImageBatch14:
    @classmethod
    def INPUT_TYPES(s):
        # 动态生成 image_2 到 image_14 的可选输入
        optional_images = {f"image_{i}": ("IMAGE",) for i in range(2, 15)}
        
        return {
            "required": {
                "image_1": ("IMAGE",),
            },
            "optional": optional_images,
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    CATEGORY = "lxj"

    def execute(self, image_1, **kwargs):
        # 以第一张图的宽和高作为画布的标准尺寸 (H, W)
        target_h, target_w = image_1.shape[1], image_1.shape[2]
        
        # 结果列表，先放入第一张图
        out_list = [image_1]

        for i in range(2, 15):
            img = kwargs.get(f"image_{i}")
            if img is not None:
                curr_h, curr_w = img.shape[1], img.shape[2]
                
                # 如果尺寸完全一致，直接添加
                if curr_h == target_h and curr_w == target_w:
                    out_list.append(img)
                    continue

                # 1. 计算缩放比例，确保图片完整显示 (Fit 模式)
                scale = min(target_w / curr_w, target_h / curr_h)
                new_w = int(curr_w * scale)
                new_h = int(curr_h * scale)

                # 2. 执行缩放 (默认使用高质量的 bicubic)
                # movedim 将 [B,H,W,C] 转为 [B,C,H,W]
                img_resized = comfy.utils.common_upscale(
                    img.movedim(-1, 1), new_w, new_h, "bicubic", "disabled"
                )

                # 3. 计算白色填充 (Padding)
                pad_left = (target_w - new_w) // 2
                pad_right = target_w - new_w - pad_left
                pad_top = (target_h - new_h) // 2
                pad_bottom = target_h - new_h - pad_top

                # F.pad 参数顺序: (左, 右, 上, 下)
                # value=1.0 在图像张量中代表白色 (0.0是黑色)
                img_padded = F.pad(
                    img_resized, 
                    (pad_left, pad_right, pad_top, pad_bottom), 
                    mode='constant', 
                    value=1.0 
                ).movedim(1, -1) # 转换回 [B,H,W,C]

                out_list.append(img_padded)

        # 4. 沿 Batch 维度合并
        out = torch.cat(out_list, dim=0)
        return (out,)