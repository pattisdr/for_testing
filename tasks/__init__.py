import invoke
from invoke import Collection

ns = Collection()

current_version = '19.0.3'

def task(*args, **kwargs):
    """Behaves the same way as invoke.task. Adds the task
    to the root namespace.
    """
    if len(args) == 1 and callable(args[0]):
        new_task = invoke.task(args[0])
        ns.add_task(new_task)
        return new_task

    def decorator(f):
        new_task = invoke.task(f, *args, **kwargs)
        ns.add_task(new_task)
        return new_task
    return decorator

@task
def hotfix(ctx, name, finish=False, push=False):
    """Rename hotfix branch to hotfix/<next-patch-version> and optionally
    finish hotfix.
    """
    print('Checking out master to calculate curent version')
    ctx.run('git checkout master')
    latest_version = current_version
    print('Current version is: {}'.format(latest_version))
    major, minor, patch = latest_version.split('.')
    next_patch_version = '.'.join([major, minor, str(int(patch) + 1)])
    print('Bumping to next patch version: {}'.format(next_patch_version))
    print('Renaming branch...')

    new_branch_name = 'hotfix/{}'.format(next_patch_version)
    ctx.run('git checkout {}'.format(name), echo=True)
    ctx.run('git branch -m {}'.format(new_branch_name), echo=True)
    if finish:
        ctx.run('git flow hotfix finish {}'.format(next_patch_version), echo=True, pty=True)
    if push:
        ctx.run('git push --follow-tags origin master', echo=True)
        ctx.run('git push origin develop', echo=True)
