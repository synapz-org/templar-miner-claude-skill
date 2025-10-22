# Templar Miner Claude Skill

A Claude Code skill for expert-level setup, optimization, and management of Templar AI miners on Bittensor Subnet 3 (netuid 3).

## Overview

This skill transforms Claude into a Templar mining expert, providing comprehensive guidance on:

- **Miner Setup & Configuration** - Wallet creation, subnet registration, environment setup
- **Performance Optimization** - Memory management, gradient quality, communication efficiency
- **Monitoring & Metrics** - WandB, Grafana, InfluxDB integration and interpretation
- **Incentive Mechanism** - Understanding validator scoring and reward distribution
- **Troubleshooting** - Common issues and systematic debugging approaches
- **Advanced Strategies** - Techniques for achieving top miner ranking

## Installation

### Install via Claude Code

1. Download `templar-miner-claude-skill.zip` from releases
2. In Claude Code, use the command:
   ```
   /skills install templar-miner-claude-skill.zip
   ```

### Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/synapz-org/templar-miner-claude-skill.git
   cd templar-miner-claude-skill
   ```

2. Copy to your Claude skills directory:
   ```bash
   cp -r . ~/.claude/skills/templar-miner-claude-skill/
   ```

## Usage

Once installed, the skill automatically activates when you ask Claude about Templar mining topics:

- "Help me set up a Templar miner"
- "My miner is getting negative gradient scores, what's wrong?"
- "How do I optimize my gather success rate?"
- "Explain the Templar incentive mechanism"
- "What btcli commands do I need to create a wallet?"

## Skill Contents

### SKILL.md
Main skill document with workflow guidance, quick reference for key concepts, and task execution guidelines.

### scripts/
Executable utilities for miner operations:
- **check_miner_health.py** - Comprehensive health check (environment, GPU, wallet, R2, resources)
- **setup_miner_env.sh** - Generate template .env file with all required variables

### references/
Detailed reference documentation loaded as needed:
- **templar_architecture.md** - Complete codebase structure, file locations, line numbers
- **incentive_mechanism.md** - Detailed scoring formulas, penalties, evaluation process
- **bittensor_btcli.md** - Complete btcli command reference with examples

## Key Features

### Comprehensive Coverage
- Complete Templar codebase knowledge (miners, validators, compression, incentives)
- All btcli wallet management commands
- Hardware requirements and optimization strategies
- Monitoring dashboards and critical alert thresholds

### Actionable Guidance
- Step-by-step setup workflows
- Troubleshooting guides with symptoms and solutions
- Performance benchmarks and target metrics
- Code references with exact file paths and line numbers

### Progressive Disclosure
- Lean SKILL.md for quick reference
- Detailed references loaded only when needed
- Scripts for deterministic operations

## System Requirements

### For Competitive Templar Mining

- **Minimum GPUs**: 8x H200 (141GB VRAM each)
- **CPU**: 64+ cores
- **RAM**: 512+ GB
- **Storage**: 1TB+ NVMe SSD
- **Network**: 10Gbps+ bandwidth

**Note**: Smaller configurations are unlikely to be competitive for rewards in the Templar network.

### GPU Rental Option

Don't have 8x H200 GPUs? Rent them via **Basilica's decentralized compute marketplace**:

- Install the [Basilica CLI Claude Skill](https://github.com/synapz-org/basilica-cli-claude-skill)
- Seamlessly integrates with this Templar skill
- Rent H200 GPUs on-demand with `basilica up h200 --gpu-count 8`
- Claude can coordinate both skills together automatically

See the SKILL.md **GPU Rental via Basilica** section for complete workflows.

## Setup Prerequisites Checklist

Before renting GPUs and launching your Templar miner, complete these prerequisites:

### Critical Requirements (Must Have)

#### 1. Cloudflare R2 Buckets (TWO buckets required)

**A. Your Personal Gradient Bucket**
- [ ] Create Cloudflare account
- [ ] Create R2 bucket for your gradients (e.g., `templar-miner-yourname`)
- [ ] Generate READ API token and save credentials
- [ ] Generate WRITE API token and save credentials
- [ ] Note your Cloudflare Account ID

**B. Templar Shared Dataset Bucket**
- [ ] Join Templar Discord/GitHub community
- [ ] Request dataset bucket access credentials from Templar team
- [ ] Save provided credentials

#### 2. HuggingFace
- [ ] Create account at https://huggingface.co
- [ ] Generate READ access token (Settings → Access Tokens)
- [ ] Accept Gemma-3 model license agreement

#### 3. Bittensor Wallet Registration
- [ ] Choose coldkey/hotkey pair for mining
- [ ] Check registration status: `btcli wallet overview --wallet.name [name] --wallet.hotkey [hotkey] --netuid 3`
- [ ] If not registered, register to Subnet 3:
  ```bash
  btcli subnet register --wallet.name [name] --wallet.hotkey [hotkey] --netuid 3 --subtensor.network finney
  ```

### Highly Recommended

#### 4. Weights & Biases (WandB)
- [ ] Create account at https://wandb.ai
- [ ] Copy API key (User Settings → API Keys)
- [ ] Create project for monitoring (e.g., "templar-mining")

**Benefits**: Real-time loss curves, throughput, gather success rate, GPU monitoring

### Optional

#### 5. InfluxDB (Time-Series Metrics)
- [ ] Request token from Templar team OR set up your own InfluxDB Cloud instance

### Environment Variables Required

Create a `.env` file with all credentials:

```bash
# Hugging Face
HF_TOKEN=your_token_here

