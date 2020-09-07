'''Handles interaction with github'''

import os
from git import Repo
from dotenv import load_dotenv

load_dotenv()


class GithubHandler:
    '''Returns argument a is squared.'''

    def __init__(self):
        self.git_repo_path = os.getenv("GIT_REPO_PATH")

    def add_to_github(self, commit_messge):

        print("Initializing repo")

        repo = Repo(self.git_repo_path)
        changed = [item.a_path for item in repo.index.diff(None)]

        print("Adding and committing changes")

        repo.index.add(changed)
        repo.index.add(repo.untracked_files)
        repo.index.commit(commit_messge)

        print("Pushing changes")

        origin = repo.remote(name="origin")
        origin.push()