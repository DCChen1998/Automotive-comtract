#from web3utils.web3 import Web3, HTTPProvider
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
#from web3utils.web3.contract import ConciseContract
#from web3.utils.currency import to_wei
#from web3utils.currency import to_wei
import json

with open('.././build/contracts/CarRenter.json' , 'r') as f:
    data = json.loads(f.read())

abi = data['abi']
for dic in data['networks']:
    #print(dic)
    address = data['networks'][dic]['address']

config = {
    'abi': abi,
    'address': address,
    
}

web3 = Web3(HTTPProvider('http://localhost:8545'))
owner = web3.eth.accounts[0]
customer = web3.eth.accounts[1]
contract_instance = web3.eth.contract(address=config['address'], abi=config['abi']) 
eth = Web3.toWei(1, 'ether')


def Create_Vtoken(_name, _age):
    transact_hash = contract_instance.functions.Create_Vtoken(_name, _age).transact({'from': owner})
    return transact_hash

def Rent_Car(_tokenId):
    transact_hash = contract_instance.functions.Rent_Car(_tokenId).transact({'from': customer, 'value': eth})
    return transact_hash

def Return_Car(_tokenId, _oil, crashes, rate):
    #transact_hash = contract_instance.Return_Car(_tokenId, _oil, crashes, rate, transact={'from': customer})
    
    if (crashes == 0):
       transact_hash2 = contract_instance.functions.Return_Bail(_tokenId).transact({'from': owner, 'value': eth})
    
    transact_hash = contract_instance.functions.Return_Car(_tokenId, _oil, crashes, rate).transact({'from': customer})
    transact_receipt = web3.eth.getTransactionReceipt(transact_hash)
    logs = contract_instance.events.Price().processReceipt(transact_receipt)
    print(logs[0]['args']['_price'])
    price = logs[0]['args']['_price']
    price = Web3.toWei(price, 'szabo') * 1000
    transact_hash2 = contract_instance.functions.Pay_Owner(_tokenId).transact({'from': customer, 'value': price})

    return transact_hash

def Is_Rented(_id):
    transact_hash = contract_instance.functions.Is_Rented(_id).call() #, transact={'from': owner}
    return transact_hash

def Get_Available_Car():
    transact_hash = contract_instance.functions.Get_Available_Car_Num().call()
    print(transact_hash)

    transact_hash2 = contract_instance.functions.Get_All_Cars().transact({'from': customer})
    transact_receipt = web3.eth.getTransactionReceipt(transact_hash2)
    logs = contract_instance.events.AvailableCar().processReceipt(transact_receipt)

    car_list = []
    for i in range(transact_hash):
        if logs[i]['args']['_rate_num'] == 0:
            rate = 0
        else:
            rate = logs[i]['args']['_rate_sum'] / logs[i]['args']['_rate_num']
        
        print("ID: {0} Name: {1} Rate: {2}".format(logs[i]['args']['_id'], logs[i]['args']['_name'], rate))
        car_list.append({'ID': logs[i]['args']['_id'], 'Name': logs[i]['args']['_name'], 'Rate': rate})
    return car_list
    
'''
print(Web3.fromWei(web3.eth.getBalance(owner), 'ether'))
print(Web3.fromWei(web3.eth.getBalance(customer), 'ether'))
print('create')
Create_Vtoken('b', 2)
Create_Vtoken('c', 10)
print(Web3.fromWei(web3.eth.getBalance(owner), 'ether'))
print(Web3.fromWei(web3.eth.getBalance(customer), 'ether'))
print(bool(Is_Rented(0)))
Get_Available_Car()
print('rent')
Rent_Car(0)
print(Web3.fromWei(web3.eth.getBalance(owner), 'ether'))
print(Web3.fromWei(web3.eth.getBalance(customer), 'ether'))
print(bool(Is_Rented(0)))
Get_Available_Car()
print('return')
Return_Car(0, 1, 0, 5)
print(bool(Is_Rented(0)))
print(Web3.fromWei(web3.eth.getBalance(owner), 'ether'))
print(Web3.fromWei(web3.eth.getBalance(customer), 'ether'))
Get_Available_Car()
'''