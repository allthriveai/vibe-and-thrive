"""
ASCII art banner for vibe-and-thrive CLI tools.
"""

from . import __version__

# Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
DIM = '\033[2m'
RESET = '\033[0m'

BANNER = f"""{CYAN}
 ╭─────────────────────────────────────╮
 │  {MAGENTA}✨ vibe & thrive{CYAN}                   │
 │  {DIM}AI coding guardrails{RESET}{CYAN}               │
 ╰─────────────────────────────────────╯{RESET}
"""

BANNER_MINI = f"{MAGENTA}✨ vibe & thrive{RESET} {DIM}v{__version__}{RESET}"


def print_banner(mini: bool = False) -> None:
    """Print the vibe-and-thrive banner."""
    if mini:
        print(BANNER_MINI)
    else:
        print(BANNER)


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{GREEN}✓{RESET} {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"{YELLOW}⚠{RESET} {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"{RED}✗{RESET} {message}")


def print_finding(filepath: str, line_num: int, description: str) -> None:
    """Print a single finding."""
    print(f"  {DIM}{filepath}:{line_num}{RESET} {description}")


def print_summary(tool_name: str, total: int, files_checked: int) -> None:
    """Print a summary of findings."""
    if total == 0:
        print(f"\n{GREEN}✓{RESET} {tool_name}: All clear! ({files_checked} files checked)")
    else:
        print(f"\n{YELLOW}⚠{RESET} {tool_name}: {total} issue(s) found in {files_checked} files")


def format_blocked() -> str:
    """Return the BLOCKED indicator."""
    return f"{RED}{BOLD}BLOCKED{RESET}"


def format_warning() -> str:
    """Return the WARNING indicator."""
    return f"{YELLOW}WARNING{RESET}"
