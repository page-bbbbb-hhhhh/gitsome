from __future__ import print_function, unicode_literals
import re
import requests
from datetime import datetime
from github3 import GitHub

import os
import re
import builtins
import pickle
import subprocess
import sys

from tabulate import tabulate
from xonsh.built_ins import iglobpath
from xonsh.tools import subexpr_from_unbalanced
from xonsh.tools import ON_WINDOWS
from xonsh.environ import user_and_repo_from_path


class GitSome(object):
    def __init__(self):
        get_env = lambda name, default=None: builtins.__xonsh_env__.get(name,
                                                                        default)
        self.user_id = get_env('GITHUB_USER_ID', None)
        self.user_pass = get_env('GITHUB_USER_PASS', None)
        self.gh = GitHub(self.user_id, self.user_pass)
        self.dispatch = {
            'emails': self.emails,
            'emojis': self.emojis,
            'events': self.events,
            'feeds': self.feeds,
            'followers': self.followers,
            'following': self.following,
            'gitignore_template': self.gitignore_template,
            'gitignore_templates': self.gitignore_templates,
            'issue': self.issue,
            'issues': self.issues,
            'me': self.me,
            'notifications': self.notifications,
            'octocat': self.octocat,
            'pull_requests': self.pull_requests,
            'repo': self.repo,
            'repos': self.repos,
            'search_issues': self.search_issues,
            'search_repositories': self.search_repositories,
            'stars': self.stars,
        }

    def _two_factor_code(self):
        code = ''
        while not code:
            code = input('Enter 2FA code: ')
        return code

    def _return_elem_or_list(self, args):
        if len(args) == 1:
            return args[0]
        else:
            return args

    def _extract_args(self,
                      input_args,
                      default_args,
                      expected_args):
        if not input_args and default_args is not None:
            return self._return_elem_or_list(default_args)
        valid_args = True
        if (expected_args is not None and input_args is None) or \
            len(input_args) != len(expected_args):
            valid_args = False
        if not valid_args:
            print('Error, expected arguments:', expected_args)
            return None
        else:
            return self._return_elem_or_list(input_args)
        return None

    def _format_repo(self, repo):
        return '/'.join(repo)

    def _listify(self, items):
        output = []
        for item in items:
            item_list = []
            item_list.append(item)
            output.append(item_list)
        return output

    def _print_items(self, items, headers):
        table = []
        for item in items:
            import pdb; pdb.set_trace()
            table.append(item)
        print(tabulate(table, headers=headers, tablefmt='grid'))

    def execute(self, tokens):
        if tokens:
            method = tokens[0]
            args = tokens[1:] if tokens[1:] else None
            if method == 'stars':
                self.stars(args)
            elif method == 'octocat':
                self.octocat(args)

    def octocat(self, say=None):
        if say is not None:
            say = ' '.join(say)
        output = str(self.gh.octocat(say))
        output = output.replace('\\n', '\n')
        print(output)

    def stars(self, tokens):
        if not tokens:
            user_id, repo = user_and_repo_from_path()
        else:
            if len(tokens) != 2:
                print('gh stars expected arguments: [user id] [repo name]')
                return
            else:
                user_id, repo = tokens
        url = 'https://api.github.com/repos/' + self.user_id + '/' + repo
        r = requests.get(url, auth=(self.user_id, self.user_pass))
        response = r.json()
        print('Stars for ' + user_id + '/' + repo + ': ' + str(response['stargazers_count']))
