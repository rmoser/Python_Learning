import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from train_utils import batchify_data, run_epoch, train_model, Flatten
import utils_multiMNIST as U
path_to_data_dir = '../Datasets/'
use_mini_dataset = True

batch_size = 64
nb_classes = 10
nb_epoch = 30
num_classes = 10
img_rows, img_cols = 42, 28 # input image dimensions



class CNN(nn.Module):

    def __init__(self, input_dimension):
        super(CNN, self).__init__()
        self.flatten = Flatten()
        # TODO initialize model layers here
        self.conv_00 = nn.Conv2d(1, 32, (3, 3))
        self.conv_01 = nn.Conv2d(1, 32, (3, 3))

        self.maxp_10 = nn.MaxPool2d((2, 2))
        self.maxp_11 = nn.MaxPool2d((2, 2))

        self.drop_10 = nn.Dropout(0.5)
        self.drop_11 = nn.Dropout(0.5)

        self.conv_20 = nn.Conv2d(32, 64, (3, 3))
        self.conv_21 = nn.Conv2d(32, 64, (3, 3))

        self.maxp_30 = nn.MaxPool2d((2, 2))
        self.maxp_31 = nn.MaxPool2d((2, 2))

        self.linear_40 = nn.Linear(2880, 128)
        self.linear_41 = nn.Linear(2880, 128)

        self.linear_50 = nn.Linear(128, 10)
        self.linear_51 = nn.Linear(128, 10)

    def forward(self, x):

        # TODO use model layers to predict the two digits
        # print('x', x.shape)
        h00 = F.relu(self.conv_00(x))
        # print('h00', h00.shape)
        h10 = self.maxp_10(h00)
        # print('h10', h10.shape)
        h20 = F.relu(self.conv_20(h10))
        # print('h20', h20.shape)
        h30 = self.maxp_30(h20)
        # print('h30', h30.shape)
        h40 = self.flatten(h30)
        # print('h40', h40.shape)
        h50 = self.linear_40(h40)
        # print('h50', h50.shape)
        h60 = self.drop_10(h50)
        # print('h60', h60.shape)
        h70 = self.linear_50(h60)
        # print('h70', h70.shape)

        h01 = F.relu(self.conv_01(x))
        h11 = self.maxp_11(h01)
        h21 = F.relu(self.conv_21(h11))
        h31 = self.maxp_31(h21)
        h41 = self.flatten(h31)
        h51 = self.linear_41(h41)
        h61 = self.drop_11(h51)
        h71 = self.linear_51(h61)

        out_first_digit = h70
        out_second_digit = h71

        return out_first_digit, out_second_digit

def main():
    X_train, y_train, X_test, y_test = U.get_data(path_to_data_dir, use_mini_dataset)

    # Split into train and dev
    dev_split_index = int(9 * len(X_train) / 10)
    X_dev = X_train[dev_split_index:]
    y_dev = [y_train[0][dev_split_index:], y_train[1][dev_split_index:]]
    X_train = X_train[:dev_split_index]
    y_train = [y_train[0][:dev_split_index], y_train[1][:dev_split_index]]

    permutation = np.array([i for i in range(len(X_train))])
    np.random.shuffle(permutation)
    X_train = [X_train[i] for i in permutation]
    y_train = [[y_train[0][i] for i in permutation], [y_train[1][i] for i in permutation]]

    # Split dataset into batches
    train_batches = batchify_data(X_train, y_train, batch_size)
    dev_batches = batchify_data(X_dev, y_dev, batch_size)
    test_batches = batchify_data(X_test, y_test, batch_size)

    # Load model
    input_dimension = img_rows * img_cols
    model = CNN(input_dimension) # TODO add proper layers to CNN class above

    # Train
    train_model(train_batches, dev_batches, model)

    ## Evaluate the model on test data
    loss, acc = run_epoch(test_batches, model.eval(), None)
    print('Test loss1: {:.6f}  accuracy1: {:.6f}  loss2: {:.6f}   accuracy2: {:.6f}'.format(loss[0], acc[0], loss[1], acc[1]))

if __name__ == '__main__':
    # Specify seed for deterministic behavior, then shuffle. Do not change seed for official submissions to edx
    np.random.seed(12321)  # for reproducibility
    torch.manual_seed(12321)  # for reproducibility
    main()
