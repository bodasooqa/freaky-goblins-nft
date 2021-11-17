/**
 * This script is used during development in order to unpin your files from Pinata.
 */

const axios = require('axios');

const hashes = require('./data/hashes_to_unpin.json');

if (!!hashes && hashes.length) {
    hashes.forEach(hash => {
        const url = `https://api.pinata.cloud/pinning/unpin/${hash}`;
        axios.delete(url, {
            headers: {
                pinata_api_key: process.env.PINATA_API_KEY,
                pinata_secret_api_key: process.env.PINATA_API_SECRET,
            }
        })
            .then(() => {
                console.log(`Hash ${hash} successfully deleted`);
            })
            .catch(() => {
                console.log(`Can't find hash ${hash}`);
            });
    });
} else {
    console.log('No hashes :(');
}
