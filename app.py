# -*- coding:utf-8 -*-
from fastapi import FastAPI, Request
from transformers import BertTokenizer
import torch
from model import MyModel
from config import parsers
import json

app = FastAPI()


def torch_gc():
    if torch.cuda.is_available():
        # with torch.cuda.device(CUDA_DEVICE):
        # with torch.cuda.device():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

def load_model(device, model_path):
    myModel = MyModel().to(device)
    myModel.load_state_dict(torch.load(model_path, map_location=device))
    myModel.eval()
    return myModel

def process_text(text, bert_pred, max_len):
    tokenizer = BertTokenizer.from_pretrained(bert_pred)
    # 如果文本长度超出max_len，则截断，否则保留原文本
    truncated_text = text[:max_len-1] # 截断max_len-1是为了给CLS留一个位置

    # 分词
    tokenized_text  = tokenizer.tokenize(truncated_text)

    # 编码
    token_id = tokenizer.convert_tokens_to_ids(["[CLS]"] + tokenized_text)
    
    # 掩码  
    mask = [1] * len(token_id) + [0] * (max_len  - len(token_id))
    token_ids = token_id + [0] * (max_len  - len(token_id))
    
    token_ids = torch.tensor(token_ids).unsqueeze(0)
    mask = torch.tensor(mask).unsqueeze(0)
    return [token_ids, mask]

def text_class_name(pred, classification_file):
    result = torch.argmax(pred, dim=1)
    result = result.cpu().numpy().tolist()
    classification = open(classification_file, "r", encoding="utf-8").read().split("\n")
    classification_dict = dict(zip(range(len(classification)), classification))
    return classification_dict[result[0]]

# 加载模型和配置
args = parsers()
print(f"args = {args}")
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = load_model(device, args.save_model_best)

@app.post("/classify")
async def classify_text(request: Request):
    data = await request.json()
    text = data.get('text', '')

    if not text:
        return {"error": "No text provided for classification"}

    x = process_text(text, args.bert_pred, args.max_len)
    with torch.no_grad():
        pred = model(x)
    
    classification = text_class_name(pred, args.classification)

    return {"text": text, "classification": classification}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
