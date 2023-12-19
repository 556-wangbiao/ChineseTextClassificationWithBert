# -*- coding:utf-8 -*-
from transformers import BertTokenizer
import torch
from flask import Flask, jsonify, request
from config import parsers
import logging
from utils.logger import logger_config
from fastapi.responses import JSONResponse
import uvicorn
from utils.utils import torch_gc, load_model, process_text, text_class_name
import os

app = Flask(__name__)

args = parsers()
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = load_model(device, 'app_model.pth')
model.eval()

# 设置日志
logging.config.dictConfig(logger_config("dev"))
logger = logging.getLogger("app_logger")


@app.route("/classify", methods=['POST'])
def classify_text():
    status_code = 200
    message = 'success'
    classification = None

    try:
        data = request.json
        text = data.get('text', '')

        if not text:
            logger.warning("/classify endpoint: No text provided for classification")
            status_code = 400
            message = "No text provided for classification"
        else:
            x = process_text(text, args.bert_pred, args.max_len)
            with torch.no_grad():
                pred = model(x)

            # 释放显存
            torch_gc()

            classification = text_class_name(pred, args.classification)
            logger.info(f"/classify endpoint: Classification success for text: {text}")

    except Exception as e:
        logger.error(f"/classify endpoint: Server error - {str(e)}", exc_info=True)
        status_code = 500
        message = "Internal Server Error"

    return jsonify({"status_code": status_code, "message": message, "classification": classification}), status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
