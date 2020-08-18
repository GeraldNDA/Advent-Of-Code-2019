#!/usr/bin/env python3
import os, stat
import sys
import requests
import inspect

from datetime import datetime
from email.utils import parsedate_to_datetime as headerdate_to_datetime
from requests import Session, RequestException
from os import path
from shutil import copyfile

class AdventOfCode():
    AOC_SESSION_FILE = "~/.aoc_session"
    def __init__(self, year=None, day=None):
        now = datetime.now()
        self.day = day if day is not None else now.day
        self.year = year  if year is not None else now.year
        session_info_file = path.expanduser(AdventOfCode.AOC_SESSION_FILE)
        if not path.exists(session_info_file):
            raise ValueError(f"Cannot get do anything if '{AdventOfCode.AOC_SESSION_FILE}' does not exist.")
        
        with open(session_info_file) as aoc_session:
            self.session = Session()
            self.session.cookies['session'] = aoc_session.read().strip()\
    

    def get_input(self, raw=False):
        input_files = (f"day{self.day}.txt", f"day{self.day}/day{self.day}.txt")
        chosen_file = None
        for input_file in input_files:
            if path.exists(input_file):
                chosen_file = input_file
                grabbed_time = datetime.fromtimestamp(os.stat(input_file).st_mtime)
                input_release = datetime(self.year, 12, self.day)
                if input_release > grabbed_time:
                    continue

        puzzle_input = []

        if not chosen_file:
            print("Updating...")
            with self.session as session:
                response = session.get(f"https://adventofcode.com/{self.year}/day/{self.day}/input", stream=True)
                response.raise_for_status()
                with open(input_files[-1], "bw") as contents:
                    for line  in response.iter_lines():
                        if line:
                            if not raw:
                                puzzle_input.append(line.decode('utf-8').strip())
                            else:
                                puzzle_input.append(line.decode('utf-8'))
                        contents.write(line)
                        contents.write(b"\n")
        else:
            with open(chosen_file) as contents:
                if not raw:
                    puzzle_input = list(map(lambda l: l.strip(), contents.readlines()))
                else:
                    puzzle_input = list(map(lambda l: l.strip("\n"), contents.readlines()))

        if not puzzle_input:
            return None
        elif len(puzzle_input) == 1:
            return puzzle_input[0]
        return puzzle_input

    @staticmethod
    def generate_scripts(day=None, year=None):
        now  = datetime.now()
        if day is not  None:
            now = now.replace(day=day)
        if year is not None:
            now = now.replace(year=year)
        script_content = f"""
        #!/usr/bin/env python3
        # Imports
        from aoc import AdventOfCode
        
        # Input Parse
        puzzle = AdventOfCode(year={now.year}, day={now.day})
        puzzle_input = puzzle.get_input()
        
        # Actual Code
        result = puzzle_input
        
        # Result
        print(result)
        """
        script_content = inspect.cleandoc(script_content)
        script_dir = f"day{now.day}"
        script_names = (
            f"day{now.day}_1.py",
            f"day{now.day}_2.py",
        )
        # set up dir structure
        aoc_script_dir = path.dirname(path.realpath(__file__))
        aoc_script = path.join(aoc_script_dir, "aoc.py")
        if path.split(os.getcwd())[-1] != script_dir:
            if not path.exists(f"./{script_dir}"):
                os.makedirs(f"./{script_dir}")
            os.chdir(script_dir)
        # copy this script into folder
        if not path.exists("./aoc.py"):
            assert path.exists(aoc_script)

            copyfile(aoc_script, "./aoc.py")
        # set up file structure
        for script_name in script_names:
            if not path.exists(script_name):
                with open(script_name, "w") as script:
                    script.write(script_content)
                os.chmod(script_name, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)

if __name__ == "__main__":
    day = None
    year = None
    if len(sys.argv) > 1:
        day = int(sys.argv[1])
    if len(sys.argv) > 2:
        year = int(sys.argv[2])
    AdventOfCode.generate_scripts(day, year)
