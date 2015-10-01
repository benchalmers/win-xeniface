import sys
import git
import repo

def main(argv):
    git.mirror(repo.upstream, repo.internal_push)

if __name__ == '__main__':
    main(sys.argv)
