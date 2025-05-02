from brownie import Lottery, accounts

def main():
    acct = accounts[0]
    lottery = Lottery.deploy({"from": acct})
    print(f"Contract deployed to {lottery.address}")
