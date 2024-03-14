import sys, time, json, os
from ecdsa import VerifyingKey, SigningKey
from p2pnetwork.node import Node
from Crypto import Random
import hashlib
from Crypto.Cipher import AES

SERVER_ADDR = "zachcoin.net"
SERVER_PORT = 9067

class ZachCoinClient (Node):
    
    # ZachCoin Constants
    BLOCK = 0
    TRANSACTION = 1
    BLOCKCHAIN = 2
    UTXPOOL = 3
    COINBASE = 50
    DIFFICULTY = 0x0000007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

    # Hardcoded genesis block
    blockchain = [
        {
            "type": BLOCK,
            "id": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
            "nonce": "1950b006f9203221515467fe14765720",
            "pow": "00000027e2eb250f341b05ffe24f43adae3b8181739cd976ea263a4ae0ff8eb7",
            "prev": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
            "tx": {
                "type": TRANSACTION,
                "input": {
                    "id": "0000000000000000000000000000000000000000000000000000000000000000",
                    "n": 0
                },
                "sig": "adf494f10d30814fd26c6f0e1b2893d0fb3d037b341210bf23ef9705479c7e90879f794a29960d3ff13b50ecd780c872",
                "output": [
                    {
                        "value": 50,
                        "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
                    }
                ]
            }
        }
    ]
    # unverified transaction pool
    utx = []
  
    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(ZachCoinClient, self).__init__(host, port, id, callback, max_connections)

    def outbound_node_connected(self, connected_node):
        print("outbound_node_connected: " + connected_node.id)
        
    def inbound_node_connected(self, connected_node):
        print("inbound_node_connected: " + connected_node.id)

    def inbound_node_disconnected(self, connected_node):
        print("inbound_node_disconnected: " + connected_node.id)

    def outbound_node_disconnected(self, connected_node):
        print("outbound_node_disconnected: " + connected_node.id)

    def node_message(self, connected_node, data):
        #print("node_message from " + connected_node.id + ": " + json.dumps(data,indent=2))
        print("node_message from " + connected_node.id)

        if data != None:
            if 'type' in data:
                if data['type'] == self.TRANSACTION:
                    self.utx.append(data)
                elif data['type'] == self.BLOCKCHAIN:
                    self.blockchain = data['blockchain']
                elif data['type'] == self.UTXPOOL:
                    self.utx = data['utxpool']
                elif data['type'] == self.BLOCK:
                    # verify block
                    if self.validate_block(data):
                        print("Block added to blockchain.")
                        print("Block ID:", data['id'])
                        # remove transactions from utxpool
                        self.utx = list(
                            filter(lambda x: x['input']['id'] != data['tx']['input']['id'], self.utx))
                        # add block to blockchain
                        self.blockchain.append(data)
                    else:
                        print("Error: Invalid block received.")

    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")
        
    def transaction(self, sk: SigningKey, input_id: str, input_n: int, recipients: list[str], amounts: list[int]) -> dict:
        """
        Create a new unverified transaction
        """
        # generate outputs
        outputs = [{"value": amount, "pub_key": recipient} for recipient, amount in zip(recipients, amounts)]
        
        # format input
        input_obj = {
            "id": input_id,
            "n": input_n
        }
        
        # sign transaction
        signature = sk.sign(json.dumps(input_obj).encode("utf-8")).hex()
        
        utx = {
            "type": self.TRANSACTION,
            "input": input_obj,
            "sig": signature,
            "output": outputs
        }
        return utx
    
    
    def validate_block(self, block: dict) -> bool:
        """
        Ensure block is a valid ZachCoin block
        """
        if block['type'] != self.BLOCK or block['id'] != hashlib.sha256(json.dumps(block['tx'], sort_keys=True).encode('utf8')).hexdigest() or block['prev'] != self.blockchain[-1]['id'] or int(block['pow'], 16) > self.DIFFICULTY:
            print("Error: Block is not valid")
            return False
        # validate transaction within block
        return self.validate_transaction(block['tx'])
    

    def validate_transaction(self, tx: dict, validate_coinbase: bool = True) -> bool:
        """
        Ensure transaction is a valid ZachCoin transaction
        """
        # The transaction is structurally valid
        if 'type' not in tx or 'input' not in tx or 'sig' not in tx or 'output' not in tx or tx['type'] != self.TRANSACTION:
            print("Error: Transaction is not valid")
            return False
        # The transaction input is valid
        input_blocks = list(filter(
            lambda x: x['id'] == tx['input']['id'], self.blockchain))
        if len(input_blocks) == 0:
            print("Error: Transaction input refers to an invalid block")
            return False
        input_block = input_blocks[0]

        # ZC is valid (hasn't been spent yet)
        if len(list(filter(lambda x: x['tx']['input']['id'] == tx['input']['id'], self.blockchain))) > 1:
            print("Error: Transaction input is already spent")
            return False

        # Validate outputs
        if len(tx['output']) < 1 + int(validate_coinbase) or len(tx['output']) > 2 + int(validate_coinbase):
            print("Error: Transaction output count is not valid")
            return False
        sum = 0
        if validate_coinbase:
            sum -= self.COINBASE
        for output in tx['output']:
            if output['value'] <= 0:
                print("Error: Transaction output value is not positive")
                return False
            sum += output['value']
        if sum != input_block['tx']['output'][tx['input']['n']]['value']:
            print("Error: Transaction input value does not equal output value")
            return False

        # The coinbase output is correct (in value)
        if validate_coinbase and tx['output'][-1]['value'] != self.COINBASE:
            print("Error: Transaction coinbase value is not valid")
            return False

        # That the signature of the transaction verifies
        vk = VerifyingKey.from_string(bytes.fromhex(
            input_block['tx']['output'][tx['input']['n']]['pub_key']))
        try:
            vk.verify(bytes.fromhex(tx['sig']), json.dumps(
                tx['input'], sort_keys=True).encode('utf8'))
        except:
            print("Error: Transaction signature is not valid")
            return False
        print("Transaction is valid")
        return True
    

