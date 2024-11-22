import re

# Raw text from Instagram comments
# Read raw text from 'raw_sorteo.txt' file
with open('raw_sorteo.txt', 'r', encoding='utf-8') as file:
    raw_text = file.read()

# Extract lines with mentions (start with '@')
lines_with_mentions = [line.strip() for line in raw_text.split('\n') if line.startswith('@')]
lines = [line.strip() for line in raw_text.split('\n')]
lines_with_users = []

# Rule: Valid entries must have exactly two mentions
valid_entries = []

for line in lines_with_mentions:
    # Use regex to find all mentions in the line
    mentions = re.findall(r'@[\w\._]+', line)
    if len(mentions) == 2:  # Check if there are exactly two mentions
        idx = raw_text.index(line)
        previous_line = lines[lines.index(line) - 1]
        if "Foto del perfil de " in previous_line:
            username = previous_line.split("Foto del perfil de ")[1].split()[0]
            valid_entries.append((username, mentions))

# Display the valid entries
for idx, entry in enumerate(valid_entries, 1):
    print(f"{idx}. Mentions: {entry[0]}, {entry[1]}")

# Optional: Save valid entries to a file
with open("valid_entries.txt", "w", encoding="utf-8") as file:
    for entry in valid_entries:
        file.write(f"{entry[0]}, {entry[1]}\n")

# Now count the number of valid entries per username (SELECT COUNT(*) FROM valid_entries GROUP BY username)

# Count the number of valid entries per username
entry_count = {}
for entry in valid_entries:
    username = entry[0]
    if username in entry_count:
        entry_count[username] += 1
    else:
        entry_count[username] = 1

sum_count = 0
# Write the count of valid entries per username to a file
with open("entry_count.txt", "w", encoding="utf-8") as file:
    for username, count in entry_count.items():
        sum_count += count
        file.write(f"{username}: {count}\n")

# Now assign probabilities to each user based on the number of valid entries
probabilities = {}
for username, count in entry_count.items():
    probabilities[username] = count / sum_count

# Write the probabilities to a file
with open("probabilities.txt", "w", encoding="utf-8") as file:
    for username, prob in probabilities.items():
        file.write(f"{username}: {prob}\n")

# Now we can randomly select a winner based on the probabilities
import random

# Randomly select a winner based on the probabilities
winner = random.choices(list(probabilities.keys()), list(probabilities.values()), k=1)[0]
print(f"The winner is: {winner}")


