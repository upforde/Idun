#!/bin/sh

module purge
module load Anaconda3/2020.07

pip3 install gensim==3.8.1 --user
pip3 install numpy==1.19.2 --user
pip3 install regex==2019.12.20 --user
pip3 install scipy==1.3.2 --user
pip3 install sentencepiece==0.1.85 --user
pip3 install sklearn==0.0 --user
pip3 install spacy==3.1 --user
pip3 install torch==1.9.0+cu111 --user
pip3 install transformers==4.9.2 --user
pip3 install tqdm==4.41.0 --user
pip3 install jsonlines==1.2.0 --user
pip3 install nltk==3.5 --user
