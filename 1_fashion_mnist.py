from __future__ import print_function
import os
import argparse
import datetime
import six
import math

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
from torchvision import datasets
from torchvision import transforms
from torch.autograd import Variable
from tqdm import tqdm

import numpy as np

from tensorboardX import SummaryWriter
import callbacks

# Training settings
parser = argparse.ArgumentParser(description='Deep Learning JHU Assignment 1 - Fashion-MNIST')
parser.add_argument('--batch-size', type=int, default=256, metavar='B',
                    help='input batch size for training (default: 64)')
parser.add_argument('--test-batch-size', type=int, default=1000, metavar='TB',
                    help='input batch size for testing (default: 1000)')
parser.add_argument('--epochs', type=int, default=10, metavar='E',
                    help='number of epochs to train (default: 10)')
parser.add_argument('--lr', type=float, default=0.01, metavar='LR',
                    help='learning rate (default: 0.01)')
parser.add_argument('--optimizer', type=str, default='sgd', metavar='O',
                    help='Optimizer options are sgd, adam, rms_prop')
parser.add_argument('--momentum', type=float, default=0.5, metavar='MO',
                    help='SGD momentum (default: 0.5)')
parser.add_argument('--no-cuda', action='store_true', default=False,
                    help='disables CUDA training')
parser.add_argument('--seed', type=int, default=1, metavar='S',
                    help='random seed (default: 1)')
parser.add_argument('--log_interval', type=int, default=100, metavar='I',
                    help="""how many batches to wait before logging detailed
                            training status, 0 means never log """)
parser.add_argument('--dataset', type=str, default='mnist', metavar='D',
                    help='Options are mnist and fashion_mnist')
parser.add_argument('--data_dir', type=str, default='../data/', metavar='F',
                    help='Where to put data')
parser.add_argument('--name', type=str, default='', metavar='N',
                    help="""A name for this training run, this
                            affects the directory so use underscores and not spaces.""")
parser.add_argument('--model', type=str, default='default', metavar='M',
                    help="""Options are default, q7_0.5x_channels, q7_1x_channels,
                            q7_2x_channels, q8_batchnorm, q9_dropout, q10_dropout_batchnorm,
                            q11_extra_conv, q12_remove_layer, q13_ultimate.""")
parser.add_argument('--test', type=str, default='', metavar='T',
                    help="""Run a unit test to make sure all models can be created,
                            options are the empty string, no test runs, or 'models'.""")
args = parser.parse_args()
args.cuda = not args.no_cuda and torch.cuda.is_available()

torch.manual_seed(args.seed)
if args.cuda:
    torch.cuda.manual_seed(args.seed)

kwargs = {'num_workers': 1, 'pin_memory': True} if args.cuda else {}

# choose the dataset
if args.dataset == 'mnist':
    DatasetClass = datasets.MNIST
elif args.dataset == 'fashion_mnist':
    DatasetClass = datasets.FashionMNIST
else:
    raise ValueError('unknown dataset: ' + args.dataset + ' try mnist or fashion_mnist')


def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
    """ Add a timestamp to your training run's name.
    """
    # http://stackoverflow.com/a/5215012/99379
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

training_run_name = timeStamped(args.dataset + '_' + args.name)

# Create the dataset, mnist or fasion_mnist
dataset_dir = os.path.join(args.data_dir, args.dataset)
training_run_dir = os.path.join(args.data_dir, training_run_name)
train_dataset = DatasetClass(
    dataset_dir, train=True, download=True,
    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ]))
train_loader = torch.utils.data.DataLoader(
    train_dataset, batch_size=args.batch_size, shuffle=True, **kwargs)
test_dataset = DatasetClass(
    dataset_dir, train=False, transform=transforms.Compose([
                    transforms.ToTensor(),
                    transforms.Normalize((0.1307,), (0.3081,))
                ]))
test_loader = torch.utils.data.DataLoader(
    test_dataset, batch_size=args.test_batch_size, shuffle=True, **kwargs)

# Set up visualization and progress status update code
callback_params = {'epochs': args.epochs,
                   'samples': len(train_loader) * args.batch_size,
                   'steps': len(train_loader),
                   'metrics': {'acc': np.array([]),
                               'loss': np.array([]),
                               'val_acc': np.array([]),
                               'val_loss': np.array([])}}
callbacks = callbacks.CallbackList(
    [callbacks.BaseLogger(),
     callbacks.TQDMCallback(),
     callbacks.CSVLogger(filename=training_run_dir + training_run_name + '.csv')])
callbacks.set_params(callback_params)

writer = SummaryWriter(log_dir=training_run_dir, comment=args.dataset + '_embedding_training')

# show some image examples in tensorboard projector with inverted color
images = 255 - test_dataset.test_data[:100].float()
label = test_dataset.test_labels[:100]
features = images.view(100, 784)
writer.add_embedding(features, metadata=label, label_img=images.unsqueeze(1))

# TODO Add classes for every option listed under the --model parser argument above.

# Define the neural network classes


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


class Q7HalfChannelsNet(nn.Module):
    def __init__(self):
        super(Q7HalfChannelsNet, self).__init__()
        # TODO Implement me
        print('TODO implement me')

    def forward(self, x):
        # TODO Implement me
        print('TODO implement me')


