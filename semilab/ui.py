"""Console helpers for the interactive walkthrough (auto=True accepts all defaults)."""


def pause(auto, msg="   [Enter to continue] "):
    if not auto:
        input(msg)


def steps(title, items, auto):
    print(f"\n=== {title} ===")
    for i, s in enumerate(items, 1):
        print(f" {i}. {s}")
        pause(auto, "")


def ask_float(prompt, default, auto):
    if auto:
        print(f"{prompt} [{default}] -> {default}")
        return float(default)
    s = input(f"{prompt} [{default}]: ").strip()
    return float(s) if s else float(default)


def ask_str(prompt, default, auto):
    if auto:
        print(f"{prompt} [{default}] -> {default}")
        return default
    s = input(f"{prompt} [{default}]: ").strip()
    return s or default


def header(title, objective):
    bar = "#" * 70
    print(f"\n{bar}\n# {title}\n# Objective: {objective}\n{bar}")
