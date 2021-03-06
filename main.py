import torch

from config import Config
from dataset import create_datasets, my_collate_fn
from model import Net
from trainer import Trainer


def main():
    train_dataset, val_dataset = create_datasets(Config.DATASET_DIR)

    train_dataloader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=Config.BATCH_SIZE,
        num_workers=Config.DATALOADER_WORKER_NUM,
        shuffle=True,
        collate_fn=my_collate_fn
    )

    val_dataloader = torch.utils.data.DataLoader(
        val_dataset,
        batch_size=Config.BATCH_SIZE,
        num_workers=Config.DATALOADER_WORKER_NUM,
        shuffle=False,
        collate_fn=my_collate_fn
    )

    model = Net()
    optimizer = torch.optim.Adam(
        params=model.parameters(),
        lr=Config.LEARNING_RATE, weight_decay=Config.WEIGHT_DECAY
    )

    trainer = Trainer(
        optimizer,
        model,
        train_dataloader,
        val_dataloader,
        resume=Config.RESUME_FROM,
        log_dir=Config.LOG_DIR,
        persist_stride=Config.MODEL_SAVE_STRIDE
    )
    trainer.train()


if __name__ == "__main__":
    torch.backends.cudnn.benchmark = True
    torch.set_default_tensor_type('torch.FloatTensor')

    main()
