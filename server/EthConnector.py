from web3 import Web3


provider = Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v11/K22BWUGCWQVDIJYJV5IAJTK3FWWFNKFST4')
w3 = Web3(provider)


contract_address = Web3.to_checksum_address("0x4d6B6Df0BD2CF0E96A74746399F35bA818cBbeC4")
contract_abi = [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "id",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "D",
          "type": "string"
        }
      ],
      "name": "addOperation",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "op",
          "type": "address"
        }
      ],
      "name": "addToWhitelist",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getOperations",
      "outputs": [
        {
          "components": [
            {
              "internalType": "uint256",
              "name": "id",
              "type": "uint256"
            },
            {
              "internalType": "string",
              "name": "data",
              "type": "string"
            },
            {
              "internalType": "uint256",
              "name": "status",
              "type": "uint256"
            }
          ],
          "internalType": "struct Contract.OperationData[]",
          "name": "",
          "type": "tuple[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "op",
          "type": "address"
        }
      ],
      "name": "removeFromWhitelist",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "id",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "s",
          "type": "uint256"
        }
      ],
      "name": "setStatus",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
]


contract = w3.eth.contract(address=contract_address, abi=contract_abi)


sender_address = Web3.to_checksum_address("0x883d473C3b136315e9e491E5D1Ab9f4EaC667F0e")
private_key = "e78950d8e70f36a4c5c8fdda2ccb240fdaef719b7d1062880df38c664acd48d0"  # Replace with secure method


w3.eth.defaultAccount = sender_address


def send_transaction(function, *args):
    try:
        
        nonce = w3.eth.get_transaction_count(sender_address)
        transaction = function(*args).buildTransaction({
            'gas': 2000000,
            'gasPrice': w3.toWei('50', 'gwei'),
            'nonce': nonce,
        })

        
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

        
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

       
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        print(f"Transaction Hash: {tx_hash.hex()}")
        print(f"Transaction Receipt: {tx_receipt}")
        return tx_receipt
    except Exception as e:
        print(f"Error occurred: {e}")
        return None



def get_operations():
    try:
        operations = contract.functions.getOperations().call()
        print("Operations List:")
        for op in operations:
            print(f"ID: {op[0]}, Data: {op[1]}, Status: {op[2]}")
        return operations
    except Exception as e:
        print(f"Error fetching operations: {e}")
        return None


print(" ===================== MallEZ Admin Terminal ========================")
while True:
    print("Available Commands:")
    print("1 => addToWhiteList(address) : Adds address to whiteList, Requires Address ")
    print("2 => removeFromWhiteList(address) : Removes address from whiteList, Requires Address ")

    try:
        x = int(input("Enter your choice (integer 1-8) : "))
        if x == 1:
            s = input("Enter Address to add to whitelist: ")
            send_transaction(contract.functions.addToWhitelist, Web3.to_checksum_address(s))
        elif x == 2:
            s = input("Enter Address to remove from whitelist: ")
            send_transaction(contract.functions.removeFromWhitelist, Web3.to_checksum_address(s))
        else:
            print("Invalid choice! Please select 1 or 2.")
    except ValueError:
        print("Invalid input! Please enter a valid integer.")
    except KeyboardInterrupt:
        print("\nExiting the admin terminal...")
        break
