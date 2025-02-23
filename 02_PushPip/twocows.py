import cowsay
import argparse


def side_by_side(cow1_str, cow2_str, gap=4):
    lines1 = cow1_str.rstrip().splitlines()
    lines2 = cow2_str.rstrip().splitlines()
    max_lines = max(len(lines1), len(lines2))
    if len(lines1) < max_lines:
        lines1 = [""] * (max_lines - len(lines1)) + lines1
    if len(lines2) < max_lines:
        lines2 = [""] * (max_lines - len(lines2)) + lines2
    width1 = max(len(line) for line in lines1)
    gap_str = " " * gap
    combined_lines = [
        line1.ljust(width1) + gap_str + line2 for line1, line2 in zip(lines1, lines2)
    ]
    return "\n".join(combined_lines)


parser = argparse.ArgumentParser()
parser.add_argument("message1")
parser.add_argument("message2")
parser.add_argument("-f", "--cowfile", default="default")
parser.add_argument("-e", "--eyes", default="oo")
parser.add_argument("-T", "--tongue", default="  ")
parser.add_argument("-F", "--cowfile2", default="default")
parser.add_argument("-E", "--eyes2", default="oo")
parser.add_argument("-N", "--tongue2", default="  ")

args = parser.parse_args()

cow1_str = cowsay.cowsay(
    args.message1, cow=args.cowfile, eyes=args.eyes, tongue=args.tongue
)
cow2_str = cowsay.cowsay(
    args.message2, cow=args.cowfile2, eyes=args.eyes2, tongue=args.tongue2
)
combined = side_by_side(cow1_str, cow2_str, gap=4)
print(combined)
