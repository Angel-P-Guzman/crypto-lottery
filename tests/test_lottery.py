import pytest
from brownie import Lottery, accounts, network, exceptions, web3
from brownie import Wei

# Fixture to deploy the contract
@pytest.fixture
def lottery():
    acct = accounts[0]
    contract = Lottery.deploy({"from": acct})
    return contract

def test_contract_deploys(lottery):
    assert lottery.manager() == accounts[0]

def test_can_enter_lottery(lottery):
    tx = lottery.enter({"from": accounts[1], "value": Wei("0.01 ether")})
    tx.wait(1)
    assert lottery.players(0) == accounts[1]

def test_rejects_insufficient_eth(lottery):
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": accounts[2], "value": Wei("0.001 ether")})

def test_only_manager_can_pick_winner(lottery):
    lottery.enter({"from": accounts[1], "value": Wei("0.01 ether")})
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.pickWinner({"from": accounts[1]})

def test_winner_receives_funds(lottery):
    player1 = accounts[1]
    player2 = accounts[2]
    player3 = accounts[3]

    lottery.enter({"from": player1, "value": Wei("1 ether")})
    lottery.enter({"from": player2, "value": Wei("1 ether")})
    lottery.enter({"from": player3, "value": Wei("1 ether")})

    starting_balance = player1.balance() + player2.balance() + player3.balance()

    tx = lottery.pickWinner({"from": accounts[0]})
    tx.wait(1)
    
    assert len(lottery.getPlayers()) == 0
    
    
