import subprocess
from datetime import datetime
from pathlib import Path

REPO_PATH = Path(__file__).parent.resolve()


def run_git(command):
    result = subprocess.run(
        command,
        cwd=REPO_PATH,
        capture_output=True,
        text=True,
        shell=True
    )

    if result.stderr:
        print(result.stderr)

    return result.stdout.strip()


today = datetime.now().strftime("%Y-%m-%d")

last_commit_date = run_git(
    'git log -1 --format=%cd --date=format:%Y-%m-%d'
)

if last_commit_date == today:
    print("Ya existe un commit hoy.")
    exit()

# Archivo que se modificará para generar cambios
activity_file = REPO_PATH / "activity.txt"

with open(activity_file, "a", encoding="utf-8") as f:
    f.write(
        f"\nActividad automática: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

# Git
run_git("git add .")

commit_result = run_git(
    f'git commit -m "chore: daily activity {today}"'
)

if "nothing to commit" in commit_result.lower():
    print("No hay cambios para commitear.")
    exit()

run_git("git push origin main")

print("Commit realizado correctamente.")