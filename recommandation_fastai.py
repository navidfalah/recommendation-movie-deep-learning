# -*- coding: utf-8 -*-
"""recommandation.fastai

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LxvJ-IRHqCcA042YBbiAbCP6ioV1228t
"""

from fastai.collab import *
from fastai.tabular.all import *


path = untar_data(URLs.ML_100k)
ratings = pd.read_csv(path/'u.data', delimiter='\t', header=None,
                      names=['user', 'movie', 'rating', 'timestamp'])

ratings.head()

last_skywalker = np.array([0.98,0.9,-0.9])
user1 = np.array([0.9,0.8,-0.6])

(user1*last_skywalker).sum()

movies = pd.read_csv(path/'u.item',  delimiter='|', encoding='latin-1',
                     usecols=(0,1), names=('movie','title'), header=None)
movies.head()

ratings = ratings.merge(movies)
ratings.head()

dls = CollabDataLoaders.from_df(ratings, item_name='title', bs=64)
dls.show_batch()

n_users = len(dls.classes['user'])
n_movies = len(dls.classes['title'])
n_factors = 5

user_factors = torch.randn(n_users, n_factors)
movie_factors = torch.randn(n_movies, n_factors)

one_hot_3 = one_hot(3, n_users).float()
user_factors.t() @ one_hot_3

one_hot_3

user_factors[3]

x, y = dls.one_batch()
x.shape, y.shape

class DotProduct(Module):
 def __init__(self, n_users, n_movies, n_factors):
  self.user_factors = Embedding(n_users, n_factors)
  self.movie_factors = Embedding(n_movies, n_factors)

 def forward(self, x):
  users = self.user_factors(x[:,0])
  movies = self.movie_factors(x[:,1])
  return (users * movies).sum(dim=1)

model = DotProduct(n_users, n_movies, 50)
learn = Learner(dls, model, loss_func=MSELossFlat())

learn.fit_one_cycle(5, 5e-3)

class DotProduct(Module):
 def __init__(self, n_users, n_movies, n_factors, y_range=(0,5.5)):
  self.user_factors = Embedding(n_users, n_factors)
  self.movie_factors = Embedding(n_movies, n_factors)
  self.y_range = y_range

 def forward(self, x):
  users = self.user_factors(x[:,0])
  movies = self.movie_factors(x[:,1])
  return sigmoid_range((users * movies).sum(dim=1), *self.y_range)

model = DotProduct(n_users, n_movies, 50)
learn = Learner(dls, model, loss_func=MSELossFlat())
learn.fit_one_cycle(5, 5e-3)

class DotProductBias(Module):
 def __init__(self, n_users, n_movies, n_factors, y_range=(0,5.5)):
  self.user_factors = Embedding(n_users, n_factors)
  self.user_bias = Embedding(n_users, 1)
  self.movie_factors = Embedding(n_movies, n_factors)
  self.movie_bias = Embedding(n_movies, 1)
  self.y_range = y_range

 def forward(self, x):
  users = self.user_factors(x[:,0])
  movies = self.movie_factors(x[:,1])
  res = (users * movies).sum(dim=1, keepdim=True)
  res += self.user_bias(x[:,0]) + self.movie_bias(x[:,1])
  return sigmoid_range(res, *self.y_range)

model = DotProductBias(n_users, n_movies, 50)
learn = Learner(dls, model, loss_func=MSELossFlat())
learn.fit_one_cycle(5, 5e-3)

#### pass the wd for the l2 generalization of the weights

model = DotProduct(n_users, n_movies, 50)
learn = Learner(dls, model, loss_func=MSELossFlat())
learn.fit_one_cycle(5, 5e-3, wd=0.1)

class T(Module):
 def __init__(self): self.a = nn.Parameter(torch.ones(3))

L(T().parameters())

class T(Module):
 def __init__(self): self.a = nn.Linear(1, 3, bias=False)
t = T()
L(t.parameters())

def create_params(size):
 return nn.Parameter(torch.zeros(*size).normal_(0, 0.01))

class DotProductBias(Module):
 def __init__(self, n_users, n_movies, n_factors, y_range=(0,5.5)):
  self.user_factors = create_params([n_users, n_factors])
  self.user_bias = create_params([n_users])
  self.movie_factors = create_params([n_movies, n_factors])
  self.movie_bias = create_params([n_movies])
  self.y_range = y_range

 def forward(self, x):
  users = self.user_factors[x[:,0]]
  movies = self.movie_factors[x[:,1]]
  res = (users*movies).sum(dim=1)
  res += self.user_bias[x[:,0]] + self.movie_bias[x[:,1]]
  return sigmoid_range(res, *self.y_range)

model = DotProductBias(n_users, n_movies, 50)
learn = Learner(dls, model, loss_func=MSELossFlat())
learn.fit_one_cycle(5, 5e-3, wd=0.1)

movie_bias = learn.model.movie_bias.squeeze()
idxs = movie_bias.argsort()[:5]
[dls.classes['title'][i] for i in idxs]

learn = collab_learner(dls, n_factors=50, y_range=(0, 5.5))
learn.fit_one_cycle(5, 5e-3, wd=0.1)

learn.model

movie_bias = learn.model.i_bias.weight.squeeze()
idxs = movie_bias.argsort(descending=True)[:5]
[dls.classes['title'][i] for i in idxs]

### find the closest movie to the one movie
### as the distance between the embeddings should be the same

movie_factoes = learn.model.i_weight.weight
idx = dls.classes['title'].o2i['Silence of the Lambs, The (1991)']
distances = nn.CosineSimilarity(dim=1)(movie_factoes, movie_factoes[idx][None])
print(distances)
idx = distances.argsort(descending=True)[1]
dls.classes['title'][idx]

embs = get_emb_sz(dls)
embs

class CollabNN(Module):
 def __init__(self, user_sz, item_sz, y_range=(0,5.5), n_act=100):
  self.user_factors = Embedding(*user_sz)
  self.item_factors = Embedding(*item_sz)
  self.layers = nn.Sequential(
  nn.Linear(user_sz[1]+item_sz[1], n_act),
  nn.ReLU(),
  nn.Linear(n_act, 1))
  self.y_range = y_range

 def forward(self, x):
  embs = self.user_factors(x[:,0]),self.item_factors(x[:,1])
  x = self.layers(torch.cat(embs, dim=1))
  return sigmoid_range(x, *self.y_range)

model = CollabNN(*embs)

learn = Learner(dls, model, loss_func=MSELossFlat())
learn.fit_one_cycle(5, 5e-3, wd=0.01)

learn = collab_learner(dls, use_nn=True, y_range=(0, 5.5), layers=[100,50])
learn.fit_one_cycle(5, 5e-3, wd=0.1)

@delegates(TabularModel)
class EmbeddingNN(TabularModel):
 def __init__(self, emb_szs, layers, **kwargs):
 super().__init__(emb_szs, layers=layers, n_cont=0, out_sz=1, **kwargs)

