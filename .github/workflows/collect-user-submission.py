import json
import os
import typing

import pydantic


class Submission(pydantic.BaseModel):
    repo: str


@pydantic.dataclasses.dataclass
class IssueInfo:
    gh_event_path: pydantic.FilePath
    submission: Submission = pydantic.Field(default=None)

    def __post_init_post_parse__(self):
        with open(self.gh_event_path) as f:
            self.data = json.load(f)
        print(self.data)

    def create_submission(self):
        self._create_submission_input()
        return self

    def _create_submission_input(self):
        text = self.data['issue']['body'] 

        left = "### Root Repository Name\n\n"
        right = "\n\n###"
        repo = text[text.index(left)+len(left):text.index(right)])
        repo = f'  - {repo.strip()}'
        
        self.submission = Submission(repo=repo)


if __name__ == '__main__':

    issue = IssueInfo(gh_event_path=os.environ['GITHUB_EVENT_PATH']).create_submission()
    inputs = issue.submission.dict()
    with open('gallery-submission-input.json', 'w') as f:
        json.dump(inputs, f)
