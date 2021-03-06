import numpy as np
from nplm import Model
from charNgrams import nPhones
from argparse import ArgumentParser
import os


parser = ArgumentParser(description="model")
parser.add_argument('--input', nargs='?', default='/home/tlacomiston/Downloads/ENTROPY_data/script/corpora/',
	                    help='name of directory')
args = parser.parse_args()

directory = args.input
all_files = os.listdir(directory)

for n in all_files:
  inputcorpus=directory+n
  file=open(inputcorpus,'r', encoding="utf-8")

  #extrae los nphones, variar este parámetro implica tomar uniphones, triphones u otros
  phones = nPhones(file.read(),nphone_siz=1)
  phones.get_phones()

  print('\n\nCorpus:',n)
  #Aprende el modelo de Bengio
  model = Model(phones.word_phones, ngramas=2)
  model.train(its=51, batch=300)
  
  #Tamaño de nphones
  N = len(phones.voc)

  mu = np.zeros(N)
  Hnorm = np.zeros(N)
  H = np.zeros(N)
  for i,w in enumerate(model.voc.keys()):
    #print(phones.voc[w])
    pw = model.forward([w])
    # \sum_j p_ij*logN p_ij
    condHnorm = np.dot(pw,np.log(pw))/np.log(N)
    condH = np.dot(pw,np.log(pw))
    #Filling pre-conditional_entropies
    Hnorm[i] = condHnorm
    H[i] = condH

    #Filling pre-mu
    mu += pw

  #\sum_i mu_i \sum_j p_ij*logN p_ij
  Entropy = -np.dot(mu/mu.sum(0),H)
  Entropy_norm = -np.dot(mu/mu.sum(0),Hnorm)
  
  print('Corpus:', n)
  print('Entropía:', Entropy)
  print('Entropía norm:', Entropy_norm)
