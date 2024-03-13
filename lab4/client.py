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
                #TODO: Validate blocks

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


def get_input_block(client: ZachCoinClient):
    """
    Get the input block for a new transaction
    """
    # user picks block from blockchain
    print("\nChoose a block from the blockchain to use as input:")
    print("\n" + "-" * 20)
    for i, block in enumerate(client.blockchain):
        print(f"Block {i}:")
        print("-" * 20)
        print(json.dumps(block, indent=4))
        print("-" * 20)
    x = input("Which block would you like to use? Enter the corresponding number -> ")
    try:
        x = int(x)
        
        # verify that the block exists
        if x < 0 or x >= len(client.blockchain):
            print("Error: Invalid block number.")
            return None
    except:
        print("Error: Invalid block number.")
        return None
    
    block = client.blockchain[x]
    
    # user picks transaction output from block
    print("\nChoose a transaction output from the block to use as input:")
    for i, tx in enumerate(block["tx"]["output"]):
        print(f"Output {i}:")
        print("-" * 20)
        print(json.dumps(tx, indent=4))
        print("-" * 20)
    n = input("Which output would you like to use? Enter the corresponding number -> ")
    try:
        n = int(n)
        
        # verify that the output exists
        if n < 0 or n >= len(block["tx"]["output"]):
            print("Error: Invalid output number.")
            return None
    except:
        print("Error: Invalid output number.")
        return None
    
    return {
        "id": block["id"],
        "n": n
    }
    
    
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
            return None, None
    except:
        print("Error: Invalid amount.")
        return None, None
    return recipient, amount


def create_transaction(client: ZachCoinClient, sk: SigningKey):
    """
    Create a transaction and add it to the unverified transaction pool
    """
    # get input block
    input_info = get_input_block(client)
    input_id = input_info["id"]
    input_n = input_info["n"]
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





def mine_transaction(client: ZachCoinClient, vk: VerifyingKey):
    # check if there are any transactions to mine
    if len(client.utx) == 0:
        print("Error: No unverified transactions in pool to mine.")
        return
    # prompt user to select a transaction to mine
    print("Select an unverified transaction from the UTX pool:")
    for i, utx in enumerate(client.utx):
        print(f"-------- {i} --------\n{json.dumps(utx, indent=1)}")
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
    client.utx['output'].append({
            "value": client.COINBASE,
            "pub_key": vk.to_string().hex()
        })

    # mine transaction
    print("Mining transaction...")
    # generate nonce until hash is less than difficulty
    nonce = Random.new().read(AES.block_size).hex()
    while int(hashlib.sha256(json.dumps(client.utx, sort_keys=True).encode('utf8') + prev.encode('utf-8') + nonce.encode('utf-8')).hexdigest(), 16) > client.DIFFICULTY:
        nonce = Random.new().read(AES.block_size).hex()
    pow = hashlib.sha256(json.dumps(client.utx, sort_keys=True).encode(
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
    print("Transaction successfully mined:", json.dumps(block, indent=1))
    client.sent_to_nodes(block)


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
            print(json.dumps(client.blockchain, indent=1))
        elif x == 2:
            print(json.dumps(client.utx, indent=1))
        # TODO: Add options for creating and mining transactions
        # as well as any other additional features
        
        # create transaction
        elif x == 3:
            create_transaction(client, sk)
        # mine transaction
        elif x == 4:
            mine_transaction(client, vk)
        # quit
        elif x == 9:
            client.stop()
            break

        input()
        
if __name__ == "__main__":
    main()