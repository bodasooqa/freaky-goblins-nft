# Freaky Goblins NFT

This is a repo that shows how to create NFTs with metadata that is 100% on-chain

- [Freaky Goblins NFT](#freaky-goblins-nft)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Quickstart / Deploy](#quickstart--deploy)
- [Create NFT & View on OpenSea](#create-nft--view-on-opensea)
  - [Verify on Etherscan](#verify-on-etherscan)


 ## Requirements

- [NPM](https://www.npmjs.com/) & Node.js

## Installation

![WARNING](https://via.placeholder.com/15/f03c15/000000?text=+) **WARNING** ![WARNING](https://via.placeholder.com/15/f03c15/000000?text=+)

Don't commit and push any changes to .env files that may contain sensitive information, such as a private key! If this information reaches a public GitHub repository, someone can use it to check if you have any Mainnet funds in that wallet address, and steal them!

`.env` example:
```
export RINKEBY_RPC_URL='https://polygon-mumbai.g.alchemy.com/v2/your-address'
export MNEMONIC='your mnemonic phrase here'
export PRIVATE_KEY='your_private_key'
export PUBLIC_KEY='your_public_key'
export ETHERSCAN_API_KEY='your_etherscan_key'
export PINATA_API_KEY=your_pinata_api_key
export PINATA_API_SECRET=your_pinata_api_secret
```

Then you can install all the dependencies

```bash
git clone https://github.com/bodasooqa/freaky-goblins-nft
cd freaky-goblins-nft
```
then

```bash
npm install
```


## Quickstart / Deploy

FIRST OF ALL:

```bash
source .env
```

To begin with, you should put your png in the `trait-layers` directory and specify the correct data in the `utils/main.py` script and run it.

This script will generate the required images and upload them to *Pinata*, and also will generate metadata for your NFTs and put *Pinata* pins in a separate file (`utils/data/hashes_to_unpin.json`) so that they can be quickly unpinned, clearing the *Pinata* space.

### Deployment

This will deploy to a local hardhat network.

```bash
npx hardhat deploy --tags goblin
```

To deploy to testnet:

*You'll need testnet MATIC in your wallet*

```bash
npx hardhat deploy --network mumbai --tags goblin
```

To deploy to Polygon mainnet:

*You'll need MATIC in your Polygon Mainnet wallet*

```bash
npx hardhat deploy --network polygon --tags goblin
```

# Development

To unpin your images from pinata after uploading use:

```bash
node utils/pinata-unpin.js
```

Use the `utils/opensea-polygon-sell-order.scpt` (Apple Script) to set the price for your NFTs on Opensea.

# Create NFT & View on OpenSea

Once deployed, each will look something like this: 

[Freaky Goblins on Testnet](https://testnets.opensea.io/assets/mumbai/0x9342df95959d03c173a80922ef9e2aae427af4cf/0)


## Verify on Etherscan

You'll need an `ETHERSCAN_API_KEY` environment variable. You can get one from the [Etherscan API site.](https://polygonscan.com)

```
npx hardhat verify --network <NETWORK> <CONTRACT> <CONSTRUCTOR_PARAMETERS>
```
example:

```
npx hardhat verify --network polygon "0x0000000000000000" "Freaky Goblins" "GOBLIN" "ipfs://XXXXXXXXXXXXX/" "0x0000000000000000"
```
