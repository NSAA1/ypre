from fastapi import FastAPI, UploadFile, File
from captcha_recognizer.slider import Slider
from typing import Dict
import uvicorn

app = FastAPI(title="移动云滑块识别 API")
slider = Slider()   # 全局加载模型，启动后只加载一次

@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> Dict:
    content = await file.read()
    
    # identify 方法直接对单张带缺口的 puzzle 图有效
    box, confidence = slider.identify(source=content, show=False)
    
    # ================== 关键：根据移动云实际样式调整偏移量 ==================
    # 你需要先手动测几次移动云的验证码，确定初始偏移（initial_offset）和缩放比例
    initial_offset = 8          # ←←← 这里要你自己测准（常用值 0~30）
    scale = 1.0                 # 如果前端对图片做了缩放，这里要乘比例
    offset = int((box[0] - initial_offset) * scale) if box else 0
    
    return {
        "success": bool(confidence > 0.75),
        "offset": offset,
        "box": box,
        "confidence": float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
