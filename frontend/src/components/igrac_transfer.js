import { ethers } from "ethers";
import axios from "axios";
import { Auth } from "@/components/registracija";

// Blockchain Configuration
const CONTRACT_ADDRESS = process.env.VUE_APP_CONTRACT_ADDRESS || "0x5FbDB2315678afecb367f032d93F642f64180aa3";
const ABI = [
    "function registerPlayer(string name, string clubId, uint256 birthDate, uint256 initialValue) public returns (uint256)",
    "function transferPlayer(uint256 playerId, string newClubId, string txHash, uint256 amount) public",
    "function getPlayerContracts(uint256 playerId) public view returns (tuple(string fromClub, string toClub, uint256 timestamp, string txHash, uint256 amount)[])",
    "event PlayerRegistered(uint256 indexed playerId, string name, string clubId)",
    "event PlayerTransferred(uint256 indexed playerId, string oldClubId, string newClubId, string txHash)"
];



const FootballerService = axios.create({
    baseURL: process.env.VUE_APP_FOOTBALLER_API || "http://localhost:8006",
    timeout: 5000,
});

const TransferService = axios.create({
    baseURL: process.env.VUE_APP_TRANSFER_API || "http://localhost:8007",
    timeout: 5000,
});


[FootballerService, TransferService].forEach(service => {
    service.interceptors.request.use((config) => {
        const token = Auth.getToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    });
});

const BlockchainService = {
    async ensureCorrectNetwork() {
        const network = await window.ethereum.request({ method: 'eth_chainId' });
        // 31337 is 0x7a69 in hex
        if (network !== '0x7a69' && network !== '31337') {
            try {
                await window.ethereum.request({
                    method: 'wallet_switchEthereumChain',
                    params: [{ chainId: '0x7a69' }],
                });
            } catch (err) {
                // This error code indicates that the chain has not been added to MetaMask.
                if (err.code === 4902) {
                    await window.ethereum.request({
                        method: 'wallet_addEthereumChain',
                        params: [{
                            chainId: '0x7a69',
                            chainName: 'Hardhat Local',
                            nativeCurrency: { name: 'ETH', symbol: 'ETH', decimals: 18 },
                            rpcUrls: ['http://localhost:8545'],
                        }],
                    });
                } else {
                    throw err;
                }
            }
        }
    },

    async getProvider() {
        if (!window.ethereum) {
            throw new Error("MetaMask is not installed");
        }
        // Force correct network
        await this.ensureCorrectNetwork();
        // Force account connection
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        return new ethers.providers.Web3Provider(window.ethereum);
    },


    async getContract() {
        const provider = await this.getProvider();
        const signer = provider.getSigner();
        return new ethers.Contract(CONTRACT_ADDRESS, ABI, signer);
    },

    async registerPlayer(name, clubId, birthDate, slikaIgraca, initialValue = 0, drzavljanstvo = "Nepoznato") {
        try {
            const contract = await this.getContract();
            const tx = await contract.registerPlayer(
                name, 
                clubId, 
                Math.floor(new Date(birthDate).getTime() / 1000),
                initialValue
            );
            const receipt = await tx.wait();
            
            // Get Player ID from events
            const event = receipt.events.find(e => e.event === 'PlayerRegistered');
            const blockchainPlayerId = event.args.playerId.toNumber();

            const res = await FootballerService.post("/api/footballer/create", {
                ime: name,
                datumRodjenja: birthDate,
                drzavljanstvo: drzavljanstvo,
                slikaIgraca: slikaIgraca,
                klub: clubId,
                korisnikEmail: Auth.state.userEmail,
                blockchainPlayerId: blockchainPlayerId,
                initialValue: initialValue
            });
            
            alert("Igrač uspješno kreiran na blockchainu i u bazi! ✅");
            return res.data;
        } catch (err) {
            console.error("registerPlayer error:", err);
            alert("Greška pri kreiranju igrača: " + (err.reason || err.message));
            throw err;
        }
    },


    async transferPlayer(playerId, currentClubId, newClubId, blockchainPlayerId, value = 0) {
        try {
            const contract = await this.getContract();
            // We pass "PENDING" or similar, the real hash is added to backend after wait()
            const tx = await contract.transferPlayer(blockchainPlayerId, newClubId, "PENDING", value);
            const receipt = await tx.wait();
            
            await TransferService.post("/api/transfer/record", {
                igracId: playerId,
                stariKlubId: currentClubId,
                noviKlubId: newClubId,
                datumTransfera: new Date().toISOString().split('T')[0],
                korisnikEmail: Auth.state.userEmail,
                transakcijaHash: receipt.transactionHash,
                vrijednost: value
            });
            
            alert("Transfer uspješno obavljen! 💸");
            return receipt.transactionHash;
        } catch (err) {
            console.error("transferPlayer error:", err);
            alert("Greška pri transferu: " + (err.reason || err.message));
            throw err;
        }
    },

    async getPlayerContracts(blockchainPlayerId) {
        try {
            console.log("BlockchainService: Dohvaćam ugovore za ID:", blockchainPlayerId);
            const contract = await this.getContract();
            const contracts = await contract.getPlayerContracts(blockchainPlayerId);
            console.log("BlockchainService: Sirov odgovor:", contracts);
            
            return contracts.map((c, index) => {
                console.log(`Processing contract ${index}:`, c);
                // Logging raw values to help debugging if names are missing
                console.log(`Raw [0]: ${c[0]}, [1]: ${c[1]}, [2]: ${c[2]}, [3]: ${c[3]}, [4]: ${c[4]}`);
                
                return {
                    fromClub: c.fromClub || c[0],
                    toClub: c.toClub || c[1],
                    timestamp: c.timestamp ? new Date(c.timestamp.toNumber() * 1000).toLocaleString() : "Nepoznato",
                    txHash: c.txHash || c[3],
                    value: c.amount ? c.amount.toNumber() : (c[4] && typeof c[4].toNumber === 'function' ? c[4].toNumber() : 0)
                };
            });
        } catch (err) {
            console.error("BlockchainService error:", err);
            return [];
        }
    },


    async getDatabaseContracts(igracId) {
        try {
            console.log("BlockchainService: Dohvaćam ugovore iz baze za ID:", igracId);
            const res = await TransferService.get(`/api/transfer/contracts/${igracId}`);
            console.log("BlockchainService: Odgovor iz baze:", res.data);
            
            return res.data.map(c => ({
                fromClub: c.izKluba || (c.tip === 'INITIAL_SIGNING' ? 'INITIAL_SIGNING' : c.klubId),
                toClub: c.uKlub || c.klubId,
                timestamp: c.datum,
                value: c.vrijednost || 0,
                tip: c.tip
            }));
        } catch (err) {
            console.error("BlockchainService: Greška pri dohvaćanju ugovora iz baze:", err);
            return [];
        }
    }
};

export default BlockchainService;
