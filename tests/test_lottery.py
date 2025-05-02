import pytest
from brownie import Lottery, accounts, network, exceptions, web3

# Fixture to deploy the contract
@pytest.fixture
def lottery():
    acct = accounts[0]
    contract = Lottery.deploy({"from": acct})
    return contract

def test_contract_deploys(lottery):
    assert lottery.manager() == accounts[0]

def test_can_enter_lottery(lottery):
    tx = lottery.enter({"from": accounts[1], "value": web3.toWei(0.01, "ether")})
    tx.wait(1)
    assert lottery.players(0) == accounts[1]

def test_rejects_insufficient_eth(lottery):
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": accounts[2], "value": web3.toWei(0.001, "ether")})

def test_only_manager_can_pick_winner(lottery):
    lottery.enter({"from": accounts[1], "value": web3.toWei(0.01, "ether")})
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.pickWinner({"from": accounts[1]})

def test_winner_receives_funds(lottery):
    player = accounts[1]
    lottery.enter({"from": player, "value": web3.toWei(1, "ether")})
    starting_balance = player.balance()
    tx = lottery.pickWinner({"from": accounts[0]})
    tx.wait(1)
    ending_balance = player.balance()
    assert ending_balance > starting_balance
    assert len(lottery.getPlayers()) == 0
