import os
import random
import subprocess
from datetime import datetime, timedelta

# --- CONFIGURATION ---
days_back = 240         # How many days into the past to go
commit_frequency = 0.85  # Probability of committing on any given day (0.0 to 1.0)
max_commits_per_day = 10 # Maximum number of dummy commits per day
# ---------------------

def create_commit(date_string):
    # Write a dummy change to a file
    with open("history.txt", "a") as f:
        f.write(f"Commit for {date_string}\n")
    
    # Stage the file
    subprocess.run(["git", "add", "history.txt"], check=False)

    # Commit with backdated environment variables in a Windows-safe way
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_string
    env["GIT_COMMITTER_DATE"] = date_string

    try:
        subprocess.run(["git", "commit", "-m", "Update project history"], check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"git commit failed: {e}")

# Start from the past and move toward today
start_date = datetime.now() - timedelta(days=days_back)

print(f"Generating history starting from {start_date.strftime('%Y-%m-%d')}...")

for day in range(days_back):
    current_date = start_date + timedelta(days=day)
    
    # Decide if we should commit on this day to keep it looking natural
    if random.random() < commit_frequency:
        # Determine how many commits to make on this specific day
        num_commits = random.randint(1, max_commits_per_day)
        
        for i in range(num_commits):
            # Add random hours/minutes so the timestamps look organic
            hour = random.randint(9, 18)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            
            commit_time = current_date.replace(hour=hour, minute=minute, second=second)
            formatted_date = commit_time.strftime('%Y-%m-%d %H:%M:%S')
            
            create_commit(formatted_date)

print("Done! Run 'git push origin main' to update your GitHub graph.")