class Q13UltimateNet(nn.Module):

    def __init__(self):
        super(Q13UltimateNet, self).__init__()
        # TODO Implement me
        print('TODO implement me')

    def forward(self, x):
        # TODO Implement me
        print('TODO implement me')


# TODO add all the other models here if their parameter is specified
if args.model == 'default':
    model = Net()
elif args.model == 'q13_ultimate':
    model = Q13UltimateNet()

else:
    raise ValueError('Unknown model type: ' + str(args.model))


if args.test == 'models':
    # TODO create all models and at least call their init and forward functions
    model = Net()
    model = Q13UltimateNet()
    batch_size = 1000
    test_batch_size = 1000
    epochs_to_run = 1
else:
    epochs_to_run = args.epochs


writer.add_graph(model, images[:2])

if args.cuda:
    model.cuda()

print('args.optimizer: ' + args.optimizer)
if args.optimizer == 'sgd':
    print('sgd<<<<')
    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)
elif args.optimizer == 'adam':
    optimizer = optim.Adam(model.parameters())
elif args.optimizer == 'rmsprop':
    optimizer = optim.RMSprop(model.parameters())
else:
    raise ValueError('Unsupported optimizer: ' + args.optimizer)

total_minibatch_count = 0


def train(epoch, total_minibatch_count):
    # Training
    model.train()
    correct_count = np.array(0)
    for batch_idx, (data, target) in enumerate(train_loader):
        callbacks.on_batch_begin(batch_idx)
        if args.cuda:
            data, target = data.cuda(), target.cuda()
        data, target = Variable(data), Variable(target)
        optimizer.zero_grad()

        # Forward prediction step
        output = model(data)
        loss = F.nll_loss(output, target)

        # Backpropagation step
        loss.backward()
        optimizer.step()

        # The batch has ended, determine the
        # accuracy of the predicted outputs
        _, argmax = torch.max(output, 1)

        # target labels and predictions are
        # categorical values from 0 to 9.
        accuracy = (target == argmax.squeeze()).float().mean()
        pred = output.data.max(1, keepdim=True)[1]  # get the index of the max log-probability
        correct_count += pred.eq(target.data.view_as(pred)).cpu().sum()

        batch_logs = {
            'loss': np.array(loss.data[0]),
            'acc': np.array(accuracy.data[0]),
            'size': np.array(len(target))
        }

        batch_logs['batch'] = np.array(batch_idx)
        callbacks.on_batch_end(batch_idx, batch_logs)

        if args.log_interval != 0 and total_minibatch_count % args.log_interval == 0:
            # put all the logs in tensorboard
            for name, value in six.iteritems(batch_logs):
                    writer.add_scalar(name, value, global_step=total_minibatch_count)

            # put all the parameters in tensorboard histograms
            for name, param in model.named_parameters():
                name = name.replace('.', '/')
                writer.add_histogram(name, param.data.cpu().numpy(), global_step=total_minibatch_count)
                writer.add_histogram(name + '/gradient', param.grad.data.cpu().numpy(), global_step=total_minibatch_count)

        total_minibatch_count += 1

    # display the last batch of images in tensorboard
    img = torchvision.utils.make_grid(255 - data.data, normalize=True, scale_each=True)
    writer.add_image('images', img, global_step=total_minibatch_count)

    return total_minibatch_count


def test(epoch, total_minibatch_count):
    # Validation Testing
    model.eval()
    test_loss = 0
    correct = 0
    progress_bar = tqdm(test_loader, desc='Validation')
    for data, target in progress_bar:
        if args.cuda:
            data, target = data.cuda(), target.cuda()
        data, target = Variable(data, volatile=True), Variable(target)
        output = model(data)
        test_loss += F.nll_loss(output, target, size_average=False).data[0]  # sum up batch loss
        pred = output.data.max(1, keepdim=True)[1]  # get the index of the max log-probability
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()

    test_size = np.array(len(test_loader.dataset), np.float32)
    test_loss /= test_size

    acc = np.array(correct, np.float32) / test_size
    epoch_logs = {'val_loss': np.array(test_loss),
                  'val_acc': np.array(acc)}
    for name, value in six.iteritems(epoch_logs):
        writer.add_scalar(name, value, global_step=total_minibatch_count)
    callbacks.on_epoch_end(epoch, epoch_logs)
    progress_bar.write(
        'Epoch: {} - validation test results - Average val_loss: {:.4f}, val_acc: {}/{} ({:.2f}%)'.format(
            epoch, test_loss, correct, len(test_loader.dataset),
            100. * correct / len(test_loader.dataset)))

    return acc

# Run the primary training loop, starting with validation accuracy of 0
val_acc = 0
callbacks.on_train_begin()
for epoch in range(1, epochs_to_run + 1):
    callbacks.on_epoch_begin(epoch)
    # train for 1 epoch
    total_minibatch_count = train(epoch, total_minibatch_count)
    # validate progress on test dataset
    val_acc = test(epoch, total_minibatch_count)
callbacks.on_train_end()
writer.close()

if val_acc > 0.92 and val_acc <= 1.0:
    print("Congratulations, you beat the Question 13 minimum with ({:.2f}%) validation accuracy!".format(val_acc))
