import subprocess
from datetime import datetime
from pathlib import Path

REPO_PATH = Path(__file__).parent.resolve()
MAX_COMMITS_PER_DAY = 5


def run_git(command):
    result = subprocess.run(
        command,
        cwd=REPO_PATH,
        capture_output=True,
        text=True,
        shell=True
    )

    return result.stdout.strip()


today = datetime.now().strftime("%Y-%m-%d")

commits_today = run_git(
    f'git log --since="{today} 00:00:00" --until="{today} 23:59:59" --oneline'
)

commit_count = len([line for line in commits_today.splitlines() if line.strip()])

if commit_count >= MAX_COMMITS_PER_DAY:
    print(f"Límite alcanzado ({MAX_COMMITS_PER_DAY} commits hoy).")
    exit()

activity_file = REPO_PATH / "activity.txt"

with open(activity_file, "a", encoding="utf-8") as f:
    f.write(
        f"\nActividad automática #{commit_count + 1}: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

run_git("git add .")

commit_message = (
    f'chore: daily activity {today} '
    f'({commit_count + 1}/{MAX_COMMITS_PER_DAY})'
)

run_git(f'git commit -m "{commit_message}"')
run_git("git push origin main")

print(
    f"Commit {commit_count + 1}/{MAX_COMMITS_PER_DAY} realizado correctamente."
)