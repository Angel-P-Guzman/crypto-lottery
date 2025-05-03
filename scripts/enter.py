from brownie import Lottery, accounts, network 

def main():
    acct = accounts[1]
    lottery = Lottery[-1]  # get the most recent deployment
    tx = lottery.enter({"from": acct, "value": "0.01 ether"})
    tx.wait(1)
    print("Entered lottery!")
