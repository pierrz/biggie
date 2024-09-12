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


def init_github_client():
    GITHUB_TOKEN = os.environ["RENAME_RELEASE_TOKEN"]
    return Github(GITHUB_TOKEN)


def get_repository(g, repo_name):
    try:
        repo = g.get_repo(repo_name)
        print(f"Repository: {repo.full_name}")
        if not repo.permissions.push:
            raise Exception(
                "The authenticated user doesn't have push access to this repository."
            )
        return repo
    except GithubException as e:
        print(f"Error accessing repository: {e.status} {e.data.get('message', '')}")
        raise


def create_new_release(repo, old_release, new_tag):
    return repo.create_git_release(
        tag=new_tag,
        name=old_release.title or new_tag,
        message=old_release.body or "",
        draft=old_release.draft,
        prerelease=old_release.prerelease,
        target_commitish=old_release.target_commitish,
    )


def delete_old_tag(repo, old_tag):
    try:
        repo.get_git_ref(f"tags/{old_tag}").delete()
        print(f"Deleted old tag: {old_tag}")
    except GithubException:
        print(f"Old tag {old_tag} not found, skipping deletion")


def update_single_release(repo, release):
    old_tag = release.tag_name
    if not old_tag.startswith("v"):
        print(f"Skipping release {old_tag} (doesn't start with 'v')")
        return

    new_tag = old_tag[1:]
    try:
        print(f"Attempting to update release: {old_tag} to {new_tag}")
        new_release = create_new_release(repo, release, new_tag)
        print(f"Created new release: {new_release.tag_name}")

        release.delete_release()
        print(f"Deleted old release: {old_tag}")

        delete_old_tag(repo, old_tag)

        print(f"Successfully updated release tag from {old_tag} to {new_tag}")
    except GithubException as e:
        print(
            f"Error updating release {old_tag}: {e.status} {e.data.get('message', '')}"
        )
        if e.status == 403:
            print(
                "This could be due to insufficient permissions. Check your token scopes and repository access."
            )
    except Exception as e:
        print(f"Unexpected error updating release {old_tag}: {str(e)}")


def main():

    try:
        g = init_github_client()
        user = g.get_user()
        print(f"Authenticated as: {user.login}")

        repo = get_repository(g, REPO_NAME)

        releases = list(repo.get_releases())
        print(f"Found {len(releases)} releases")

        for release in releases:
            update_single_release(repo, release)

        print("Finished updating release tags.")
    except GithubException as e:
        print(f"GitHub API error: {e.status} {e.data.get('message', '')}")
        if e.status == 403:
            print(
                "This could be due to insufficient permissions. Check your token scopes and repository access."
            )
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
