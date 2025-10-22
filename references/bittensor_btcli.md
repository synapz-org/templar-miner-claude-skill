# Bittensor btcli Commands Reference

Complete reference for managing Bittensor wallets and subnet operations using btcli.

## Wallet Creation

### Create New Wallet

```bash
# Create complete wallet (coldkey + hotkey)
btcli wallet create

# Create coldkey only (holds TAO, main wallet)
btcli wallet new-coldkey --wallet.name default --n-words 12

# Create hotkey only (for subnet participation)
btcli wallet new-hotkey --wallet.name default --wallet.hotkey miner --n-words 12
```

**Important**:
- Coldkey holds TAO and controls funds
- Hotkey is used for subnet registration and mining
- Save mnemonic phrases securely (12 or 24 words)

## Wallet Recovery

### Regenerate from Mnemonic

```bash
# Restore coldkey from mnemonic
btcli wallet regen-coldkey --wallet.name default --mnemonic "your 12 words here"

# Restore hotkey from mnemonic
btcli wallet regen-hotkey --wallet.name default --wallet.hotkey miner --mnemonic "your 12 words here"

# Restore coldkey from seed or JSON
btcli wallet regen-coldkey --wallet.name default

# Restore hotkey from existing credentials
btcli wallet regen-hotkey --wallet.name default --wallet.hotkey miner
```

### Public Key Recovery (Machine Transfers)

```bash
# Recover coldkey public component when moving machines
btcli wallet regen-coldkeypub --wallet.name default

# Recover hotkey public component for machine transfers
btcli wallet regen-hotkeypub --wallet.name default --wallet.hotkey miner
```

## Wallet Information

### Check Balances

```bash
# Display free and staked TAO balances
btcli wallet balance --wallet.name default

# Check balance for specific network
btcli wallet balance --wallet.name default --subtensor.network finney
```

### Wallet Overview

```bash
# Detailed overview of registered accounts
btcli wallet overview --wallet.name default

# Overview for specific subnet
btcli wallet overview --wallet.name default --netuid 3

# Overview for specific network
btcli wallet overview --wallet.name default --subtensor.network finney
```

### List Wallets

```bash
# View all wallets with associated hotkeys (hierarchical format)
btcli wallet list
```

## Hotkey Management

### Associate Hotkey

```bash
# Associate a hotkey with a wallet (coldkey)
btcli wallet associate-hotkey --wallet.name default --wallet.hotkey miner
```

### Swap Hotkey

```bash
# Exchange hotkey while maintaining registration on same coldkey
btcli wallet swap-hotkey \
  --wallet.name default \
  --wallet.hotkey old_miner \
  --new-hotkey new_miner
```

**Use case**: Replace compromised hotkey without losing subnet registration.

### Swap Coldkey

```bash
# Schedule a coldkey swap for a wallet
btcli wallet swap-coldkey \
  --wallet.name default \
  --new-coldkey new_wallet

# Check status of scheduled coldkey swaps
btcli wallet swap-check --wallet.name default
```

## Transactions

### Transfer TAO

```bash
# Send TAO tokens from one wallet to another
btcli wallet transfer \
  --wallet.name default \
  --dest <SS58_ADDRESS> \
  --amount <TAO_AMOUNT>

# Example: Transfer 10 TAO
btcli wallet transfer \
  --wallet.name default \
  --dest 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKv3gB \
  --amount 10
```

## Identity Management

### Get Identity

```bash
# Retrieve on-chain identity details
btcli wallet get-identity --wallet.name default

# Get identity for specific key
btcli wallet get-identity --key <SS58_ADDRESS>
```

### Set Identity

```bash
# Create or update on-chain identity (1 TAO fee)
btcli wallet set-identity \
  --wallet.name default \
  --display "Display Name" \
  --legal "Legal Name" \
  --web "https://example.com" \
  --email "contact@example.com" \
  --twitter "@handle"
```

**Cost**: 1 TAO fee for setting identity.

## Authentication

### Sign Message

