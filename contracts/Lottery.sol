// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Lottery {
    address public manager;
    address[] public players;

    constructor() {
        manager = msg.sender;
    }

    function enter() public payable {
        require(msg.value >= 0.01 ether, "Minimum 0.01 ETH required");
        players.push(msg.sender);
    }

    function getPlayers() public view returns (address[] memory) {
        return players;
    }

    function pickWinner() public {
        require(msg.sender == manager, "Only manager can pick winner");
        require(players.length >= 3, "Not enough players");

        uint index = random() % players.length;
        address winner = players[index];
        payable(winner).transfer(address(this).balance);
        delete players;
    }

    function random() private view returns (uint) {
        return uint(keccak256(abi.encodePacked(block.difficulty, block.timestamp, players)));
    }
}
