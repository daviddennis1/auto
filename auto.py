import argparse, os, sys, getpass
from random import randint
from subprocess import Popen, PIPE
from config import SETTINGS, TEXT


class Util:
    def add_in_list(s, new_item, index, llist, one_line=False, spaces_before=0):
        if isinstance(new_item, str) and not one_line:
            new_item = new_item.split('\n')
        llist = llist[:index] + ['']*spaces_before + [new_item] + llist[index:]

        # Remove extra blank lines
        rev_llist = llist[::-1]
        for line in rev_llist:
            if line == '' or s.str_is_all(line, ' '):
                llist = llist[:-1]
            else:
                break
        return llist

    def log(s, text, tabs=0):
        print('\t'*tabs + text)

    def str_is_all(s, string, pattern):
        for c in string:
            if c != pattern:
                return False
        return True


class OSUtil(Util):
    def __init__(s, *args, **kwargs):
        s.auto_dir = os.getcwd()
        s.curr_user = getpass.getuser()

    def get_full_path(s, path):
        if path[0] != '/':
            path = '/' + path
        if not s.auto_dir in path:
            new_path = s.auto_dir + path
            return new_path
        return path

    def is_a_path(s, string):
        if s.auto_dir in string:
            return True
        if '/' in string:
            return True
        return False

    def run_shell_cmd(s, cmd, silent=False):
        if not silent:
            print('\tRunning: "%s"' % ' '.join(cmd))
        #print(cmd, '!!')
        output, error = Popen(cmd , stdout=PIPE, stderr=PIPE).communicate()
        if error:
            print('PSQL ERROR:')
            for el in error.decode('utf-8').split('\n'):
                if el:
                    print('\t'+el)
        lines = output.decode('utf-8').split('\n')
        if lines and lines != ['']:
            print('\tRun Command Output:')
            for l in lines:
                print('\t\t'+l.replace('\n', ''))
        return lines

    def mv(s, old_file_path, new_file_path, silent=False):
        s.call('mv %s %s' % (old_file_path, new_file_path), silent=silent)

    def rm(s, file_path, silent=False):
        s.call('rm %s' % file_path, silent=silent)

    def call(s, cmd, silent=False):
        if isinstance(cmd, str):
            cmd = [c for c in cmd.split(' ') if c != '']

        #if not s.args.get('test_run'): # TODO: <--
        s.run_shell_cmd(cmd, silent=silent)

    def file_exists(s, file_path):
        return os.path.exists(file_path)


class DBUtil: # (OSUtil)
    def run_sql(s, sql_cmd):
        db_cmd = ['psql', '-c', sql_cmd]
        s.run_shell_cmd(db_cmd)


