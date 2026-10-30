# Booth and Modified Booth (Bit-Pair) Multiplication Simulator

COA Bright Learner Activity - Task B1
Course: 25CE3PCC03 - Computer Organization and Architecture, Don Bosco Institute of Technology

## What it does
- Multiplies two signed numbers with **Booth's algorithm** and **bit-pair (modified Booth) recoding**, showing A, Q and Q-1 at every step.
- Compares the number of add/subtract operations of both algorithms for **all 4-bit operand pairs** (-8 to +7, 256 pairs) and checks every product.

## How to run (Python 3, no libraries needed)
```
python booth_simulator.py                  # traces (-13) x (+11), 6-bit
python booth_simulator.py -m 5 -q -3 -n 4  # any pair and width
python booth_simulator.py --all            # compare all 4-bit pairs
```

## Test results
| Test | Result |
|------|--------|
| (-13) x (+11), 6-bit | Product -143 (correct). Booth: 4 add/sub in 6 steps. Bit-pair: 3 add/sub in 3 steps |
| All 256 4-bit pairs | 0 incorrect products |
| Total add/sub operations | Booth 512 (avg 2.00, max 4); Bit-pair 384 (avg 1.50, max 2) |
| Reduction | 25% fewer operations; steps halved (4 to 2) |
| Bit-pair vs Booth | fewer in 112 pairs, equal in 144, more in 0 |

Full outputs: `test_output_6bit_example.txt` and `test_output_all_4bit_pairs.txt`.

## Files
- `booth_simulator.py` - source code
- `test_output_6bit_example.txt` - step-by-step trace output
- `test_output_all_4bit_pairs.txt` - comparison output for all 4-bit pairs
