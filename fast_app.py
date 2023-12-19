# -*- coding:utf-8 -*-
from fastapi import FastAPI, Request
from transformers import BertTokenizer
import torch

from config import parsers
import logging
from utils.logger import logger_config
from fastapi.responses import JSONResponse
import uvicorn
from utils.utils import torch_gc, load_model, process_text, text_class_name
import os

# 设置日志
logging.config.dictConfig(logger_config("dev"))
logger = logging.getLogger("app_logger")

args = parsers()
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = load_model(device, './app_model.pth')
model.eval()
app = FastAPI()


@app.post("/classify")
async def classify_text(request: Request):
    try:
        data = await request.json()
        text = data.get('text', '')

        if not text:
            logger.warning("/classify endpoint: No text provided for classification")
            return JSONResponse(status_code=400, content={"message": "No text provided for classification"})

        x = process_text(text, args.bert_pred, args.max_len)
        with torch.no_grad():
            pred = model(x)

        # 释放显存
        torch_gc()

        classification = text_class_name(pred, args.classification)
        logger.info(f"/classify endpoint: Classification success for text: {text}")

        return {"classification": classification, "status_code": 200}

    except Exception as e:
        logger.error(f"/classify endpoint: Server error - {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


if __name__ == "__main__":
    # 加载模型和配置
    # args = parsers()
    # print(f"args = {args}")
    # device = "cuda:0" if torch.cuda.is_available() else "cpu"
    # model = load_model(device, './app_model.pth')
    # model.eval()
    uvicorn.run(app, host="0.0.0.0", port=8000)
