import gpt3
from sheets import balanceSheet
from utils import clear


if __name__ == '__main__':
	print('Welcome to the Balance Sheet Maker, powered by GPT-3')
	print('This turns your informal statements about transactions into formal statements!')
	print()
	print()
	while True:
		statement = balanceSheet()
		request = input("Tell me about your transaction: ")
		transactionInfo = gpt3.getGPT3(request)
		if type(transactionInfo) == list:
			# Successfully created output
			for transaction in transactionInfo:
				print("Adding ",transaction[1], "to ", transaction[2])
				statement.add(transaction[1],transaction[2])
		else:
			# Error in parsing message
			print('GPT-3 was not able to process your statement. Try rewording it!')
			clear()