def get_transaction_input(client: ZachCoinClient, vk: VerifyingKey) -> tuple[str, int]:
    """
    Prompt the user to select an unspent transaction output
    """
    # get list of unspent transaction outputs
    unspent_outputs = []
    for i, block in enumerate(client.blockchain):
        for j, output in enumerate(block['tx']['output']):
            if output['pub_key'] == vk.to_string().hex():
                spent = False
                for blocks_spent in client.blockchain:
                    if blocks_spent['tx']['input']['id'] == block['id'] and blocks_spent['tx']['input']['n'] == j:
                        spent = True
                        break
                if not spent:
                    unspent_outputs.append((i, j))
    # print list of blocks
    print("Select an unspent transaction output from the blockchain:")
    for i, unspent_output in enumerate(unspent_outputs):
        block_index, output_index = unspent_output
        output = client.blockchain[block_index]['tx']['output'][output_index]
        print("-" * 20)
        print(f"OPTION #{i}\nBlock: {block_index}\nOutput: {output_index}\n{json.dumps(output, indent=1)}")
        print("-" * 20)
    x = input("Enter the OPTION # of the transaction output -> ")
    try:
        x = int(x)
    except:
        print("Error: Invalid block number.")
        raise Exception

    # check if input number is valid
    if x < 0 or x >= len(unspent_outputs):
        print("Error: Invalid number.")
        raise Exception
    block_index, output_index = unspent_outputs[x]
    return client.blockchain[block_index]['id'], output_index
    
    
def get_recipient(change: bool = False):
    """
    Get the recipient and amount for a new transaction
    """
    if change:
        print("\nOptional: Enter a second recipient to receive change. \
              Leave blank to skip.")
        
    recipient = input("Enter the recipient's public key -> ")
    amount = input("Enter the amount to send -> ")
    try:
        amount = int(amount)
        if amount <= 0:
            print("Error: Invalid amount.")
            raise Exception
    except:
        print("Error: Invalid amount.")
        raise Exception
    return recipient, amount


def create_transaction(client: ZachCoinClient, sk: SigningKey, vk: VerifyingKey):
    """
    Create a transaction and add it to the unverified transaction pool
    """
    # get input block
    try:
        input_id, input_n = get_transaction_input(client, vk)
        print("Input block:", input_id)
        print("Output number:", input_n)
        
        # parse recipient and amount
        recipient, amount = get_recipient()
        # optional second output for change
        self_recipient, change = get_recipient(change=True)
        
        recipients = [recipient] + ([self_recipient] if self_recipient else [])
        amounts = [int(amount)] + ([int(change)] if change else [])
        
        utx = client.transaction(sk, input_id, input_n, recipients, amounts)
        
        print("Creating transaction...", json.dumps(utx, indent=1))
        client.send_to_nodes(utx)
    except:
        print("Error: Transaction creation failed.")
        return