```bash
# Generate cryptographic signature proving key ownership
btcli wallet sign \
  --wallet.name default \
  --wallet.hotkey miner \
  --message "Message to sign"
```

### Verify Signature

```bash
# Confirm message signatures using public keys or SS58 addresses
btcli wallet verify \
  --message "Message to verify" \
  --signature <SIGNATURE> \
  --address <SS58_ADDRESS>
```

## Subnet Operations

### Register to Subnet

```bash
# Register hotkey to subnet (required before mining/validating)
btcli subnet register \
  --wallet.name default \
  --wallet.hotkey miner \
  --netuid 3 \
  --subtensor.network finney

# For Templar (Subnet 3, netuid 3)
btcli subnet register \
  --wallet.name default \
  --wallet.hotkey miner \
  --netuid 3 \
  --subtensor.network finney
```

**Cost**: Registration requires payment or proof-of-work.
**Networks**:
- `finney`: Mainnet
- `test`: Testnet
- `local`: Local development

### Check Registration

```bash
# Verify hotkey is registered to subnet
btcli wallet overview --wallet.name default --netuid 3
```

## Common Templar Wallet Setup

Complete setup sequence for Templar miners:

```bash
# Step 1: Create coldkey
btcli wallet new-coldkey --wallet.name default --n-words 12

# Step 2: Create hotkey for miner
btcli wallet new-hotkey --wallet.name default --wallet.hotkey miner --n-words 12

# Step 3: Fund coldkey with TAO (acquire from exchange)
# (Transfer TAO to coldkey address shown in wallet balance command)

# Step 4: Register to Templar subnet (netuid 3)
btcli subnet register \
  --wallet.name default \
  --wallet.hotkey miner \
  --netuid 3 \
  --subtensor.network finney

# Step 5: Verify registration
btcli wallet overview --wallet.name default --netuid 3

# Step 6: Check balance
btcli wallet balance --wallet.name default
```

## Environment Variables

btcli can use environment variables for common parameters:

```bash
export WALLET_NAME=default
export WALLET_HOTKEY=miner
export NETWORK=finney
export NETUID=3

# Then commands can be shorter:
btcli wallet balance
btcli wallet overview
```

## Network Options

**Finney (Mainnet)**:
```bash
--subtensor.network finney
```

**Test (Testnet)**:
```bash
--subtensor.network test
```

**Local (Development)**:
```bash
--subtensor.network local
--subtensor.chain_endpoint ws://127.0.0.1:9946
```

## Wallet File Locations

Default wallet storage:
```
~/.bittensor/wallets/
├── default/               # Wallet name
│   ├── coldkey           # Encrypted coldkey
│   ├── coldkeypub.txt    # Public coldkey
│   └── hotkeys/
│       ├── miner         # Encrypted hotkey
│       └── miner.pub     # Public hotkey
```

## Security Best Practices

1. **Backup mnemonics**: Store 12/24-word phrases securely offline
2. **Separate coldkey/hotkey**: Coldkey holds funds, hotkey participates in subnet
3. **Encrypt coldkey**: Keep coldkey on secure, offline machine if possible
4. **Use hotkeys for mining**: Compromised hotkey doesn't expose TAO holdings
5. **Regular backups**: Back up wallet directory before operations
6. **Verify addresses**: Double-check recipient addresses before transfers
7. **Test on testnet**: Practice operations on testnet before mainnet

## Troubleshooting

**"Insufficient funds" error**:
- Check balance: `btcli wallet balance`
- Ensure coldkey has enough TAO for registration fees

**"Already registered" error**:
- Check current registration: `btcli wallet overview --netuid 3`
- May need to deregister first or use different hotkey

**"Connection refused" error**:
- Verify network connectivity
- Check subtensor.network parameter (finney/test/local)
- Try different subtensor endpoint

**"Wallet not found" error**:
- Verify wallet name spelling
- Check wallet exists: `btcli wallet list`
- Ensure wallet files in ~/.bittensor/wallets/
