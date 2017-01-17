import os, getpass
from subprocess import Popen, PIPE

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

    # def get_kwarg(s, k):
    #     return s.kwargs[k] if s.kwargs.get(k) else None


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