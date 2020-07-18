'''
author @yash

GPT-3 Sandbox to finetune and train model to generate output for sheets
'''

import openai
import ast 

def generateCommand(request):
	key = open("key.txt", "r")
	fineTuneData = open("fineTuneData.txt", "r")
	question = "Q: " + request
	openai.api_key = key.read()
	output = openai.Completion.create(
	  engine="davinci",
	  prompt= fineTuneData.read() + request,
	  max_tokens=100,
	  stop="\n"	
	)
	output = ast.literal_eval(output["choices"][0]["text"].replace('A: ',''))
	return output
    