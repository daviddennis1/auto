import argparse, os, sys
from random import randint
from subprocess import Popen, PIPE
from settings import SETTINGS, TEXT

def args_to_kwargs(args):
    d = {}
    for k,v in args._get_kwargs():
        d[k] = v
    return d

def run_shell_cmd(cmd, silent=False):
    if not silent:
        print('Running: "%s"' % ' '.join(cmd))
    s = Popen(cmd , stdin=PIPE, stdout=PIPE, stderr=PIPE)
    lines = [o for o in s.stdout]
    if lines:
        print('\tRun Command Output:')
        for l in lines:
            print('\t\t'+l.decode('utf-8').replace('\n', ''))
    return lines

class Main:

    def __init__(s, *args, **kwargs):
        # print(kwargs)
        s.args = {}
        for k,v in kwargs.items():
            s.args[k] = v

        s.reset()
        s.create_django_project()

    def reset(s):
        if not s.args.get('reset'):
            return False
        if not s.args.get('name'):
            return False
        s.call('rm -rf %s' % s.args['name'])
        sys.exit()

    def create_django_project(s):
        if not s.args.get('name'):
            return

        s.proj_name = proj_name = s.args['name']
        cmd = 'django-admin startproject %s' % proj_name
        s.call(cmd)
        print('\tCreated Django project: %s' % proj_name)
        s.cd(proj_name)
        s.startapp()
        s.add_app_to_settings()
        #s.migrate()
        s.create_mng_cmd_dir()
        s.create_demo_mng_cmd()
        s.create_models()

    def migrate(s):
        s.call('python manage.py migrate')

    def startapp(s):
        s.app_name = app_name = 'app_' + s.proj_name
        cmd_txt = 'python manage.py startapp %s' % (app_name)
        cmd = cmd_txt.split(' ')
        s.call(cmd)
        print('\tCreated app: %s' % app_name)

    def add_app_to_settings(s):
        settings_file_path = s.get_full_path('/%s/%s/settings.py' % (s.proj_name, s.proj_name))
        new_line = "\t'%s',\n" % s.app_name
        s.insert_in_file(settings_file_path,
                         'django.contrib.staticfiles',
                         new_line)
        print('\tAdded "%s" to INSTALLED_APPS' % s.app_name)

    def insert_in_file(s, file_path, pattern, new_line):
        lines = s.get_lines_from_file(file_path)
        line_number = s.find_line_number(pattern, lines)
        new_lines = s.add_in_list(new_line, line_number+1, lines, one_line=True)
        #print(new_lines[:50])
        s.write_to_file(new_lines, file_path)

    def create_mng_cmd_dir(s):
        s.app_dir = parent_dir = s.get_full_path('%s/%s' % (s.proj_name, s.app_name))
        s.create_module_dir('%s/management' % parent_dir)
        s.mng_cmd_dir = mng_cmd_dir = '%s/management/commands' % parent_dir
        s.create_module_dir(mng_cmd_dir)

    def create_demo_mng_cmd(s):
        demo_mng_cmd_path = '%s/demo.py' % s.mng_cmd_dir
        s.create_file(demo_mng_cmd_path)
        #TODO: from %s.models import
        mngcmd_txt = TEXT['mngcmd_txt']

        s.write_to_file(mngcmd_txt, demo_mng_cmd_path)

    def create_models(s):
        model_path = s.get_full_path('%s/models.py' % (s.app_dir))
        models_txt = TEXT['models']

        lines = s.get_lines_from_file(model_path)
        pattern = 'from django.db import models'
        line_number = s.find_line_number(pattern, lines)

        new_lines = s.add_in_list(models_txt, line_number+1, lines)
        #print(new_lines)
        s.write_to_file(new_lines, model_path)

    def create_module_dir(s, path):
        s.create_dir(path)
        s.create_file('%s/__init__.py' % path)

    def create_dir(s, path):
        s.call('mkdir %s' % path)

    def create_file(s, file_path):
        s.call('touch %s' % file_path)

    def write_to_file(s, content, file_path):
        line_mode = False
        if isinstance(content, list) or isinstance(content, tuple):
            line_mode = True

        file_path = s.get_full_path(file_path)

        tmp_file_path = file_path + '.old'
        if s.file_exists(file_path):
            s.mv(file_path, tmp_file_path, silent=True)

        with open(file_path, 'w') as f:
            if line_mode:
                for line in content:
                    if isinstance(line, list):
                        for l in line:
                            f.write(l+'\n')
                        continue
                    #try:
                    f.write(line)
                    #except:
                    #    print(line)
            else:
                f.write(content)

        s.rm(tmp_file_path, silent=True)

    def add_in_list(s, new_item, num, llist, one_line=False):
        if isinstance(new_item, str) and not one_line:
            new_item = new_item.split('\n')
        llist = llist[:num] + [new_item] + llist[num:]
        return llist

    def get_lines_from_file(s, filename):
        if not s.curr_dir in filename:
            filename = s.curr_dir + filename

        lines = []
        with open(filename, 'r') as f:
            lines = f.readlines()
        return lines

    def get_full_path(s, path):
        if path[0] != '/':
            path = '/' + path
        if not s.curr_dir in path:
            return s.curr_dir + path
        return path

    def find_line_number(s, pattern, lines):
        for i, line in enumerate(lines):
            if pattern in line:
                return i
        return None

    def cd(s, new_dir):
        s.curr_dir = curr_dir = os.getcwd()
        os.chdir(curr_dir + '/%s' % new_dir)
        print('\tChanged directory to: %s' % os.getcwd())

    def mv(s, old_file_path, new_file_path, silent=False):
        s.call('mv %s %s' % (old_file_path, new_file_path), silent=silent)

    def rm(s, file_path, silent=False):
        s.call('rm %s' % file_path, silent=silent)

    def file_exists(s, file_path):
        return os.path.exists(file_path)

    def call(s, cmd, silent=False):
        if isinstance(cmd, str):
            cmd = [c for c in cmd.split(' ') if c != '']

        if not s.args.get('test_run'):
            run_shell_cmd(cmd, silent=silent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name')
    parser.add_argument('--test_run', action='store_true')
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    Main(**args_to_kwargs(args))
