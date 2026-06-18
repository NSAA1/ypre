from fastapi import FastAPI, UploadFile, File
from captcha_recognizer.slider import Slider
from typing import Dict

app = FastAPI(title="移动云滑块识别 API")
slider = Slider()   # 全局加载一次模型

@app.post("/predict")
async def predict(file: UploadFile = File(...), correction: int = 0) -> Dict:
    content = await file.read()
    offset, confidence = slider.identify_offset(content)
    
    final_offset = int(offset + correction)
    
    return {
        "success": confidence > 0.75,
        "offset": final_offset,
        "confidence": round(float(confidence), 4),
        "raw_offset": int(offset),
        "correction": correction
    }
