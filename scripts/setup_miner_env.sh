#!/usr/bin/env bash
# Templar Miner Environment Setup Script
#
# This script helps set up the environment for running a Templar miner.
# It creates a template .env file with all required variables.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${1:-.env}"

echo "=========================================="
echo "Templar Miner Environment Setup"
echo "=========================================="
echo

if [ -f "$ENV_FILE" ]; then
    read -p "⚠️  $ENV_FILE already exists. Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

cat > "$ENV_FILE" << 'EOF'
# Templar Miner Environment Configuration
# Fill in all values before running the miner

# Hugging Face
HF_TOKEN=your_huggingface_token_here

# Weights & Biases (optional but recommended for monitoring)
WANDB_API_KEY=your_wandb_api_key_here
WANDB_PROJECT=templar
WANDB_ENTITY=your_wandb_entity_here

# InfluxDB Metrics (optional but recommended for monitoring)
INFLUXDB_TOKEN=your_influxdb_token_here

# R2 Gradient Bucket (your miner's storage)
R2_GRADIENTS_ACCOUNT_ID=your_cloudflare_account_id
R2_GRADIENTS_BUCKET_NAME=your_gradient_bucket_name
R2_GRADIENTS_READ_ACCESS_KEY_ID=your_read_access_key_id
R2_GRADIENTS_READ_SECRET_ACCESS_KEY=your_read_secret_key
R2_GRADIENTS_WRITE_ACCESS_KEY_ID=your_write_access_key_id
R2_GRADIENTS_WRITE_SECRET_ACCESS_KEY=your_write_secret_key

# R2 Dataset Bucket (shared training data)
R2_DATASET_ACCOUNT_ID=templar_dataset_account_id
R2_DATASET_BUCKET_NAME=templar_dataset_bucket_name
R2_DATASET_READ_ACCESS_KEY_ID=dataset_read_access_key_id
R2_DATASET_READ_SECRET_ACCESS_KEY=dataset_read_secret_key
DATASET_BINS_PATH=tokenized/

# Bittensor Wallet
WALLET_NAME=default
WALLET_HOTKEY=miner
NETWORK=finney
NETUID=3

# Optional: Custom subtensor endpoint
# SUBTENSOR_ENDPOINT=wss://entrypoint-finney.opentensor.ai:443

# Optional: Logging level
# LOG_LEVEL=INFO
EOF

echo "✅ Created environment file: $ENV_FILE"
echo
echo "Next steps:"
echo "1. Edit $ENV_FILE and fill in all required values"
echo "2. Obtain R2 bucket credentials from Cloudflare"
echo "3. Contact Templar team for dataset bucket access credentials"
echo "4. Create and register your Bittensor wallet:"
echo "   btcli wallet new-coldkey --wallet.name default"
echo "   btcli wallet new-hotkey --wallet.name default --wallet.hotkey miner"
echo "   btcli subnet register --wallet.name default --wallet.hotkey miner --netuid 3"
echo "5. Source the environment: source $ENV_FILE"
echo "6. Run health check: python scripts/check_miner_health.py"
echo "7. Start the miner: python neurons/miner.py"
echo
echo "=========================================="
