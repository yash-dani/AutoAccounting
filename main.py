import gpt3 # user generated packages
from sheets import balanceSheet
from utils import clear


if __name__ == '__main__':
	clear()
	# Intro text
	print("------------------------------------------------------")
	print('Welcome to the Balance Sheet Maker, powered by GPT-3.')
	print("")
	print('Your transaction -> python code -> Google Sheets file')
	print("-----------------------------------------------------")
	print()
	statement = balanceSheet()
	# Loop to make requests to bot
	while True:
		print()
		request = input("Tell me about your transaction:\n")
		transactionInfo = gpt3.getGPT3(request) # get GPT-3 Output
		#print(transactionInfo)
		if type(transactionInfo) == list:
			# Successfully parsed output
			print()
			print("Results:")
			for transaction in transactionInfo:
				print(transaction[0],transaction[1], "to ", transaction[2])
				statement.update(transaction[0], transaction[1],transaction[2])
		else:
			# Error in parsing gpt3
			print('GPT-3 was not able to process your statement. Try rewording it!')
			clear()
