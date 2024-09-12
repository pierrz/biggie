"""
Script used to rename all release tags which start with 'v' such as 'v0.3.2'
and remove this prefix.
"""

import os

from github import Github

# GitHub personal access token
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

# Repository name (format: "owner/repo")
REPO_NAME = "pierrz/biggie"

# Initialize GitHub client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)


def update_release_tag(release):
    old_tag = release.tag_name
    if old_tag.startswith("v"):
        new_tag = old_tag[1:]
        try:
            # Update the release tag
            release.update_release(tag_name=new_tag)

            # Delete the old tag
            repo.get_git_ref(f"tags/{old_tag}").delete()

            # Create the new tag
            sha = repo.get_commits()[0].sha
            repo.create_git_ref(f"refs/tags/{new_tag}", sha)

            print(f"Updated release tag from {old_tag} to {new_tag}")
        except Exception as e:
            print(f"Error updating release {old_tag}: {str(e)}")
    else:
        print(f"Skipping release {old_tag} (doesn't start with 'v')")


# Fetch all releases
releases = repo.get_releases()

# Update each release
for release in releases:
    update_release_tag(release)

print("Finished updating release tags.")
