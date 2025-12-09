import os
import base64
import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI()

DEEPSEEK_OCR_URL = "https://api.deepseek.com/ocr"  # 替换为你的真实 OCR 接口
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")    # 从 .env 注入

# 在启动时检查 API Key 是否存在
if not DEEPSEEK_API_KEY:
    print("⚠ WARNING: 环境变量 DEEPSEEK_API_KEY 未设置，OCR 请求将无法工作！")


@app.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    # 如果运行时没有 API Key，则直接报错
    if not DEEPSEEK_API_KEY:
        return JSONResponse({
            "code": 1,
            "msg": "Missing API key: 请设置环境变量 DEEPSEEK_API_KEY"
        }, status_code=400)

    try:
        # 读取上传的图片
        content = await file.read()

        # 转 base64（很多 OCR 服务支持 base64）
        img_b64 = base64.b64encode(content).decode("utf-8")

        # 请求头
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }

        # 请求体（按 DeepSeek API 定义调整）
        payload = {
            "image": img_b64,
            # 可扩展参数：
            # "lang": "auto",
            # "detect_direction": True,
        }

        # 发送请求到 DeepSeekOCR 在线 API
        resp = requests.post(
            DEEPSEEK_OCR_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        # HTTP 错误会自动 raise
        resp.raise_for_status()
        data = resp.json()

        # 返回统一结构
        return JSONResponse({
            "code": 0,
            "msg": "success",
            "result": data
        })

    except requests.exceptions.RequestException as e:
        # 网络/HTTP错误
        return JSONResponse({
            "code": 2,
            "msg": f"Request Error: {str(e)}"
        }, status_code=502)

    except Exception as e:
        # 其他错误
        return JSONResponse({
            "code": 3,
            "msg": f"Internal Error: {str(e)}"
        }, status_code=500)
