import gpt3 # user generated packages
from sheets import balanceSheet
from utils import clear


if __name__ == '__main__':

	# Intro text
	print('Welcome to the Balance Sheet Maker, powered by GPT-3')
	print('This turns your informal statements about transactions into formal statements!')
	print()
	print()
	statement = balanceSheet()
	# Loop to make requests to bot
	while True:
		
		request = input("Tell me about your transaction: ")

		transactionInfo = gpt3.getGPT3(request) # get GPT-3 Output
		print(transactionInfo)
		if type(transactionInfo) == list:
			# Successfully parsed output
			for transaction in transactionInfo:
				print(transaction[0],transaction[1], "to ", transaction[2])
				statement.update(transaction[0], transaction[1],transaction[2])
		else:
			# Error in parsing gpt3
			print('GPT-3 was not able to process your statement. Try rewording it!')
			clear()