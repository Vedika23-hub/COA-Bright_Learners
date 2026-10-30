"""
Booth and Bit-Pair (Modified Booth) Multiplication Simulator
COA Bright Learner Activity - Task B1

Usage:
    python booth_simulator.py            # traces (-13) x (+11), 6-bit
    python booth_simulator.py -m -13 -q 11 -n 6
    python booth_simulator.py --all      # compares ALL 4-bit operand pairs
"""
import argparse


def b(x, n):
    """Two's-complement binary string of x using n bits."""
    return format(x & ((1 << n) - 1), "0{}b".format(n))


def booth(M, Q, n):
    """Radix-2 Booth. Returns (trace rows, product, add/sub count).
    P = A:Q:Q-1 is held as one signed integer, so Python's >> is exactly
    the arithmetic right shift performed by the hardware."""
    P = (Q & ((1 << n) - 1)) << 1      # A = 0, Q = multiplier, Q-1 = 0
    rows, ops = [], 0
    for step in range(1, n + 1):
        pair = P & 3                   # (Q0, Q-1)
        if pair == 0b10:
            P -= M << (n + 1)
            action = "A = A - M"
            ops += 1
        elif pair == 0b01:
            P += M << (n + 1)
            action = "A = A + M"
            ops += 1
        else:
            action = "no operation"
        a_mid = b(P >> (n + 1), n)
        P >>= 1                        # arithmetic shift right (A, Q, Q-1)
        rows.append((step, "{}{}".format(pair >> 1, pair & 1), action,
                     a_mid, b(P >> (n + 1), n), b(P >> 1, n), str(P & 1)))
    return rows, P >> 1, ops


def bitpair(M, Q, n):
    """Bit-pair (modified Booth / radix-4). n must be even."""
    P = (Q & ((1 << n) - 1)) << 1
    rows, ops = [], 0
    names = {-2: "A = A - 2M", -1: "A = A - M", 0: "no operation",
             1: "A = A + M", 2: "A = A + 2M"}
    for step in range(1, n // 2 + 1):
        q1, q0, qm = (P >> 2) & 1, (P >> 1) & 1, P & 1
        digit = -2 * q1 + q0 + qm      # recoded digit in {-2,-1,0,+1,+2}
        P += (digit * M) << (n + 1)
        ops += digit != 0
        a_mid = b(P >> (n + 1), n + 1)
        P >>= 2                        # arithmetic shift right by 2
        rows.append((step, "{}{}{}".format(q1, q0, qm), names[digit],
                     a_mid, b(P >> (n + 1), n + 1), b(P >> 1, n),
                     str(P & 1)))
    return rows, P >> 1, ops


def show(title, rows, product, n, M, Q):
    print("\n" + title)
    print("Step  Bits  Operation      A(after op)    A        Q        Q-1")
    for r in rows:
        print("{:<5} {:<5} {:<14} {:<14} {:<8} {:<8} {}".format(*r))
    print("Product = {}  ({})  expected {}".format(
        product, b(product, 2 * n), M * Q))


def compare_all(n=4):
    lo, hi = -(1 << (n - 1)), (1 << (n - 1)) - 1
    pairs = better = same = worse = wrong = 0
    tot_b = tot_p = max_b = max_p = 0
    for M in range(lo, hi + 1):
        for Q in range(lo, hi + 1):
            _, p1, o1 = booth(M, Q, n)
            _, p2, o2 = bitpair(M, Q, n)
            wrong += (p1 != M * Q) or (p2 != M * Q)
            pairs += 1
            tot_b += o1
            tot_p += o2
            max_b, max_p = max(max_b, o1), max(max_p, o2)
            if o2 < o1:
                better += 1
            elif o2 == o1:
                same += 1
            else:
                worse += 1
    print("\nAll {}-bit signed pairs ({} to {}): {} pairs".format(
        n, lo, hi, pairs))
    print("Incorrect products         : {}".format(wrong))
    print("Booth total add/sub ops    : {} (avg {:.3f}, max {})".format(
        tot_b, tot_b / pairs, max_b))
    print("Bit-pair total add/sub ops : {} (avg {:.3f}, max {})".format(
        tot_p, tot_p / pairs, max_p))
    print("Cycles per multiplication  : Booth {}, Bit-pair {}".format(
        n, n // 2))
    print("Bit-pair fewer ops in {} pairs, equal in {}, more in {}".format(
        better, same, worse))
    print("Reduction in ops           : {:.1f}%".format(
        100 * (tot_b - tot_p) / tot_b))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", type=int, default=-13, help="multiplicand")
    ap.add_argument("-q", type=int, default=11, help="multiplier")
    ap.add_argument("-n", type=int, default=6, help="register width (even)")
    ap.add_argument("--all", action="store_true",
                    help="compare all 4-bit pairs")
    a = ap.parse_args()
    if a.all:
        compare_all(4)
    else:
        print("M = {} ({}), Q = {} ({}), n = {}".format(
            a.m, b(a.m, a.n), a.q, b(a.q, a.n), a.n))
        r, p, o = booth(a.m, a.q, a.n)
        show("BOOTH'S ALGORITHM", r, p, a.n, a.m, a.q)
        print("Add/subtract operations: {}".format(o))
        r, p, o = bitpair(a.m, a.q, a.n)
        show("BIT-PAIR (MODIFIED BOOTH) RECODING", r, p, a.n, a.m, a.q)
        print("Add/subtract operations: {}".format(o))
