import os
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import ImageFolder

# 데이터셋 경로 설정
data_dict = {
    "cifar10": "/home/data/cifar10",          # train, test로 나눠야함
    "cifar100": "/home/data/cifar100",        # train, test로 나눠야함
    "imagenet": "/home/data/imagenet_1k",     # train, val로 나눠야함
    "imagenet-c": "/home/data/imagenet-c",    # ood로 사용시 label = -1 or 0 필요
    "imagenet-r": "/home/data/imagenet-r",    # ood로 사용시 label = -1 or 0 필요
    "inaturalist": "/home/data/inaturalist",
    "iSUN": "/home/data/iSUN/test",
    "LSUN-C": "/home/data/LSUN-C/test",
    "LSUN-R": "/home/data/LSUN-R/test",
    "ninco": "/home/data/ninco",              # ood로 사용시 label = -1 or 0 필요
    "openimage_o": "/home/data/openimage-o",
    "PACS": "/home/data/PACS",
    "places365": "/home/data/places365",      # ood로 사용시 label = -1 or 0 필요
    "ssb_hard": "/home/data/ssb_hard",        # ood로 사용시 label = -1 or 0 필요
    "svhn": "/home/data/svhn",
    "texture": "/home/data/texture",          # ood로 사용시 label = -1 or 0 필요
    "VLCS": "/home/data/VLCS"
}

# normalization and image size
info_dict = {
    'cifar10': [[0.4914, 0.4822, 0.4465],[0.2023, 0.1994, 0.2010], 32],
    'cifar100': [[0.5071, 0.4867, 0.4408],[0.2675, 0.2565, 0.2761], 32],
    'imagenet': [[0.485, 0.456, 0.406], [0.229, 0.224, 0.225], 224],
}

# 기본 이미지 변환 (CIFAR 및 ImageNet 스타일)

def get_dataloader(base_data, dataname, batch_size=128, phase="train"):
    """
    학습에 사용한 data(base_data), 데이터셋 이름(dataname), batchsize, phase(train, test, ood)에 맞는 DataLoader를 반환.
    
    Args:
        base_data (str): 학습에 사용한 데이터셋 이름 ("cifar10","cifar100","imagenet" 중 하나)
        dataname (str): 사용할 데이터셋 이름
        batch_size (int): DataLoader의 batch size
        phase (str): "train","val","test","ood" 중 하나
    Returns:
        DataLoader: 해당 데이터셋에 대한 DataLoader
    """
    if base_data not in ["cifar10", "cifar100", 'imagenet']:
        raise ValueError(f"Dataset {base_data} is not used for training")
    
    if dataname not in data_dict:
        raise ValueError(f"Dataset {dataname} is not found in data_dict.")
    
    img_size = info_dict[base_data][2]
    MEAN, STD = info_dict[base_data][0], info_dict[base_data][1]


    # Train Transform (Data Augmentation 포함)
    train_transform = transforms.Compose([
        transforms.RandomCrop(img_size, padding=4),  # 랜덤 크롭 후 리사이즈
        transforms.RandomHorizontalFlip(),       # 수평 플립
        transforms.ToTensor(),
        transforms.Normalize(mean=MEAN, std=STD)
    ])

    # Test/Val/OOD Transform (Data Augmentation 없음)
    test_transform = transforms.Compose([
        transforms.Resize((img_size,img_size)),  # 크기 맞추기
        transforms.ToTensor(),
        transforms.Normalize(mean=MEAN, std=STD)
    ])
    
    # Phase에 따라 transform 선택
    transform = train_transform if phase == "train" else test_transform

    dataset_path = data_dict[dataname]

    # Phase에 따라 train/test 디렉토리 설정
    if phase == "ood":
        pass

    elif phase in ["train","val", "test"]:
        dataset_path = os.path.join(dataset_path, phase)

    # ImageFolder로 모든 데이터셋 로드
    dataset = ImageFolder(dataset_path, transform=transform)

    # OOD 데이터셋이면 모든 label을 -1로 설정
    if phase == "ood":
        dataset.targets = [-1] * len(dataset)

    # DataLoader 생성
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=(phase == "train"), num_workers=4)
    
    print(f"Loaded {dataname} ({phase}) with {len(dataset)} samples.")
    return dataloader

if __name__ == "__main__":
    dataloader = get_dataloader(base_data='cifar10',dataname='openimage-o',batch_size=128, phase='ood')