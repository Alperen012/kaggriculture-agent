# Kaggriculture Simulation & Game Mechanics

A comprehensive technical reference for the Kaggle Kaggriculture simulation environment, economics, spatial grids, and mechanics.

---

## 1. Simulation Overview & Time Scale

- **Grid Size**: $10 \times 10$ toroidal/bounded grid (farm layout with dedicated shop, field, and barn zones).
- **Duration**: Exactly **30 game days** ($720$ steps total, $24$ steps per day).
- **Turn Granularity**: 1 step = 1 hour of game time.
- **Workers**: Autonomous agents controlled per turn. Additional workers can be hired at the farmhouse each morning (Turn $\equiv 0 \pmod{24}$).
- **Objective**: Maximize final liquid cash ($\text{balance}$) at Step 719.

---

## 2. Worker Economics & Hiring Mechanics

- **Base Worker**: Every farm starts with 1 worker.
- **Hiring Schedule**: Workers can only be recruited at daybreak ($t = 0, 24, 48, \dots$).
- **Hiring Costs**: Hiring costs follow a strict exponential/Fibonacci cost curve:
  $$\text{Cost}(N) = C_0 \times \phi^{N-1}$$
  Missing a morning hire due to cash depletion ($< \text{HireCost}$) starves worker throughput for the next 24 turns. This is why **Morning Hire Capital Protection Guards** (e.g., reserving $\ge 30$ gold on pre-dawn steps $20\text{--}23$) are critical.
- **Worker Actions**: Each step, a worker may:
  - `MOVE [UP, DOWN, LEFT, RIGHT]`
  - `TILL` / `PLANT [SEED_TYPE]` / `WATER` / `HARVEST`
  - `FEED [ANIMAL_TYPE]` / `COLLECT [ANIMAL_PRODUCT]`
  - `BUY [ITEM, QTY]` / `SELL [ITEM, QTY]` at adjacent shop or market

---

## 3. Crop Lifecycles & Soil Dynamics

Crops progress through distinct growth stages based on hydration and soil quality:

| Crop | Seed Cost | Maturation (steps) | Water Requirement | Base Yield Value | Yield Multiplier |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Carrot** | Low | Fast (12--18h) | Low | Low-Medium | Quick cash cycles |
| **Wheat** | Very Low | Medium (24--36h) | Low | Low | Animal feed & late flour |
| **Tomato** | Medium | Medium-Fast (18--24h) | Medium | Medium-High | High margin cash crop |
| **Melon** | High | Slow (48--72h) | High | Very High | Premium bulk cash |
| **Strawberry** | High | Very Slow (72h+) | High | Maximum | Ultra-late endgame windfall |

---

## 4. Livestock & Animal Products

Livestock require daily feeding and shelter maintenance:

- **Chickens**: Low feed consumption (Wheat/Seeds). Produces **Eggs** daily. Fast ROI.
- **Cows**: Medium feed consumption (Wheat/Hay). Produces **Milk** every 12--24 hours. Reliable steady cashflow.
- **Sheep**: Heavy feed consumption. Produces **Wool** (or processed **Yarn**).
  - *Strategic Catch*: On maps without dedicated Yarn/Fabric processing shops, or where Brunch Spots / Bakeries dominate local demand, sheep build-outs cause catastrophic cash traps (negative ROI due to feed consumption vs sell price).

---

## 5. Village Shops & Town Unlock Cadence

Village shops unlock progressively every 3 days ($72$ steps):

- **Day 0 (Step 0)**: Basic General Store & Seed Merchant.
- **Day 3 (Step 72)**: Local Marketplaces & Feed Mill.
- **Day 6--15**: Specialized processors (Bakery, Brunch Spot, Textile Mill, Juice Bar, Dairy).
- **Dynamic Demand & Price Multipliers**:
  - Processing shops purchase specific high-tier goods at significant premiums (e.g. $1.8\times\text{--}2.5\times$ base market value).
  - If a map features `BRUNCH_SPOT` and `BAKERY`, egg/milk/crop demand spikes while wool remains unsellable at parity.

---

## 6. Central Market & Order-Book Priority

The market allows placing buy and sell orders.

- **Order Limit**: Maximum **10 active orders** per player simultaneously.
- **Execution Engine**:
  - Orders are matched based on price priority, followed by arrival order (FIFO).
  - Unmatched orders tie up order slots. If all 10 slots are occupied by stale high-price asks, no new orders can be dispatched.
- **V90_AGY Coalescing Solution**:
  - In-place coalescing groups duplicate item orders into the earliest matching slot index, freeing up trailing slots for the **Drip Squeezer** without losing FIFO priority in the order book.

---

## 7. Endgame Liquidation (Step 708--719)

- All assets, inventories, crops, and animal goods have **zero terminal value** unless converted to liquid currency.
- Steps $708\text{--}718$ require progressive terminal liquidation.
- Step $719$ is the final settlement step where all remaining items must be dumped at whatever bid price exists.
