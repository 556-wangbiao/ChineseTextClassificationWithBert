import os
import shutil
import torch
import logging
from utils.utils import read_data, MyDataset
from config import parsers
from torch.utils.data import DataLoader
from model import MyModel
from torch.optim import AdamW
import torch.nn as nn
from sklearn.metrics import accuracy_score
import time
from app import load_model
from datetime import datetime
from utils.logger import logger_config

# 应用日志配置
logging.config.dictConfig(logger_config("dev"))
training_logger = logging.getLogger('training_logger')


# 生成模型版本
def generate_model_version():
    """
    按时间戳生成模型版本
    :return:
    """
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"{timestamp}.pth"


# 删除旧版本模型
def delete_old_model(model_save_path, nums=3):
    """
    删除多余的旧版本模型
    :param model_save_path: 模型保存的地址
    :param nums: 超过nums个模型执行删除
    :return: None
    """
    try:
        model_list = [model[:-4] for model in os.listdir(model_save_path)]
        model_list.sort()
        if len(model_list) > nums:
            delete_model = model_list[0]
            delete_model_path = os.path.join(model_save_path, delete_model) + '.pth'
            if os.path.exists(delete_model_path):
                os.remove(delete_model_path)
                training_logger.info(f"Deleted old model: {delete_model_path}")
            else:
                training_logger.warning(f"Model file not found: {delete_model_path}")
    except Exception as e:
        training_logger.error(f"Error occurred while deleting old models: {e}")


def train_time(start_time, end_time):
    training_duration_seconds = end_time - start_time
    hours, remainder = divmod(training_duration_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds


def train(args, app_model_path, device):
    # 记录训练开始
    start_time = time.time()
    training_logger.info(f"Training started at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")

    train_text, train_label, max_len = read_data(args.train_file)
    dev_text, dev_label = read_data(args.dev_file)
    # args.max_len = max_len

    train_dataset = MyDataset(train_text, train_label, args.max_len)
    train_dataloader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)

    dev_dataset = MyDataset(dev_text, dev_label, args.max_len)
    dev_dataloader = DataLoader(dev_dataset, batch_size=args.batch_size, shuffle=False)

    # 如果有训练过的模型则继续训练，否则从预训练模型开始训练
    if os.path.exists(app_model_path):
        model = load_model(device, app_model_path)
    else:
        model = MyModel().to(device)

    opt = AdamW(model.parameters(), lr=args.learn_rate)
    loss_fn = nn.CrossEntropyLoss()

    no_promotion = 0
    acc_max = float("-inf")
    model_version = generate_model_version()

    for epoch in range(args.epochs):
        loss_sum = 0
        model.train()
        for batch_index, (batch_text, batch_label) in enumerate(train_dataloader):

            batch_label = batch_label.to(device)
            pred = model(batch_text)

            loss = loss_fn(pred, batch_label)
            opt.zero_grad()
            loss.backward()
            opt.step()
            loss_sum += loss

            # 每20个批次打印一次损失（如果最后一个批次不满batch_size也打印），损失是一个批次的全局损失
            if batch_index % 20 == 19 or batch_index + 1 == len(train_dataloader):
                msg = "[{0}/{1:5d}]\tTrain_Loss:{2:.4f}"
                training_logger.info(msg.format(epoch + 1, batch_index + 1, loss_sum / (batch_index + 1)))

        model.eval()
        all_pred, all_true = [], []
        with torch.no_grad():
            for batch_text, batch_label in dev_dataloader:
                batch_label = batch_label.to(device)
                pred = model(batch_text)

                pred = torch.argmax(pred, dim=1).cpu().numpy().tolist()
                label = batch_label.cpu().numpy().tolist()

                all_pred.extend(pred)
                all_true.extend(label)

        acc = accuracy_score(all_pred, all_true)
        training_logger.info(f"dev acc:{acc:.4f}")
        if acc > acc_max:
            no_promotion = 0
            acc_max = acc
            path = os.path.join(args.save_model_path, model_version)
            torch.save(model.state_dict(), path)
        else:
            no_promotion += 1
        if no_promotion >= args.patience:
            logging.info(f"在第{epoch + 1}个批次时触发了早停法！")
            break
    # 训练结束后，复制最佳模型到应用接口调用的模型位置
    shutil.copy(os.path.join(args.save_model_path, model_version), app_model_path)
    training_logger.info(f"训练结束，复制到最佳模型到{app_model_path}")

    # 检查模型是否多余nums个，如果多于nums个则删除最老的一个模型
    delete_old_model(args.save_model_path, nums=args.nums)

    end_time = time.time()

    hours, minutes, seconds = train_time(start_time=start_time, end_time=end_time)
    # 记录训练结束、耗时和模型版本
    training_logger.info(f"Training completed in {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")
    training_logger.info(f"Model version: {model_version}")

    training_logger.info(f"\n")


if __name__ == "__main__":
    args = parsers()
    app_model_path = './app_model.pth'
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    train(args=args, app_model_path=app_model_path, device=device)
