from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Candidate:
    agent: str
    bid: float
    content: str


@dataclass
class AuctionResult:
    winner: Candidate
    price: float
    metrics: dict


def run_vickrey_auction(candidates: List[Candidate]) -> AuctionResult:
    """Run a minimal Vickrey auction: pick highest bid as winner, price is second highest.

    This is a simplified deterministic auction used for tests and local runs.
    """
    if not candidates:
        raise ValueError("No candidates provided")
    # Sort by bid descending
    sorted_cands = sorted(candidates, key=lambda c: c.bid, reverse=True)
    winner = sorted_cands[0]
    price = sorted_cands[1].bid if len(sorted_cands) > 1 else 0.0
    metrics = {"num_candidates": len(sorted_cands)}
    return AuctionResult(winner=winner, price=price, metrics=metrics)
