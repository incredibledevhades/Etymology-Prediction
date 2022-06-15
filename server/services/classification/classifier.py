from flask import Flask
import torch
import math

from .model.load_model import NB_CHARS, NB_CATEGORIES, ALL_CHARS, model


def word_to_tensor(word):
    tensor = torch.zeros(len(word), 1, NB_CHARS)
    for i, letter in enumerate(word):
        tensor[i][0][ALL_CHARS.index(letter)] = 1
    return tensor


def run_rnn_model_prediction(word_tensor):
    hidden = model.initHidden()
    for i in range(word_tensor.size()[0]):
        output, hidden = model(word_tensor[i], hidden)
    return output


def tensor_to_etymology(out_tensor):
    etymology_pred_probs = []
    topv, topi = out_tensor.topk(NB_CATEGORIES, 1, True)
    for i in range(NB_CATEGORIES):
        category = ["Latin", "Germanic"][topi[0][i].item()]
        probability = math.exp(topv[0][i].item())
        etymology_pred_probs.append({category: probability})
    return etymology_pred_probs


def predict(word):
    in_tensor = word_to_tensor(word)
    out_tensor = run_rnn_model_prediction(in_tensor)
    word_etymology_pred_probs = tensor_to_etymology(out_tensor)
    return word_etymology_pred_probs
