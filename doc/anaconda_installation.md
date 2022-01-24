# Installing Anaconda on Linux

1. Download [Anaconda installer for Linux](https://www.anaconda.com/products/individual#linux)

2. Install Anaconda for Python 3.7 with command
```
bash ~/Downloads/Anaconda3-2020.11-Linux-x86_64.sh
```
or for Python 2.7 with command
```
bash ~/Downloads/Anaconda2-2019.10-Linux-x86_64.sh
```

3. Review the license agreement and enter 'Yes' to agree

4. Enter 'Yes' to initialize Anaconda3 by running 'conda init'

5. Close and open terminal window for the installation to take effect, or enter the command
```
source ~/.bashrc
```

6. To control whether or not each shell session has the base environment activated or not, run
```
conda config --set auto_activate_base False or True
```
This only works if you have run 'conda init' first

## Reference
- [Anaconda doc, installing on Linux](https://docs.anaconda.com/anaconda/install/linux/)
