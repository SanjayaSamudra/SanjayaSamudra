import os
from datetime import datetime, timedelta
from git import Repo
import xml.etree.ElementTree as ET

# Your repository details
repo_path = 'https://github.com/SanjayaSamudra/SanjayaSamudra.git'
local_repo_path = 'cloned_repo'

# Clone the repository if not already cloned
if not os.path.exists(local_repo_path):
    repo = Repo.clone_from(repo_path, local_repo_path)
else:
    repo = Repo(local_repo_path)

author = 'Sanjaya Samudra <sanjayasamudraelpitiya@gmail.com>'

# Define the wave pattern
wave_pattern = [
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    [(4, 1), (3, 1), (2, 1), (1, 1), (0, 1)],
    [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)],
    [(4, 3), (3, 3), (2, 3), (1, 3), (0, 3)],
    [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]
]

# Ensure the local_repo_path exists
if not os.path.exists(local_repo_path):
    os.makedirs(local_repo_path)

# Create an SVG with the wave pattern
svg_path = os.path.join(local_repo_path, 'wave_pattern.svg')
svg = ET.Element('svg', width='200', height='200', xmlns='http://www.w3.org/2000/svg')
rect = ET.SubElement(svg, 'rect', x='10', y='10', width='180', height='180', fill='none', stroke='black')

# Add wave pattern to SVG
for day_offset, wave_row in enumerate(wave_pattern):
    for position in wave_row:
        ET.SubElement(svg, 'circle', cx=str(10 + position[0] * 40), cy=str(10 + position[1] * 40), r='10', fill='blue')

# Write the SVG file
tree = ET.ElementTree(svg)
tree.write(svg_path)

# Change directory to the cloned repo
os.chdir(local_repo_path)

# Make commits for the wave pattern
start_date = datetime(2024, 7, 1, 12, 0)  # Example: July 1, 2024, 12:00 PM
commit_time = start_date

for day_offset, wave_row in enumerate(wave_pattern):
    for position in wave_row:
        # Calculate commit date
        commit_date = commit_time + timedelta(days=day_offset)

        # Create a new file or modify existing files as needed
        file_path = os.path.join(local_repo_path, f'wave_{position[0]}_{position[1]}.txt')
        with open(file_path, 'w') as f:
            f.write(f'Commit at {commit_date}\n')

        # Stage changes
        repo.index.add([file_path])

        # Commit
        commit_message = f'Wave commit at {commit_date}'
        repo.index.commit(commit_message, author=author, author_date=commit_date)

# Add and commit the SVG file
repo.index.add([svg_path])
commit_message = 'Add wave pattern SVG'
repo.index.commit(commit_message, author=author, author_date=commit_time)

# Push changes to remote
repo.remotes.origin.push()
