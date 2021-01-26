"""
  Script to test conda installation of deep learning packages
"""
import importlib
import os
import sys


def test_imports():
    """
      Tests importing base packages
    """
    print("#### \t Testing package import \t ####\n\n")
    packages_to_test = [
        "pandas", "scipy", "numpy", "sklearn", "tensorflow",  "keras", "torch", "xgboost", "lightgbm", 
        "catboost", "dask", "arrow", "attrdict", "mkl", "chainer", "ax", "botorch", "optuna"

    ]

    print(sys.version)
    for package in packages_to_test:
        try:
            _ = importlib.import_module(package)
            print("\t", _.__name__, "\t", "\t: Success!")
        except (ImportError, AttributeError) as err:
            print("\t", package, "\t: Error:", err)
            sys.exit("\tError in test_imports")


def test_tf_install():
    try:
        print("\n\n#### \t Testing Tensorflow \t ####")
        import tensorflow as tf
        hello = tf.constant("hello TensorFlow!")
        sess = tf.Session()
        print(sess.run(hello))
    except Exception as err:
        print("\tError:", err)
        sys.exit("\tError in test_tf_install")

def test_keras_install():
    # Keras check
    try:
        import keras
        print("#### \t Testing Keras \t ####\n\n")
        from keras.datasets import mnist
        from keras.models import Sequential
        from keras.layers import Dense, Dropout
        from keras.optimizers import RMSprop

        batch_size = 30
        num_classes = 10
        epochs = 1

        # the data, split between train and test sets
        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        # print(x_train.shape, y_train.shape )
        x_train = x_train[:90, :, :]
        x_test = x_test[:90, :, :]

        y_train = y_train[:90]
        y_test = y_test[:90]

        x_train = x_train.reshape(90, 784)
        x_test = x_test.reshape(90, 784)
        x_train = x_train.astype('float32')
        x_test = x_test.astype('float32')
        x_train /= 255
        x_test /= 255
        # print(x_train.shape[0], 'train samples')
        # print(x_test.shape[0], 'test samples')

        # convert class vectors to binary class matrices
        y_train = keras.utils.to_categorical(y_train, num_classes)
        y_test = keras.utils.to_categorical(y_test, num_classes)

        model = Sequential()
        model.add(Dense(512, activation='relu', input_shape=(784,)))
        model.add(Dropout(0.2))
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(num_classes, activation='softmax'))

        model.summary()

        model.compile(loss='categorical_crossentropy',
                      optimizer=RMSprop(),
                      metrics=['accuracy'])

        history = model.fit(x_train, y_train,
                            batch_size=batch_size,
                            epochs=epochs,
                            verbose=1,
                            validation_data=(x_test, y_test))
        score = model.evaluate(x_test, y_test, verbose=0)
        print('\t Keras installation-test :  loss:', score[0])
        print('\t Keras installation-test :  accuracy:', score[1])

    except Exception as err:
        print("\tError:", err)
        sys.exit("\tError in test_keras_install")

def test_ax_install():

    print("\n\n#### \t Testing AX \t ####")
    try:
        from ax import optimize
        best_parameters, best_values, experiment, model = optimize(
            parameters=[
                {
                    "name": "x1",
                    "type": "range",
                    "bounds": [-3.0, 3.0],
                },
                {
                    "name": "x2",
                    "type": "range",
                    "bounds": [-3.0, 3.0],
                },
            ],
            # Booth function
            evaluation_function=lambda p: (
                p["x1"] + 2*p["x2"] - 7)**2 + (2*p["x1"] + p["x2"] - 5)**2,
            minimize=True,
            total_trials=1
        )
        print("\tAX", "\t Best parameters: ", best_parameters)
    except Exception as err:
        print("\tAX", "\t: Error:", err)
        sys.exit("\tError in test_ax_install")

