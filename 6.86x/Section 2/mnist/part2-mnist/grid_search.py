import nnet_fc
import numpy as np
import torch
import torch.nn as nn

def search(hidden_size=10):
    print(f'\nBaseline{" hidden {hidden_size}" if hidden_size != 10 else ""}:')
    np.random.seed(12321)  # for reproducibility
    torch.manual_seed(12321)  # for reproducibility
    nnet_fc.main(size=hidden_size)

    print(f'\nBatch size 64{" hidden {hidden_size}" if hidden_size != 10 else ""}:')
    np.random.seed(12321)  # for reproducibility
    torch.manual_seed(12321)  # for reproducibility
    nnet_fc.main(batch_size=64, size=hidden_size)

    print(f'\nLearning Rate 0.01{" hidden {hidden_size}" if hidden_size != 10 else ""}:')
    np.random.seed(12321)  # for reproducibility
    torch.manual_seed(12321)  # for reproducibility
    nnet_fc.main(lr=0.01, size=hidden_size)

    print(f'\nMomentum 0.9{" hidden {hidden_size}" if hidden_size != 10 else ""}:')
    np.random.seed(12321)  # for reproducibility
    torch.manual_seed(12321)  # for reproducibility
    nnet_fc.main(momentum=0.9, size=hidden_size)

    print(f'\nActivation LeakyReLU{" hidden {hidden_size}" if hidden_size != 10 else ""}:')
    np.random.seed(12321)  # for reproducibility
    torch.manual_seed(12321)  # for reproducibility
    nnet_fc.main(activation=nn.LeakyReLU, size=hidden_size)

if __name__ == '__main__':
    search()
    search(128)
