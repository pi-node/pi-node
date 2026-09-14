import torch
import torch.nn as nn
import torch.nn.functional as F

class ResNet(nn.Module):
    def __init__(self, num_classes):
        super(ResNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(64, 64, 3)
        self.layer2 = self._make_layer(64, 128, 4)
        self.layer3 = self._make_layer(128, 256, 6)
        self.layer4 = self._make_layer(256, 512, 3)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)

    def _make_layer(self, in_channels, out_channels, num_blocks):
        layers = []
        for i in range(num_blocks):
            layers.append(ResidualBlock(in_channels, out_channels))
            in_channels = out_channels
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avgpool(x)
        x = x.view(-1, 512)
        x = self.fc(x)
        return x

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(out_channels)

    def forward(self, x):
        residual = x
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x += residual
        x = self.relu(x)
        return x

class DenseNet(nn.Module):
    def __init__(self, num_classes):
        super(DenseNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.dense_block1 = self._make_dense_block(64, 128, 6)
        self.transition1 = self._make_transition(128, 128)
        self.dense_block2 = self._make_dense_block(128, 256, 12)
        self.transition2 = self._make_transition(256, 256)
        self.dense_block3 = self._make_dense_block(256, 512, 24)
        self.transition3 = self._make_transition(512, 512)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)

    def _make_dense_block(self, in_channels, out_channels, num_layers):
        layers = []
        for i in range(num_layers):
            layers.append(DenseLayer(in_channels, out_channels))
            in_channels = out_channels
        return nn.Sequential(*layers)

    def _make_transition(self, in_channels, out_channels):
        return nn.Sequential(
            nn.BatchNorm2d(in_channels),
            nn.ReLU(),
            nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0),
            nn.AvgPool2d(kernel_size=2, stride=2, padding=0)
        )

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.dense_block1(x)
        x = self.transition1(x)
        x = self.dense_block2(x)
        x = self.transition2(x)
        x = self.dense_block3(x)
        x = self.transition3(x)
        x = self.avgpool(x)
        x = x.view(-1, 512)
        x = self.fc(x)
        return x

class DenseLayer(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(DenseLayer, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=1)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x

class InceptionV3(nn.Module):
    def __init__(self, num_classes):
        super(InceptionV3, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.inception_block1 = self._make_inception_block(32, 64, 96, 128, 16, 32, 32)
        self.inception_block2 = self._make_inception_block(128, 128, 192, 256, 32, 64, 64)
        self.inception_block3 = self._make_inception_block(256, 256, 320, 400, 48, 96, 96)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc= nn.Linear(400, num_classes)

    def _make_inception_block(self, in_channels1, in_channels2, out_channels1, out_channels2, out_channels3, out_channels4, out_channels5):
        return nn.Sequential(
            InceptionModule(in_channels1, out_channels1, out_channels2, out_channels3, out_channels4, out_channels5),
            InceptionModule(in_channels2, out_channels1, out_channels2, out_channels3, out_channels4, out_channels5)
        )

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.inception_block1(x)
        x = self.inception_block2(x)
        x = self.inception_block3(x)
        x = self.avgpool(x)
        x = x.view(-1, 400)
        x = self.fc(x)
        return x

class InceptionModule(nn.Module):
    def __init__(self, in_channels, out_channels1, out_channels2, out_channels3, out_channels4, out_channels5):
        super(InceptionModule, self).__init__()
        self.branch1 = nn.Sequential(
            nn.Conv2d(in_channels, out_channels1, kernel_size=1, stride=1, padding=0),
            nn.BatchNorm2d(out_channels1),
            nn.ReLU()
        )
        self.branch2 = nn.Sequential(
            nn.Conv2d(in_channels, out_channels2, kernel_size=1, stride=1, padding=0),
            nn.BatchNorm2d(out_channels2),
            nn.ReLU(),
            nn.Conv2d(out_channels2, out_channels3, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(out_channels3),
            nn.ReLU()
        )
        self.branch3 = nn.Sequential(
            nn.Conv2d(in_channels, out_channels4, kernel_size=1, stride=1, padding=0),
            nn.BatchNorm2d(out_channels4),
            nn.ReLU(),
            nn.Conv2d(out_channels4, out_channels5, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(out_channels5),
            nn.ReLU()
        )
        self.branch4 = nn.Sequential(
            nn.MaxPool2d(kernel_size=3, stride=1, padding=1),
            nn.Conv2d(in_channels, out_channels1, kernel_size=1, stride=1, padding=0),
            nn.BatchNorm2d(out_channels1),
            nn.ReLU()
        )

    def forward(self, x):
        x1 = self.branch1(x)
        x2 = self.branch2(x)
        x3 = self.branch3(x)
        x4 = self.branch4(x)
        return torch.cat((x1, x2, x3, x4), 1)

class MobileNetV2(nn.Module):
    def __init__(self, num_classes):
        super(MobileNetV2, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.inverted_residual_block1 = self._make_inverted_residual_block(32, 64, 1)
        self.inverted_residual_block2 = self._make_inverted_residual_block(64, 128, 2)
        self.inverted_residual_block3 = self._make_inverted_residual_block(128, 256, 3)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(256, num_classes)

    def _make_inverted_residual_block(self, in_channels, out_channels, num_blocks):
        layers = []
        for i in range(num_blocks):
            layers.append(InvertedResidualBlock(in_channels, out_channels))
            in_channels = out_channels
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.inverted_residual_block1(x)
        x = self.inverted_residual_block2(x)
        x = self.inverted_residual_block3(x)
        x = self.avgpool(x)
        x = x.view(-1, 256)
        x = self.fc(x)
        return x

class InvertedResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(InvertedResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, groups=out_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.conv3 = nn.Conv2d(out_channels, out_channels, kernel_size=1, stride=1, padding=0)
        self.bn3 = nn.BatchNorm2d(out_channels)

    def forward(self, x):
        residual = x
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.conv3(x)
        x = self.bn3(x)
        x += residual
        x = self.relu(x)
        return x
