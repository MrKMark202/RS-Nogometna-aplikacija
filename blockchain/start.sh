#!/bin/sh

# Start Hardhat node in the background
npx hardhat node &

# Wait for node to start
sleep 5

# Deploy the contract
npx hardhat run scripts/deploy.js --network localhost

# Keep the container running
wait