class File(OSUtil):
    def __init__(s, *args, **kwargs):
        super(File, s).__init__(*args, **kwargs)
        file_path = args[0]
        content = args[1] if len(args) > 1 else None

        s.file_path = s.get_full_path(file_path)

        s.load_file_contents(content)

    def load_file_contents(s, content=None):
        if content:
            s.content = content
        else:
            with open(s.file_path) as f:
                s.content = f.read()
        s.lines = s.content.split('\n')

    def insert_in_file(s, pattern, new_line, spaces_before=0):
        line_number = s.find_line_number(pattern)
        new_lines = s.add_in_list(new_line, line_number, s.lines, one_line=True,
                                  spaces_before=spaces_before)
        s.write_to_file(new_lines)

    def add_to_line(s, pattern, new_line):
        new_lines = []
        for line in s.lines:
            if pattern in line:
                line += new_line
            new_lines.append(line)
        s.write_to_file(new_lines)

    def write_to_file(s, content, file_path=None):
        if file_path:
            file_path = s.get_full_path(file_path)
        else:
            file_path = s.file_path

        line_mode = False
        if isinstance(content, list) or isinstance(content, tuple):
            line_mode = True

        tmp_file_path = s.archive_file(file_path)

        with open(s.file_path, 'w') as f:
            if line_mode:
                for line in content:
                    if isinstance(line, list):
                        for l in line:
                            f.write(l+'\n')
                        continue
                    f.write(line+'\n')
            else:
                f.write(content)

        s.load_file_contents()

        s.rm(tmp_file_path, silent=True)

    def remove_lines(s, beg_pattern, end_pattern=None):
        beg_line_num = s.find_line_number(beg_pattern)
        if end_pattern:
            end_line_num = s.find_line_number(end_pattern, after=beg_line_num)
        else:
            end_line_num = None
        #print(beg_pattern,  beg_line_num)
        s.remove_line_nums(beg_line_num, end_line_num)

    def remove_line_nums(s, beg_num, end_num=None):
        # print(beg_num, end_num, '>>')
        # print(s.lines[:100])
        # print(1)
        if end_num:
            new_lines = s.lines[:beg_num-1] + s.lines[end_num:]
        else:
            new_lines = s.lines[:beg_num-1] + s.lines[beg_num:]
        # print(new_lines[:100])
        # print(2)
        s.write_to_file(new_lines)

    def find_line_number(s, pattern, after=0):
        line_area = s.lines[after:]
        # print(pattern, after)
        for i, line in enumerate(line_area, start=1):
            if pattern in line:
                return i + after
        return None

    def archive_file(s, file_path):
        tmp_file_path = file_path + '.old'
        if s.file_exists(file_path):
            s.mv(file_path, tmp_file_path, silent=True)
        return tmp_file_path

    def file_exists(s, file_path):
        if os.path.exists(file_path):
            return True
        return False

    # def get_file_obj(s, file_pointer):
    #     file_obj = None
    #     if s.is_a_path(file_pointer):
    #         file_path = file_pointer
    #         file_obj = File(file_path)
    #     elif isinstance(file_pointer, File):
    #         file_obj = file_pointer
    #     return file_obj


