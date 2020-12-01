#!/usr/bin/env python3

import re
import shlex
import subprocess
import time

def get_commit_log():
    output = subprocess.check_output(shlex.split('git log --pretty=%s --color'), stderr=subprocess.STDOUT)
    output = output.decode('ascii')
    output = output.split('\n')
    return output

def strip_commits(commits):
    output = []
    for line in commits:
        if re.findall(r'^(feat|fix|refactor|test|ci)', line):
            output.append(line)
    return output

def overwrite_changelog(commits):
    print ("Going to write the following commits:\n{}".format(commits))
    with open("/github/home/CHANGELOG.md", "w+") as file:
        file.write('# Changelog\n\n\n## Features\n\n')
        for feat in commits:
            if re.findall(r'^feat', feat):
                file.write('8 {}\n'.format(feat))
        file.write('\n\n Changelog generated through the projects\' Github Actions.')
        file.close()
    return

def main():
    commits = get_commit_log()
    commits = strip_commits(sorted(commits))
    overwrite_changelog(commits)

main()