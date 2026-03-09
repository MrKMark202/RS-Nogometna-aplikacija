// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FootballerRegistry {
    struct Player {
        string name;
        string clubId;
        uint256 birthDate;
        bool exists;
    }

    struct TransferContract {

        string fromClub;
        string toClub;
        uint256 timestamp;
        string txHash;
        uint256 amount;
    }

    mapping(uint256 => Player) public players;
    mapping(uint256 => TransferContract[]) public playerContracts;
    uint256 public nextPlayerId;

    event PlayerRegistered(uint256 indexed playerId, string name, string clubId);
    event PlayerTransferred(uint256 indexed playerId, string oldClubId, string newClubId, string txHash);

    function registerPlayer(string memory _name, string memory _clubId, uint256 _birthDate, uint256 _initialValue) public returns (uint256) {
        uint256 playerId = nextPlayerId++;
        players[playerId] = Player(_name, _clubId, _birthDate, true);
        
        // Record the initial signing as the first "contract"
        playerContracts[playerId].push(TransferContract(
            "INITIAL_SIGNING", // No previous club
            _clubId,
            block.timestamp,
            "GENESIS_TX",
            _initialValue
        ));

        emit PlayerRegistered(playerId, _name, _clubId);
        return playerId;
    }


    function transferPlayer(uint256 _playerId, string memory _newClubId, string memory _txHash, uint256 _amount) public {
        require(players[_playerId].exists, "Player does not exist");
        
        string memory oldClubId = players[_playerId].clubId;
        players[_playerId].clubId = _newClubId;

        playerContracts[_playerId].push(TransferContract(
            oldClubId,
            _newClubId,
            block.timestamp,
            _txHash,
            _amount
        ));
        
        emit PlayerTransferred(_playerId, oldClubId, _newClubId, _txHash);
    }

    function getPlayer(uint256 _playerId) public view returns (string memory name, string memory clubId, uint256 birthDate) {
        require(players[_playerId].exists, "Player does not exist");
        Player storage p = players[_playerId];
        return (p.name, p.clubId, p.birthDate);
    }

    function getPlayerContracts(uint256 _playerId) public view returns (TransferContract[] memory) {
        return playerContracts[_playerId];
    }
}

