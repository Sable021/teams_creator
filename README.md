# Teams Creator

This python application will split up a large group of participants into smaller teams, based on provided parameters.

Usage:
At root folder, run command "py src/main.py <participants_file>".

Parameters:
1. List of participants to split
 - Name
 - Cluster
2. Number of teams
3. Maximum of participants in the same cluster in a team (Optional)


Use Cases:
1. The application must split any number of participants equally. Output will be the team members in each team.
2. If the number of participants cannot be evenly split into the required number of teams, the difference between team size is minimised.
3. If maximum number of participants from the same cluster is provided, the number must be respected.
4. Application will return a "Cannot Split" error if there is no logical way to successfully do the splitting.