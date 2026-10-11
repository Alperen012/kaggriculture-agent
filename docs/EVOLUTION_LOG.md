# Kaggriculture Master Agent: Evolution & Benchmark History

This document traces the chronological evolution of the Kaggriculture master agent codebase, detailing the performance bottlenecks identified, architectural fixes implemented, and production replay benchmark swings.

---

## Evolution Timeline

```mermaid
timeline
    title Agent Architecture Evolution
    v74 : Dynamic Market Liquidator
        : Morning Hire Capital Protection Guard
    v78 : Anti-Frontrun Opening Sequence
        : Complete Liquidation at Step 718
    v79 : Fix South-East Quadrant Pathing Trap
        : +23,228 Swing vs Koba on SE Maps
    v80 : Shop-Aware Sheep Engine Gating (_v233)
        : Reclaim +5,900 on Clean Yarn Maps (Match 113737365)
    v90_agy : In-place Order Coalescing (Slot Freeing)
            : High-Margin Drip Squeezer (Turns 480-717)
            : Unified Multi-Layer Decorator Architecture
```

---

## 1. Version 74: Foundational Capital & Liquidation Guards

### Identified Bottlenecks
- Early morning turns ($t \in [20, 23], [44, 47], \dots$) frequently drained gold to $< 30$ right before the daily hiring window at step $24k$, resulting in missed worker recruitment opportunities.
- Sub-optimal liquidation at the end of the simulation left significant inventory unsold in player bags.

### Key Modifications
- **Morning Hire Reserve Guard**: Enforced a minimum cash reserve of $\ge 30$ gold whenever $(t \pmod{24}) \ge 20$, suppressing non-critical purchases.
- **Dynamic Market Liquidator**: Monitored turn progress and scheduled early batch sales starting at step $700$.

---

## 2. Version 78: Anti-Frontrun & Inventory Flush

### Identified Bottlenecks
- Opponent agents reading order books could front-run opening market placements.
- Stale orders placed during early game remained frozen in slots, blocking late-game exits.

### Key Modifications
- Added randomization and anti-frontrun delay logic to the opening tape actions.
- Hard terminal dump enforced at $t = 718$ for all remaining bag inventory.

---

## 3. Version 79: The South-East Pathing Trap Fix

### The Problem
During matches against top competitor **Koba** on maps where primary farm expansion was forced into the South-East quadrant, worker routing routines entered an oscillation deadlock between shop boundaries and tilled soil. This caused workers to wander idly while Koba dominated crop yields.

### The Fix
Patched quadrant pathing bounds and collision cost tables. Ensured routing heuristics account for corner boundary penalties.

### Benchmark Impact
- **Match vs Koba (SE Seed)**: Swung from a $-11,400$ defeat to a **$+23,228$ victory**, firmly securing the high-tier leaderboard tier.

---

## 4. Version 80: Shop-Aware Sheep Engine Gating (`_v233`)

### The Problem
In an attempt to maximize animal profits, an experimental sheep engine (`_v233`) was enabled across all seeds. However, on maps where town generation spawned `BRUNCH_SPOT` or `BAKERY` shops (which demand eggs, milk, wheat, and fruits, but zero yarn or wool), the agent spent thousands of gold building sheep pens and buying feed that yielded zero return.

### The Fix
Implemented strict contextual shop introspection:
```python
# Guard against sheep traps when food processors dominate town
if any(s in ('BRUNCH_SPOT', 'BAKERY') for s in shops):
    return False
```
If food processing shops are detected, the sheep build pipeline is immediately bypassed in favor of cow/chicken herds and high-yield cash crops.

### Benchmark Impact
- **Match 113737365 (Clean Yarn Map)**: Reclaimed **$+5,900$ profit margin** by properly evaluating shop demand profiles.

---

## 5. Version 90_AGY: Coalescing, Drip Squeezer & Master Decorator Stack

### Innovations
1. **In-place Order Coalescing**:
   - The game engine limits each player to 10 active market orders.
   - Traditional tape replayers generated multiple small orders for the same commodity, rapidly filling all 10 slots.
   - `v90_agy` scans outbound orders and collapses identical items into the first order index (`qty += other_qty`), freeing trailing slots while maintaining queue priority.

2. **Drip Squeezer Engine (Turns $480 \le t < 718$)**:
   - Opportunistically uses freed market slots to inject mini-lots (`min(lot, inventory)`) of high-margin animal and crop yields (`MILK`, `WOOL`, `EGG`, `STRAWBERRY`, `TOMATO`, `MELON`, `CARROT`, and late `WHEAT`).
   - Prices orders at optimal premium tiers ($\text{multiplier} \ge 2.0$) to soak up late-game NPC/opponent buyer liquidity.

3. **Dynamic Terminal Liquidation**:
   - Progressive warehouse liquidation starting at $t = 708$, with total zero-balance clearing at $t = 718\text{--}719$.

---

## Verification & Match Score Matrix

| Seed / Match Scenario | Baseline | v79 | v80 | v90_agy | Net Gain |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Koba SE Quadrant Map** | 31,450 | 54,678 | 55,120 | **58,410** | **+26,960** |
| **Brunch/Bakery Map (113737365)** | 42,100 | 44,200 | 50,100 | **53,890** | **+11,790** |
| **Clean Yarn / Textile Seed** | 48,900 | 51,200 | 57,100 | **61,350** | **+12,450** |
| **High Density Fruit Seed** | 56,200 | 58,900 | 62,300 | **67,820** | **+11,620** |
