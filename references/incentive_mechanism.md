# Templar Incentive Mechanism

Complete reference for how miners are evaluated and rewarded in the Templar network.

## Loss-Based Gradient Evaluation

Validators measure miner contribution quality by computing loss improvement:

```
s_i = L_before - L_after
```

### Evaluation Process

For each miner UID being evaluated, validators:

1. **Load miner's data assignment** - Same deterministic dataset the miner used
2. **Compute L_before** - Loss on assigned data BEFORE applying miner's gradient
3. **Apply miner's gradient** - Decompress and apply to validator's model
4. **Compute L_after** - Loss on same data AFTER applying gradient
5. **Calculate score** - Difference represents miner's contribution

### Score Interpretation

- **Positive s_i**: Miner's gradient improved the model → reward
- **Zero s_i**: No change in model performance → minimal reward
- **Negative s_i**: Miner's gradient worsened the model → penalty

## Moving Average Smoothing

Raw scores are smoothed using exponential moving average:

```
s̄_i = α * s_i + (1 - α) * s̄_i
```

**Parameters** (from hparams.json):
- α = 0.05 (`binary_score_ma_alpha`)
- Provides stability over time
- Prevents gaming via single exceptional gradient
- Historical reputation matters for long-term rewards

## Weight Assignment

Final weights are computed from moving average scores:

```
w_i = s̄_i
```

**Blockchain Update**:
- Validators call `subtensor.set_weights()` to publish weights
- Weights determine TAO reward distribution per block
- Higher weights → more rewards → more stake → better peer selection
- Update frequency: Every 3 windows (`windows_per_weights`)

## Penalty Mechanisms

### 1. Missing Gradient Penalty

**Score**: -99.0 (`missing_gradient_penalty_score`)
**Slash Rate**: 0.25 (25% reduction per window)
**Threshold**: Below 0.00001 sets weight to zero

Applied when miner fails to upload gradient for a window.

### 2. Invalid Gradient Penalty

Applied for:
- Corrupted compressed data
- Malformed tensor formats
- Decompression failures
- Shape mismatches

Tracked via OpenSkill rating system for persistent offenders.

### 3. Consecutive Negative Threshold

**Threshold**: 3 consecutive negative evaluations (`consecutive_negative_threshold`)
**Action**: Miner excluded from peer selection
**Recovery**: Must produce positive gradients to re-enter peer pool
**Config**: `exclude_negative_peers: true`

### 4. Desynchronization Penalty

Tracks how many steps behind miner is from validator's model state.

**Sync Score Formula**:
```
sync_score = max(0, (1 - min(avg_steps_behind, 5) / 5) ^ 2.5)
```

**Calculation** (validator.py lines 2965-3030):
- Compare miner's gradient fingerprint with validator model
- Detect step lag via global_step metadata
- Exponential penalty for being >5 steps behind

**Impact**: Combined with gradient score for final weight.

### 5. Index Overlap Detection

**Threshold**: 0.4 (`idx_overlap_threshold`)
**Detection**: Compare sparse gradient indices between miners
**Purpose**: Prevent gradient plagiarism
**Action**: Flag for investigation, potential exclusion

## Inactivity Slashing

**Slash Rate**: 0.25 (25% per window inactive)
**Reset Window**: 3 (`reset_inactivity_windows`)

Tracks:
- `inactive_scores`: Dict of (uid: (last_active_window, last_score))
- Gradually reduces weights for inactive miners
- Resets upon return to activity

## OpenSkill Rating System

**Model**: PlackettLuce
**Parameters**:
- Beta: 7.0 (`openskill_beta`)
- Tau: 0.1 (`openskill_tau`)

**Purpose**:
- Provides ordinal ranking of miners
- Accounts for peer quality in evaluation
- Tracks mu (mean skill) and sigma (uncertainty) per miner
- Updates after each evaluation window

**Usage** (validator.py lines 3049-3054):
- Ratings updated via `openskill.rate()`
- Ordinal score: `rating.ordinal()`
- Helps with peer selection decisions

## Binary Indicator Scoring

**Binary Score Calculation** (validator.py lines 3039-3064):
- Positive gradient: +1 point
- Negative/zero gradient: -1 point or penalty
- Applies consecutive_negative_threshold logic
- Combined with moving average for stability

## State Tracking

Validators maintain per-UID tracking:

```python
gradient_scores = torch.zeros(256)              # Raw loss improvement
sync_scores = torch.zeros(256)                  # Synchronization metric
binary_indicator_scores = torch.zeros(256)      # +1/-1 binary indicator
binary_moving_averages = torch.zeros(256)       # Smoothed binary scores
final_scores = torch.zeros(256)                 # Combined final score
weights = torch.zeros(256)                      # Weights for blockchain
```

## Formal Guarantees

1. **Alignment Incentive**: Miners maximize rewards by producing gradients that reduce loss
2. **Discouraging Malicious Actions**: Harmful updates receive low/negative scores
3. **Fair Reward Distribution**: Weights based on actual performance contributions
4. **Convergence Assurance**: Aggregating beneficial updates guides model improvement
5. **Sybil Resistance**: Quality-based rewards make fake identities unprofitable

## Key Evaluation Parameters

From `hparams.json`:

```json
{
  "binary_score_ma_alpha": 0.05,
  "moving_average_window": 5,
  "missing_gradient_penalty_score": -99.0,
  "idx_overlap_threshold": 0.4,
  "consecutive_negative_threshold": 3,
  "exclude_negative_peers": true,
  "openskill_beta": 7,
  "openskill_tau": 0.1,
  "num_evaluation_bins": 5,
  "inactivity_slash_rate": 0.25,
  "reset_inactivity_windows": 3
}
```
