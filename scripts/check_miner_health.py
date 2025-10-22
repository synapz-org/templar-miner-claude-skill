#!/usr/bin/env python3
"""
Templar Miner Health Check Script

Checks key metrics and health indicators for a running Templar miner.
"""

import argparse
import json
import sys
from pathlib import Path


def check_env_variables():
    """Check if required environment variables are set."""
    import os

    required_vars = [
        'HF_TOKEN',
        'WANDB_API_KEY',
        'R2_GRADIENTS_ACCOUNT_ID',
        'R2_GRADIENTS_BUCKET_NAME',
        'R2_DATASET_ACCOUNT_ID',
        'R2_DATASET_BUCKET_NAME',
        'WALLET_NAME',
        'WALLET_HOTKEY',
    ]

    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        return False
    else:
        print("✅ All required environment variables are set")
        return True


def check_gpu_availability():
    """Check if CUDA GPUs are available."""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            print(f"✅ {gpu_count} GPU(s) available")
            for i in range(gpu_count):
                name = torch.cuda.get_device_name(i)
                memory = torch.cuda.get_device_properties(i).total_memory / 1024**3
                print(f"   GPU {i}: {name} ({memory:.1f} GB)")
            return True
        else:
            print("❌ No CUDA GPUs available")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed, cannot check GPU availability")
        return None


def check_wallet_registration():
    """Check if wallet is registered to subnet."""
    import os
    import subprocess

    wallet_name = os.getenv('WALLET_NAME', 'default')
    wallet_hotkey = os.getenv('WALLET_HOTKEY', 'miner')
    netuid = os.getenv('NETUID', '3')

    try:
        result = subprocess.run(
            ['btcli', 'wallet', 'overview',
             '--wallet.name', wallet_name,
             '--wallet.hotkey', wallet_hotkey,
             '--netuid', netuid],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print(f"✅ Wallet registered to subnet {netuid}")
            return True
        else:
            print(f"❌ Wallet not registered or btcli error")
            print(f"   Error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("⚠️  btcli not found in PATH")
        return None
    except Exception as e:
        print(f"⚠️  Could not check registration: {e}")
        return None


def check_r2_connectivity():
    """Check connectivity to R2 buckets."""
    import os
    import subprocess

    account_id = os.getenv('R2_GRADIENTS_ACCOUNT_ID')
    bucket_name = os.getenv('R2_GRADIENTS_BUCKET_NAME')
    access_key = os.getenv('R2_GRADIENTS_READ_ACCESS_KEY_ID')

    if not all([account_id, bucket_name, access_key]):
        print("⚠️  R2 environment variables not fully set")
        return None

    endpoint = f"https://{account_id}.r2.cloudflarestorage.com"

    try:
        # Try to list bucket (requires aws cli)
        result = subprocess.run(
            ['aws', 's3', 'ls', f"s3://{bucket_name}", '--endpoint-url', endpoint],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print(f"✅ R2 gradient bucket accessible")
            return True
        else:
            print(f"❌ Cannot access R2 gradient bucket")
            return False
    except FileNotFoundError:
        print("⚠️  aws CLI not found, cannot check R2 connectivity")
        return None
    except Exception as e:
        print(f"⚠️  R2 connectivity check failed: {e}")
        return None


def check_disk_space():
    """Check available disk space."""
    import shutil

    total, used, free = shutil.disk_usage("/")
    free_gb = free / (1024**3)
    total_gb = total / (1024**3)
    percent_free = (free / total) * 100

    print(f"💾 Disk: {free_gb:.1f} GB free / {total_gb:.1f} GB total ({percent_free:.1f}% free)")

    if free_gb < 50:
        print("   ⚠️  Low disk space (< 50 GB free)")
        return False
    else:
        print("   ✅ Sufficient disk space")
        return True


def check_memory():
    """Check available system memory."""
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()

        mem_info = {}
        for line in lines:
            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                value = int(parts[1].strip().split()[0])  # Value in KB
                mem_info[key] = value

        total_gb = mem_info.get('MemTotal', 0) / (1024**2)
        available_gb = mem_info.get('MemAvailable', 0) / (1024**2)
        percent_available = (available_gb / total_gb) * 100

        print(f"🧠 Memory: {available_gb:.1f} GB available / {total_gb:.1f} GB total ({percent_available:.1f}% available)")

        if total_gb < 200:
            print(f"   ⚠️  Low total memory (< 200 GB, have {total_gb:.1f} GB)")
            return False
        else:
            print(f"   ✅ Sufficient memory")
            return True
    except Exception as e:
        print(f"⚠️  Could not check memory: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Check Templar miner health')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = parser.parse_args()

    print("=" * 60)
    print("Templar Miner Health Check")
    print("=" * 60)
    print()

    checks = [
        ("Environment Variables", check_env_variables),
        ("GPU Availability", check_gpu_availability),
        ("Wallet Registration", check_wallet_registration),
        ("R2 Connectivity", check_r2_connectivity),
        ("Disk Space", check_disk_space),
        ("System Memory", check_memory),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        result = check_func()
        results.append(result)
        print()

    print("=" * 60)
    print("Summary:")
    passed = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is False)
    warnings = sum(1 for r in results if r is None)

    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️  Warnings: {warnings}")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)
    elif warnings > 0:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
