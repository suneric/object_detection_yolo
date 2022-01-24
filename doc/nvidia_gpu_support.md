## nvidia gpu support

## Install nvidia driver and cuda application
- check the system driver requirement (assume ubuntu 18.04)
```
ubuntu-drivers devices
```
- Geforce RTX1070, nvidia-driver-450, cuda 11.0, cudnn 8.0.
  Follow the instruction of [TensorFlow GPU Support](https://www.tensorflow.org/install/gpu) to install cuda and cudnn.

- GeForce RTX3070, nvidia-driver-460, cuda 11.2, cudnn 8.1.
  Follow the [instruction](https://docs.nvidia.com/deeplearning/cudnn/install-guide/index.html) to install cuda and cudnn  
  ```
  wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
  sudo mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
  sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
  sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/ /"
  sudo apt-get update

  sudo apt-get install libcudnn8=8.1.0.77-1+cuda11.2
  sudo apt-get install libcudnn8-dev=8.1.0.77-1+cuda11.2
  ```

- check gpu enabled and [use gpu](https://www.tensorflow.org/guide/gpu) once tensorflow is installed
```
import tensorflow as tf
gpus = tf.config.list_physical_devices('GPU')
print(len(gpus))
```

## install cudatoolkit 11.0, cudnn 8 and tensorflow 2.4 in anaconda
- install cudatoolkit=11.0 with conda (latest shuld be 11.0.221)
- pip install tensorflow (latest should be 2.4)
- download cudnn 8 and unzip, copy the include files and lib64 file to your anaconda environment (include folder and lib folder)

## References
- [Tensorflow GPU support](https://www.tensorflow.org/install/gpu)
- [CUDA Compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/index.html)
- [Install TF2.4 with CUDA 11 and CUDNN 8](https://medium.com/analytics-vidhya/install-tensorflow-gpu-2-4-0-with-cuda-11-0-and-cudnn-8-using-anaconda-8c6472c9653f)
- [Deep Learning with RTX3090(CUDA, cuDNN, Tensorflow, Keeras, PyTorch)](https://medium.com/@dun.chwong/the-simple-guide-deep-learning-with-rtx-3090-cuda-cudnn-tensorflow-keras-pytorch-e88a2a8249bc)
- [How to install latest cuda](https://stackoverflow.com/questions/55256671/how-to-install-latest-cudnn-to-conda)
- [CUDA Application compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/index.html#cuda-application-compatibility)
