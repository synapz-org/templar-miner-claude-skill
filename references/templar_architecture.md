# Templar System Architecture

Reference documentation for the Templar codebase structure and key components.

## Repository Structure

**GitHub**: https://github.com/one-covenant/templar

### Core Neuron Implementations

**neurons/miner.py** (985 lines)
- Main miner node implementation
- Window-based training loop (lines 354-942)
- Inner steps for gradient accumulation (lines 498-563)
- Gradient compression and upload (lines 568-673)
- Peer gradient gathering (lines 705-726)
- Outer model updates (lines 746-768)
- Memory management and cleanup (lines 943-975)

**neurons/validator.py** (~3400 lines)
- Validator node implementation
- Miner evaluation loop (lines 1056-2900+)
- Loss-based scoring (lines 1644-1940)
- Weight computation and blockchain updates (lines 2050-2150)
- Synchronization tracking (lines 2965-3030)

**neurons/trainer.py** (1200+ lines)
- Shared training logic for both miners and validators
- Inner steps implementation (lines 655-900)
- Optimizer configuration (lines 180-320)

### Core Library (src/tplr/)

**neurons.py** (1000+ lines)
- `prepare_gradient_dict()` (lines 47-222): Gradient compression pipeline
  - DTensor synchronization
  - Momentum update with error feedback
  - DCT transform and top-k compression
  - Async GPU↔CPU transfers
- `outer_step()` (lines 226-450+): Apply gathered peer gradients

**compress.py** (~1500 lines)
- `ChunkingTransformer`: DCT-based gradient transformation
- `TopKCompressor`: Top-k selection with 12-bit index packing (lines 51-142)
- Quantization/dequantization (4-bit default)

**comms.py** (~1200 lines)
- R2 bucket interface for gradient storage
- `put()`: Upload compressed gradients
- `gather_with_reserve()`: Download peer gradients with fallback
- Three bucket types: gradients, aggregator, dataset

**chain.py** (~400 lines)
- `ChainManager`: Bittensor blockchain integration
- Metagraph synchronization
- Weight setting interface

**metrics.py** (369 lines)
- `MetricsLogger`: InfluxDB integration
- Time-series metrics storage
- WandB integration via wandb_ops.py

**dataset.py**
- Sharded dataset management
- Deterministic UID-based data assignment
- Dataset rotation every 455 outer steps

## Key Configuration Parameters

**hparams/hparams.json** - Main production config for 70B Gemma-3:

```json
{
  "model_size": "70B",
  "tokenizer_name": "google/gemma-3-270m",
  "sequence_length": 2048,
  "spec_version": 5,

  "micro_batch_size": 1,
  "batch_size": 192,
  "target_batch_size": 1024,
  "inner_steps": 30,

  "topk_compression": 64,
  "target_chunk": 64,
  "use_dct": false,
  "quantization_bins": 4,

  "outer_learning_rate": 0.7,
  "momentum_decay": 0.95,
  "weight_decay": 0.1,

  "blocks_per_window": 115,
  "outer_steps_per_shard": 455,
  "validator_offset": 1,

  "gather_peer_count": 20,
  "gather_share": 0.75,
  "gather_top_ratio": 2.0,
  "reserve_peer_count": 10,

  "optimizer": {
    "type": "adamw",
    "adamw": {
      "learning_rate": 1.17e-4,
      "weight_decay": 0.1,
      "betas": [0.9, 0.95],
      "eps": 1e-8,
      "scheduler": {
        "warmup_steps": 1500,
        "t_max": 140000,
        "eta_min_factor": 0.1
      }
    }
  },

  "torchtitan": {
    "tp_degree": 1,
    "pp_degree": 1,
    "dp_shard": 8,
    "mixed_precision_param": "bfloat16",
    "mixed_precision_reduce": "float32"
  }
}
```

**Alternative configs**:
- `hparams/150M.json`: Small model for testing
- `hparams/1B.json`: Medium model
- `hparams/hparams-local-run.json`: Local development config

## Documentation References

- **Miner Setup**: docs/miner.md
- **Validator Setup**: docs/validator.md
- **Dataset Preparation**: docs/shared_sharded_dataset.md
- **Performance Profiling**: docs/profilers.md
