import sys
from fabric.api import run, env, cd, prefix, task

DB_COMMANDS = {
    'mysql': {
        'create': 'mysql -uroot -e "drop database if exists {};"',
        'drop': 'mysql -uroot -e "drop database if exists {};"'},
    'postgresql': {
        'create': 'createdb {};"',
        'drop': 'dropdb {};"'}
}

env.apps = 'web'
env.prefix = 'source env/bin/activate'
env.user = 'webmaster'


@task
def test():
    env.hosts = ['cdn.com']
    env.path = '/home/webmaster/apps/cdn'
    env.branch = 'master'
    env.db_name = 'cdn'
    env.db_type = 'postgresql'
    env.sys_command = './app.py'

if not 'prod' in sys.argv:
    test()


@task
def prod():
    env.hosts = ['example.com']
    env.path = '/home/webmaster/apps/cdn'
    env.branch = 'stable'
    env.db_name = 'cdn'
    env.db_type = 'postgresql'
    env.sys_command = './app.py'


@task
def manage(command):
    with cd(env.path), prefix(env.prefix):
        run('python manage.py {}'.format(command))


@task
def update():
    with cd(env.path):
        run('git pull origin {}'.format(env.branch))
        run('find . -name "*.pyc" -exec rm -f {} \;')
        requirements()
        collectstatic()
        restart()


@task
def requirements():
    with cd(env.path), prefix(env.prefix):
        run('pip install --exists-action=s -r requirements.txt')


@task
def db():
    dropdb()
    createdb()
    syncdb()
    migrate()
    loaddata()


@task
def dropdb():
    run(DB_COMMANDS[env.db_type]['drop'].format(env.db_name))


@task
def createdb():
    run(DB_COMMANDS[env.db_type]['create'].format(env.db_name))


@task
def syncdb():
    manage('syncdb --noinput -v 0')


@task
def migrate():
    manage('migrate -v 0')


@task
def loaddata():
    manage('filldb')


@task
def collectstatic():
    manage('collectstatic --noinput')


@task
def restart():
    with cd(env.path), prefix(env.prefix):
        run('{} restart {}'.format(env.sys_command, env.apps))


@task
def start():
    with cd(env.path), prefix(env.prefix):
        run('{} start {}'.format(env.sys_command, env.apps))


@task
def stop():
    with cd(env.path), prefix(env.prefix):
        run('{} stop {}'.format(env.sys_command, env.apps))


@task
def tail(app):
    with cd(env.path), prefix(env.prefix):
        run('{} tail -f {}'.format(env.sys_command, app))


@task
def status():
    with cd(env.path), prefix(env.prefix):
        run('{} status {}'.format(env.sys_command, env.apps))
