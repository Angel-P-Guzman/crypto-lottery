from brownie import Lottery, accounts

def main():
    acct = accounts[0]  # manager
    lottery = Lottery[-1]
    tx = lottery.pickWinner({"from": acct})
    tx.wait(1)
    print(f"Winner picked: {lottery.getPlayers()}")