class Main(OSUtil, DBUtil):

    def __init__(s, *args, **kwargs):
        # print(kwargs)
        s.args = {}
        for k,v in kwargs.items():
            s.args[k] = v

        super(Main, s).__init__(*args, **kwargs)
        s.setup()

    def setup(s):
        s.reset()

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
        s.proj_dir = s.get_full_path(s.proj_name)
        s.app_name = app_name = 'app_' + s.proj_name
        s.app_dir = s.get_full_path('%s/%s' % (s.proj_name, s.app_name))

        cmd = 'django-admin startproject %s' % proj_name
        s.call(cmd)
        s.log('Created Django project: %s' % proj_name)
        s.cd(proj_name)
        s.startapp()
        s.add_app_to_settings()
        s.add_db_to_settings()
        s.create_models()
        # s.migrate()
        s.add_templates()
        s.add_views()
        s.add_urls()
        #s.create_mng_cmd_dir()
        #s.create_demo_mng_cmd()
        # s.log('Created Management Command Directory + Stub command')
        # s.add_models_to_admin()

    def migrate(s):
        create_db_cmd = 'CREATE DATABASE %s;' % s.proj_name
        s.run_sql(create_db_cmd)

        s.cd(s.proj_dir)
        s.call('python manage.py makemigrations')
        s.call('python manage.py migrate')

    def startapp(s):
        cmd_txt = 'python manage.py startapp %s' % (s.app_name)
        cmd = cmd_txt.split(' ')
        s.call(cmd)
        s.log('Created app: %s' % s.app_name)

    def add_app_to_settings(s):
        #settings_file_path = s.get_full_path('/%s/%s/settings.py' % (s.proj_name, s.proj_name))
        settings_file_path = '%s/settings.py' % (s.proj_name)
        s.settings_file = settings_file = s.get_file(settings_file_path)

        new_line = "\t'%s'," % s.app_name
        settings_file.insert_in_file('django.contrib.staticfiles', new_line)
        #s.log('Added "%s" to INSTALLED_APPS' % s.app_name)

    def add_db_to_settings(s):
        s.db_type = db_type = SETTINGS.get('database')
        if db_type not in ('mysql', 'postgres'):
            return
        db_settings_txt = TEXT['%s_db_settings' % db_type]
        db_settings_txt = db_settings_txt % (s.proj_name, s.curr_user)

        s.settings_file.remove_lines("'default': {", '}')
        s.settings_file.insert_in_file('DATABASES = {', db_settings_txt)

    def add_templates(s):
        template_dir = s.get_full_path('%s/templates' % s.app_dir)
        s.create_dir(template_dir, silent=True)
        template_app_dir = template_dir + '/' +  s.app_name
        s.create_dir(template_app_dir, silent=True)
        s.index_html_file = index_html_file = s.create_file(template_app_dir + '/index.html')
        index_file_txt = TEXT['index_file_txt']
        index_html_file.write_to_file(index_file_txt)

    def add_views(s):
        s.views_file = views_file = s.get_file('%s/views.py' % s.app_dir)
        view_txt = TEXT['view_txt']
        view_txt = view_txt % (s.models[0], s.app_name)
        views_file.insert_in_file('from django.shortcuts import render', view_txt)
        views_file.remove_lines('# Create your views here.')
        views_file.insert_in_file('from django.http import HttpResponse',
                                  s.import_models_str, spaces_before=1)

    def add_urls(s):
        # project urls
        s.proj_urls_file = urls_file = s.get_file('%s/urls.py' % s.proj_name)
        urls_file.add_to_line('from django.conf.urls import url', ', include')
        url_line = TEXT['proj_url_txt'] % (s.proj_name, s.app_name)
        urls_file.insert_in_file('admin.site.urls', url_line)

        # app_urls
        s.app_urls_file = app_urls_file = s.create_file('%s/urls.py' % s.app_name, silent=True)
        urls_txt = TEXT['app_url_txt']
        app_urls_file.write_to_file(urls_txt)

    def create_mng_cmd_dir(s, silent=True):
        s.app_dir = parent_dir = s.get_full_path('%s/%s' % (s.proj_name, s.app_name))
        s.create_module_dir('%s/management' % parent_dir, silent=silent)
        s.mng_cmd_dir = mng_cmd_dir = '%s/management/commands' % parent_dir
        s.create_module_dir(mng_cmd_dir, silent=silent)

    def create_demo_mng_cmd(s, silent=True):
        demo_mng_cmd_path = '%s/stub.py' % s.mng_cmd_dir
        mng_cmd_file = s.create_file(demo_mng_cmd_path, silent=True)
        #TODO: from %s.models import
        mngcmd_txt = TEXT['mngcmd_txt']

        mng_cmd_file.write_to_file(mngcmd_txt)#, demo_mng_cmd_path)

    def create_models(s):
        # TODO: Add BaseModel
        s.models_file = models_file = File('%s/models.py' % (s.app_dir))
        models_txt = TEXT['models']
        s.models = models = TEXT['example_models']
        s.import_models_str = 'from %s.models import %s\n\n' % (s.app_name, ', '.join(s.models))
        models_txt = models_txt % models[0]

        models_file.insert_in_file('# Create your models here.', models_txt)
        models_file.remove_lines('# Create your models here.')

    def add_models_to_admin(s):
        s.admin_file = admin_file = File('%s/admin.py' % s.app_dir)
        admin_txt = s.import_models_str[:]
        for model_name in s.models:
            admin_txt += 'admin.site.register(%s)' % model_name
        admin_file.insert_in_file('# Register your models here.', admin_txt)
        admin_file.remove_lines('# Register your models here.')

    def get_file(s, file_path):
        f = File(file_path)
        return f

    def create_module_dir(s, path, silent=False):
        s.create_dir(path, silent=silent)
        s.create_file('%s/__init__.py' % path, silent=silent)

    def create_dir(s, path, silent=False):
        s.call('mkdir %s' % path, silent=silent)

    def create_file(s, file_path, silent=False):
        s.call('touch %s' % file_path, silent=silent)
        return File(file_path)

    def get_lines_from_file(s, filename):
        if not s.curr_dir in filename:
            filename = s.curr_dir + filename

        lines = []
        with open(filename, 'r') as f:
            lines = f.readlines()
        return lines

    def cd(s, new_dir):
        if '/' not in new_dir:
            s.curr_dir = curr_dir = os.getcwd()
            os.chdir(curr_dir + '/%s' % new_dir)
        s.log('Changed directory to: %s' % os.getcwd(), tabs=1)


def args_to_kwargs(args):
    d = {}
    for k,v in args._get_kwargs():
        d[k] = v
    return d

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name')
    parser.add_argument('--test_run', action='store_true')
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    m = Main(**args_to_kwargs(args))
    m.create_django_project()
