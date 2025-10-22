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

The skill helps you understand and meet these Templar miner requirements:

- **Minimum**: 1x H100 GPU (80GB VRAM)
- **Recommended**: 2-4x H100 or H200 GPUs
- **CPU**: 32+ cores
- **RAM**: 256+ GB
- **Storage**: 500GB+ SSD
- **Network**: 1Gbps+ bandwidth

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
