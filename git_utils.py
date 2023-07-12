import subprocess

def clone_github_repo(github_url, local_dir):
    try:
        subprocess.check_call(['git', 'clone', github_url, local_dir])
        return True
    except subprocess.CalledProcessError as e:
        print(f'Error cloning {github_url} to {local_dir}: {e.output}')
        return False
