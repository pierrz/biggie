"""
Script used to rename all release tags which start with 'v' such as 'v0.3.2'
and remove this prefix.
"""

import os

from github import Github, GithubException

# GitHub personal access token
GITHUB_TOKEN = os.environ["RENAME_RELEASE_TOKEN"]

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
            # Create new release with updated tag
            repo.create_git_release(
                tag=new_tag,
                name=release.title,
                message=release.body,
                draft=release.draft,
                prerelease=release.prerelease,
                target_commitish=release.target_commitish,
            )

            # Delete the old release
            release.delete_release()

            # Delete the old tag
            try:
                repo.get_git_ref(f"tags/{old_tag}").delete()
            except GithubException:
                print(f"Old tag {old_tag} not found, skipping deletion")

            print(f"Updated release tag from {old_tag} to {new_tag}")
        except Exception as e:
            print(f"Error updating release {old_tag}: {str(e)}")
    else:
        print(f"Skipping release {old_tag} (doesn't start with 'v')")


# Fetch all releases
releases = list(
    repo.get_releases()
)  # Convert to list to avoid issues with deleting during iteration

# Update each release
for release in releases:
    update_release_tag(release)

print("Finished updating release tags.")
