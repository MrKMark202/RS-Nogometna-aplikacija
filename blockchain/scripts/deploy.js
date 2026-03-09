const hre = require("hardhat");

async function main() {
  const FootballerRegistry = await hre.ethers.getContractFactory("FootballerRegistry");
  const registry = await FootballerRegistry.deploy();

  await registry.deployed();

  console.log("FootballerRegistry deployed to:", registry.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