def mine_transaction(client: ZachCoinClient, vk: VerifyingKey):
    # check if there are any transactions to mine
    if len(client.utx) == 0:
        print("Error: No unverified transactions in pool to mine.")
        return
    # prompt user to select a transaction to mine
    print("Select an unverified transaction from the UTX pool:")
    for i, utx in enumerate(client.utx):
        print("-" * 20)
        print(f"Unverified transaction # {i} \n{json.dumps(utx, indent=1)}")
        print("-" * 20)
    x = input("Enter the number of the transaction -> ")
    try:
        x = int(x)
    except:
        print("Error: Invalid transaction number.")
        return None

    # check if transaction number is valid
    if x < 0 or x >= len(client.utx):
        print("Error: Invalid transaction number.")
        return None
    utx =  client.utx[x]

    # get previous block
    prev = client.blockchain[-1]['id']
    utx['output'].append({
            "value": client.COINBASE,
            "pub_key": vk.to_string().hex()
        })

    # mine transaction
    print("Mining block with ID ", utx['input']['id'])

    # generate nonce until hash is less than difficulty
    nonce = Random.new().read(AES.block_size).hex()
    while int(hashlib.sha256(json.dumps(utx, sort_keys=True).encode('utf8') + prev.encode('utf-8') + nonce.encode('utf-8')).hexdigest(), 16) > client.DIFFICULTY:
        nonce = Random.new().read(AES.block_size).hex()
    pow = hashlib.sha256(json.dumps(utx, sort_keys=True).encode(
        'utf8') + prev.encode('utf-8') + nonce.encode('utf-8')).hexdigest()

    # create block
    block = {
        "type": client.BLOCK,
        "id": hashlib.sha256(json.dumps(client.utx, sort_keys=True).encode('utf8')).hexdigest(),
        "nonce": nonce,
        "pow": pow,
        "prev": prev,
        "tx": client.utx
    }
    print("Transaction successfully mined")
    client.send_to_nodes(block)


def main():

    if len(sys.argv) < 3:
        print("Usage: python3", sys.argv[0], "CLIENTNAME PORT")
        quit()

    # Load keys, or create them if they do not yet exist
    keypath = './' + sys.argv[1] + '.key'
    if not os.path.exists(keypath):
        sk = SigningKey.generate()
        vk = sk.verifying_key
        with open(keypath, 'w') as f:
            f.write(sk.to_string().hex())
            f.close()
    else:
        with open(keypath) as f:
            try:
                sk = SigningKey.from_string(bytes.fromhex(f.read()))
                vk = sk.verifying_key
            except Exception as e:
                print("Couldn't read key file", e)

    # Create a client object
    client = ZachCoinClient("127.0.0.1", int(sys.argv[2]), sys.argv[1])
    client.debug = False

    time.sleep(1)

    client.start()

    time.sleep(1)

    # Connect to server 
    client.connect_with_node(SERVER_ADDR, SERVER_PORT)
    print("Starting ZachCoin™ Client:", sys.argv[1])
    time.sleep(2)

    # Command menu
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        slogan = " You can't spell \"It's a Ponzi scheme!\" without \"ZachCoin\" "
        print("=" * (int(len(slogan)/2) - int(len(' ZachCoin™')/2)), 'ZachCoin™', "=" * (int(len(slogan)/2) - int(len('ZachCoin™ ')/2)))
        print(slogan)
        print("=" * len(slogan),'\n')
        x = input("""
        0: Print keys
        1: Print blockchain
        2: Print UTX pool
        3: Create transaction
        4: Mine transaction
        
        9: Quit

        Enter your choice -> """)
        try:
            x = int(x)
        except:
            print("Error: Invalid menu option.")
            input()
            continue
        if x == 0:
            print("sk: ", sk.to_string().hex())
            print("vk: ", vk.to_string().hex())
        elif x == 1:
            for i, block in enumerate(client.blockchain):
                print(f"Block #{i+1}:")
                print(json.dumps(block, indent=1))
                print("-" * 20)
        elif x == 2:
            print(json.dumps(client.utx, indent=1))
        elif x == 3:
            create_transaction(client, sk, vk)
        elif x == 4:
            mine_transaction(client, vk)
        # quit
        elif x == 9:
            client.stop()
            break

        input()
        
if __name__ == "__main__":
    main()