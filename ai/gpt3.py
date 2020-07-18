'''
author @yash

GPT-3 Sandbox to finetune and train model to generate output for sheets
'''

import openai

def fineTune(request):
	key = open("key.txt", "r")
	fineTuneData = open("fineTuneData.txt", "r")
	question = "Q: " + request
	openai.api_key = key.read()
	a = openai.Completion.create(
	  engine="davinci",
	  prompt= fineTuneData.read() + request,
	  max_tokens=100,
	  stop="\n"	
	)
	print(a)
    



if __name__ == '__main__':
	fineTune("I bought $3000 software to be repaid in 1 month")