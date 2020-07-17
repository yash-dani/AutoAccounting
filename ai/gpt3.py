'''
author @yash

GPT-3 Sandbox to finetune and train model to generate output for sheets
'''

import openai

def fineTune():
	key = open("key.txt", "r")
	openai.api_key = key.read()
	a = openai.Completion.create(
	  engine="davinci",
	  prompt="Q: I bought a $30000 car on credit to be repaid in 5 years. A: add(30000, Property, Plant, Equipment); add (30000, Long-Term Debt) Q: I bought $20000 of equipment to be repaid in 2 months. A: add(20000, Property, Plant, Equipment); add(20000, Short-Term Loans) Q: A customer owes me $150 for his purchases. A: add(150, Accounts Receivable) Q: I bought $3000 software to be repaid in 1 month",
	  max_tokens=100
	)
	print(a)
    



if __name__ == '__main__':
	fineTune()