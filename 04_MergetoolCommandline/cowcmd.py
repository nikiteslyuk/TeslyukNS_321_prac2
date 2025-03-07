import cmd
import shlex
import cowsay


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


class CowCmd(cmd.Cmd):
    prompt = "twocows> "

    def do_list_cows(self, arg):
        "List available cow files"
        print(" ".join(cowsay.list_cows()))

    def do_make_bubble(self, arg):
        "Create a speech bubble with given text"
        try:
            args = shlex.split(arg)
            if len(args) < 1:
                print("Usage: make_bubble <text>")
                return
            print(cowsay.make_bubble(" ".join(args)))
        except Exception as e:
            print("Error:", e)

    def do_cowsay(self, arg):
        "Cowsay message [cow_name] [eyes=value] [tongue=value] reply message [cow_name] [eyes=value] [tongue=value]"
        try:
            args = shlex.split(arg)
            if len(args) < 2:
                print("Usage: cowsay <message1> [options] reply <message2> [options]")
                return

            msg1 = args.pop(0)
            cow1 = "default"
            opts1 = {}
            if args and args[0] not in ["reply", "eyes=", "tongue="]:
                cow1 = args.pop(0)

            while args and "=" in args[0]:
                key, value = args.pop(0).split("=", 1)
                opts1[key] = value

            if not args or args.pop(0) != "reply":
                print("Error: 'reply' keyword is missing")
                return

            msg2 = args.pop(0)
            cow2 = "default"
            opts2 = {}
            if args and args[0] not in ["eyes=", "tongue="]:
                cow2 = args.pop(0)

            while args and "=" in args[0]:
                key, value = args.pop(0).split("=", 1)
                opts2[key] = value

            cow1_str = cowsay.cowsay(msg1, cow=cow1, **opts1)
            cow2_str = cowsay.cowsay(msg2, cow=cow2, **opts2)
            print(side_by_side(cow1_str, cow2_str))
        except Exception as e:
            print("Error:", e)

    def do_cowthink(self, arg):
        "Cowthink message [cow_name] [eyes=value] [tongue=value]"
        try:
            args = shlex.split(arg)
            if len(args) < 1:
                print("Usage: cowthink <message> [options]")
                return
            msg = args.pop(0)
            cow = "default"
            opts = {}
            if args and args[0] not in ["eyes=", "tongue="]:
                cow = args.pop(0)

            while args and "=" in args[0]:
                key, value = args.pop(0).split("=", 1)
                opts[key] = value

            print(cowsay.cowthink(msg, cow=cow, **opts))
        except Exception as e:
            print("Error:", e)

    def do_exit(self, arg):
        "Exit the command line"
        return True

    def do_EOF(self, arg):
        "Exit on Ctrl+D"
        print()
        return True


if __name__ == "__main__":
    CowCmd().cmdloop()
