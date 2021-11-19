DEPENDENCIES:
NOTE: LINUX VERSION. this means that If on windows you need to get visual c++ aswell * change / to \ .
install solidity programming language on ide (on vsCode its just an extension)
python: (using python 3.10)
Pandas: pip install pandas
web3: pip install web3 
solcx: pip install py-solc-x
pysimplegui: pip install pysimplegui

Get ganache app image (for Linux) at https://www.trufflesuite.com/ganache 
If on windows get and install ganache from same URL. 
	
Change ganache chain settings so that accounts start with A LOT of eth (under settings/accounts & keys, set something like 100000000000)



HOW TO USE (from terminal):

Start Ganache APPimage and click Quickstart Ethereum.

NOTE: everytime you interact with the chain, you can see what is happening on ganache, under either tab "transactions" or "blocks"!
      Also, the balances can be seen under accounts in order to follow transactions.
		However, note that some funds will disappear (around 0.1-0.2 ETH per transaction since they are gas fees)

	
1. python3 deployment.py 
	this script compiles the smart contract + it deployis it on-chain + it resets the various datasets that will be used.
	you will be asked for:
		public key
		private key in hexdecimal form (means that you need to add 0x infornt of private key)
	Click on the KEY icon next to a Ganache account to get public and private keys
	
2.Once the contract is deployed: python3 gui.py
	
	This start the gui.
	
	Input the public and private key of the account you want to use.
	
	Then you can choose to use that account to create or buy options -> by clicking create/buy
	
	If choose create, input the information that is asked (leverage, cap, strikeprice, price, expiry string (in form yyyy-mm-dd), expiry time (this means in how many minutes can the option be resolved))
	NOTE: for stirkeprice input at most 2 decimals in form int.dd, for other values for now only enter INTEGERS
	EXPIRIES: STRING will help check that the Oracle data corresponds to the preferred expiry day, it only gets resolved if the oracle data is for that day. INT would be such that the date has already passed and the data from alphavantage arrived. In testing, this is in minutes, since we are using past data and can be set arbitrarily. In the actual implemetation this would be set automatically by the python script to ensure the expiry INT is 1.5/2 days > the option expiry date.

The program will create the option and make te required payment (leverage*cap) automatically to chain.
	
	
	If choose buy:
		click view to see al available options (which have not been bought or resolved yet, and data related to them)
		enter the option number (which you can see in the table) to buy it from the selected account. 
		Again the program does the payments automatically
	
3. To resolve options: python3 resolveoptions.py
	you will need to input the close date for the options you want to resolve. Only options expiring on that date will resolve!
	it can be found at https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=TSLA&apikey=0F1FJH5TJ28W5ZZH
	input a public and private key to call function (only needed to pay gas fees)
	Done!

NOTE: the contract can countinue to be used after resolution and it should keep working just as described above. 
	If an new contract is deployed with deployment.py the programm updates so that it automatically connects to the NEW contract 

	

	
