let { networkConfig, getNetworkIdFromName } = require('../helper-hardhat-config')
const fs = require('fs')

const max = 8
const part = 2

module.exports = async ({
  getNamedAccounts,
  deployments,
  getChainId
}) => {
  const { log } = deployments
  const chainId = await getChainId()
  const networkName = networkConfig[chainId]['name']

  const IPFS_JSON = ''

  let proxyRegistryAddress = "";

  if (networkName === 'rinkeby') {
    proxyRegistryAddress = "0xf57b2c51ded3a29e6891aba85459d600256cf317";
  } else {
    proxyRegistryAddress = "0xa5409ec958c83c3f309868babaca7c86dcb077c1";
  }

  log("----------------------------------------------------")

  const args = ["Freaky Goblins", "GOBLIN", `ipfs://${IPFS_JSON}/`, proxyRegistryAddress]

  const FreakyGoblins = await ethers.getContractFactory('FreakyGoblins');
  
  log('Deploying FreakyGoblins...');
  
  const freakyGoblins = await FreakyGoblins.deploy(...args);
  await freakyGoblins.deployed();

  log('FreakyGoblins deployed to:', freakyGoblins.address);
  log(`Use "npx hardhat verify --network ${networkName} ${freakyGoblins.address} ${args.join(" ")}" to verify your contract \n`)

  const contract = await FreakyGoblins.attach(
    freakyGoblins.address
  );

  for (j = 0; j < Math.ceil(max / part); j++) {
    const tx = await contract.mint((j === Math.ceil(max / part) - 1) ? max % part - 1 : part)
    await tx.wait(1)
    console.log(`Minted part ${j + 1} of ${Math.ceil(max / part)}`);
  }
}

module.exports.tags = ['all', 'goblin']
