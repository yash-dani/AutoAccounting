'''
authors: @yash-dani @georgekysaad
date: July 2020
Turn informat statements into requests to update balance sheets using GPT-3 
'''

import ast # standard library
import openai # 3rd party packages
import json

'''
	Function to turn informal request into transactional statement 
'''
def getGPT3(request):

	# setup key and fine tuning data
	key = open("key.txt", "r")
	fineTuneData = open("fineTuneData.txt", "r")
	question = "Q: " + request
	openai.api_key = key.read()

	# request completion from GPT-3
	output = openai.Completion.create(
	  engine="davinci",
	  prompt= fineTuneData.read() + question + "\n",
	  max_tokens=100,
	  temperature=0.4,
	  stop=["Q: ",'\n']	
	)

	# process output
	try:
		output = json.loads(output["choices"][0]["text"].replace('A:',''))
	except:
		output = output["choices"][0]["text"].replace('A: ','')


	return output