# Weights & Biases (optional but recommended)
WANDB_API_KEY=your_key_here
WANDB_PROJECT=templar-mining
WANDB_ENTITY=your_username

# InfluxDB (optional)
INFLUXDB_TOKEN=your_token_here

# R2 Gradient Bucket (YOUR bucket)
R2_GRADIENTS_ACCOUNT_ID=your_account_id
R2_GRADIENTS_BUCKET_NAME=your_bucket_name
R2_GRADIENTS_READ_ACCESS_KEY_ID=your_read_key
R2_GRADIENTS_READ_SECRET_ACCESS_KEY=your_read_secret
R2_GRADIENTS_WRITE_ACCESS_KEY_ID=your_write_key
R2_GRADIENTS_WRITE_SECRET_ACCESS_KEY=your_write_secret

# R2 Dataset Bucket (Templar shared - get from team)
R2_DATASET_ACCOUNT_ID=provided_by_team
R2_DATASET_BUCKET_NAME=provided_by_team
R2_DATASET_READ_ACCESS_KEY_ID=provided_by_team
R2_DATASET_READ_SECRET_ACCESS_KEY=provided_by_team
DATASET_BINS_PATH=tokenized/

# Bittensor Wallet
WALLET_NAME=your_wallet
WALLET_HOTKEY=your_hotkey
NETWORK=finney
NETUID=3
```

### Pre-Flight Verification

Before renting GPUs, verify:
- [ ] All environment variables documented and saved securely
- [ ] R2 buckets created and accessible
- [ ] Dataset bucket credentials obtained from Templar team
- [ ] Bittensor wallet registered to Subnet 3
- [ ] WandB project created (if using)

**Most Important**: Contact the Templar team to get shared dataset bucket credentials - this is the biggest blocker for new miners.

## Resources

- **Templar GitHub**: https://github.com/one-covenant/templar
- **WandB Dashboard**: https://wandb.ai/tplr/templar
- **Grafana Metrics**: https://grafana.tplr.ai/d/ceia6bwlwn8qof/eval-metrics
- **Bittensor Docs**: https://docs.learnbittensor.org
- **DeepWiki**: https://deepwiki.com/one-covenant/templar

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This skill is provided as-is for educational and operational purposes. Please refer to the Templar project's license for information about the underlying codebase.

## Acknowledgments

Built with deep analysis of the [Templar](https://github.com/one-covenant/templar) codebase and designed to help miners achieve top performance in the decentralized training network.
