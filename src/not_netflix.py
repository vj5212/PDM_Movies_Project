# Main executable for program. Command line based
import argparse

parser = argparse.ArgumentParser(description='Welcome to NotNetflix. Sign up or login!')
parser.add_argument('command', choices=['login', 'collection'])

# write switch for CLI interaction, use argparse
def main():
    pass