def test_sklearn_install():

    print("\n\n#### \t Testing Sklearn \t ####")
    try:
        import sklearn
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.datasets import make_classification

        X, y = make_classification(n_samples=1000, n_features=4,
                                   n_informative=2, n_redundant=0,
                                   random_state=0, shuffle=False)
        clf = RandomForestClassifier(n_estimators=100, max_depth=2,
                                     random_state=0)
        clf.fit(X, y)
        RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
                               max_depth=2, max_features='auto', max_leaf_nodes=None,
                               min_impurity_decrease=0.0, min_impurity_split=None,
                               min_samples_leaf=1, min_samples_split=2,
                               min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=None,
                               oob_score=False, random_state=0, verbose=0, warm_start=False)
        # print(clf.feature_importances_)
        # print(clf.predict([[0, 0, 0, 0]]))

        print("\tSklearn", "\t Feature importances: ", clf.feature_importances_)
    except Exception as err:
        print("\tSklearn", "\t: Error:", err)
        sys.exit("\tError in test_sklearn_install")

def test_pytorch_install():

    print("\n\n#### \t Testing PyTorch \t ####")
    try:

        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        import torch.optim as optim

        class Net(nn.Module):
            def __init__(self):
                super(Net, self).__init__()
                self.conv1 = nn.Conv2d(1, 20, 5, 1)
                self.conv2 = nn.Conv2d(20, 50, 5, 1)
                self.fc1 = nn.Linear(4*4*50, 500)
                self.fc2 = nn.Linear(500, 10)

        def forward(self, x):
            x = F.relu(self.conv1(x))
            x = F.max_pool2d(x, 2, 2)
            x = F.relu(self.conv2(x))
            x = F.max_pool2d(x, 2, 2)
            x = x.view(-1, 4*4*50)
            x = F.relu(self.fc1(x))
            x = self.fc2(x)
            return F.log_softmax(x, dim=1)

        def train(args, model, device, train_loader, optimizer, epoch):
            model.train()
            for batch_idx, (data, target) in enumerate(train_loader):
                data, target = data.to(device), target.to(device)
                optimizer.zero_grad()
                output = model(data)
                loss = F.nll_loss(output, target)
                loss.backward()
                optimizer.step()
                if batch_idx % args.log_interval == 0:
                    print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                        epoch, batch_idx *
                        len(data), len(train_loader.dataset),
                        100. * batch_idx / len(train_loader), loss.item()))

        def test(args, model, device, test_loader):
            model.eval()
            test_loss = 0
            correct = 0
            with torch.no_grad():
                for data, target in test_loader:
                    data, target = data.to(device), target.to(device)
                    output = model(data)
                    # sum up batch loss
                    test_loss += F.nll_loss(output,
                                            target, reduction='sum').item()
                    # get the index of the max log-probability
                    pred = output.argmax(dim=1, keepdim=True)
                    correct += pred.eq(target.view_as(pred)).sum().item()

            test_loss /= len(test_loader.dataset)

            print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
                test_loss, correct, len(test_loader.dataset),
                100. * correct / len(test_loader.dataset)))

        def launch_test():
            torch.manual_seed(3)
            device = torch.device("cpu") if not torch.cuda.is_available() else torch.device("cuda")

            kwargs = {}
            train_loader = torch.utils.data.DataLoader(
                datasets.MNIST('../data', train=True, download=True,
                               transform=transforms.Compose([
                                   transforms.ToTensor(),
                                   transforms.Normalize((0.1307,), (0.3081,))
                               ])),
                batch_size=args.batch_size, shuffle=True, **kwargs)
            test_loader = torch.utils.data.DataLoader(
                datasets.MNIST('../data', train=False, transform=transforms.Compose([
                    transforms.ToTensor(),
                    transforms.Normalize((0.1307,), (0.3081,))
                ])),
                batch_size=args.test_batch_size, shuffle=True, **kwargs)

            model = Net().to(device)
            optimizer = optim.SGD(model.parameters(),
                                  lr=args.lr, momentum=args.momentum)

            for epoch in range(1, 2):
                train(args, model, device, train_loader, optimizer, epoch)
                test(args, model, device, test_loader)

            if (args.save_model):
                torch.save(model.state_dict(), "mnist_cnn.pt")

        launch_test()

        print("\tPyTorch", "\t test complete")
    except Exception as err:
        print("\tPyTorch", "\t: Error:", err)
        # sys.exit("\tError in test_pytorch_install")

if __name__ == '__main__':

    print("\n\nConda env: ", sys.executable)
    # run test to check if all imports are working
    test_imports()
    test_tf_install()
    test_keras_install()
    test_ax_install()
    test_sklearn_install()
    test_pytorch_install()

    print("\n\n#### \t Test run complete \t ####\n\n")
