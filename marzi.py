import os
import demoji
import requests
from requests_oauthlib import OAuth1Session

### GRAMMAR BOT HOST ###
grammar_host = 'https://api.grammarbot.io/v2/check'

### IMGFLIP HOST ###
meme_host = 'https://api.imgflip.com/caption_image'

def marzi_act(text):
    ### EDITING TEXT ###
    text = demoji.replace(text)
    text_list = text.split()
    new_text_list = []
    for index, word in enumerate(text_list):
        if word == '&amp;':
            new_text_list.append('and')
        elif word[0] == '#' or word[0] == '@':
            continue
        elif word[0:4] == 'http':
            continue
        else:
            new_text_list.append(word)
    res_text = ' '.join(new_text_list)

    ### GET RESPONSE FROM GRAMMAR BOT ###
    res = requests.get(grammar_host, params={'text': res_text, 'language': 'en-US'})
    result = res.json()

    if result['matches'] == []:
        return False
    ### CREATE MEME ###
    elif len(result['matches'][0]['replacements']) == 1:
        meme = requests.post(meme_host, params={
            'template_id': 438680,
            'username': 'sumarnowilly94',
            'password': 'Onramus1094',
            'text0': result['matches'][0]['context']['text'],
            'text1': '*' + result['matches'][0]['replacements'][0]['value']
        })
    else:
        meme = requests.post(meme_host, params={
            'template_id': 181913649,
            'username': 'sumarnowilly94',
            'password': 'Onramus1094',
            'text0': result['matches'][0]['context']['text'],
            'text1': result['matches'][0]['message']
        })
    meme = meme.json()
    url_meme = meme['data']['url']
    return url_meme