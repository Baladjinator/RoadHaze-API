import torch
import torch.nn as nn
import torchvision.models as models
from typing import List
from torchvision import transforms
from torch import nn

device = "cuda" if torch.cuda.is_available() else "cpu"

class ResNet18(nn.Module):
    def __init__(self, num_classes):
        super(ResNet18, self).__init__()
        self.resnet = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            nn.Sequential(*list(models.resnet18(weights=None).children())[4:-1])
        )
        self.fc = nn.Linear(512, num_classes)

    def forward(self, x):
        x = self.resnet(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x


def eval(model: torch.nn.Module,
        random_Image: torch.Tensor):
    model.eval()
    with torch.inference_mode():
        # Add an extra dimension to image
        custom_image_transformed_with_batch_size = random_Image.unsqueeze(dim=0)

        # Make a prediction on image with an extra dimension
        custom_image_pred = model(random_Image.unsqueeze(dim=0).to(device))
        custom_image_pred_probs = torch.softmax(custom_image_pred, dim=1)
        print(custom_image_pred_probs)
        # Convert prediction probabilities -> prediction labels
        custom_image_pred_label = torch.argmax(custom_image_pred_probs, dim=1)
        #print(f"Prediction label: {custom_image_pred_label}")
        
    return custom_image_pred_label


def eval_for_camera(model: torch.nn.Module,
                    random_Image: torch.tensor,
                    labels_names: List):
    label = eval(model,
                random_Image)
        
    return labels_names[eval(model, random_Image).squeeze(dim=0)]

model = ResNet18(6)
model.load_state_dict(torch.load("./server/model/epoch-15.pth", map_location=torch.device('cpu'))["model_state_dict"])

labels_names = ['dry', 'fresh', 'ice', 'melted', 'water', 'wet']

convert_tensor = transforms.ToTensor()
