import os
import subprocess
import datetime
import ntpath


class GitUtil:
    def __init__(self, path):
        self.BASE_DIR = path
        self.files = list()
        for root, directories, filenames in os.walk(self.BASE_DIR):
            if '.' in root:
                continue
            for filename in filenames:
                self.files.append(os.path.join(root, filename))

# BASE_DIR = path()#os.path.dirname(os.path.abspath(__file__))

# files = [os.path.join(BASE_DIR, f) for f in os.listdir(BASE_DIR)]  # list of the files in BASE directory

# print("total files: ",len(files))

    def path_leaf(self, path):
        ''' return filename from path '''
        return ntpath.basename(path)

    def _run(self, *args):
        '''core function'''
        print(list(args))
        os.chdir(self.BASE_DIR)
        try:
            return subprocess.check_call(['git'] + list(args))
        except:
            return 0

    def commit(self, mylist):
        ''' commit function '''
        file_names = [self.path_leaf(l) for l in mylist]
        message = str(",".join(file_names))[:100]
        commit_message = message

        self._run("commit", "-m", commit_message)
        self._run("push", "-u", "origin", "master")

    def _filter_on_size(self, size=0):
        """core function to filter files to be added, take size in bytes"""
        # files_list = [file for file in f if os.path.getsize(file) > size]
        f = self.files
        file_list = list()
        date_limit = datetime.datetime.now() - datetime.timedelta(weeks=1)
        for file in f:
            try:
                last_mod_date = datetime.datetime.fromtimestamp(
                    os.path.getmtime(file))
                if last_mod_date > date_limit and os.path.getsize(file) < size:
                    # _run("add",file)
                    file_list.append(file)
            except:
                continue

        # print(files_list)

        return file_list


    def add(self,size=10000000):
        if size == 0:
            self._run("add", ".")
        else:
            files = self._filter_on_size(size)
            self._run("add", *files)
            return files
    def test(self):
        print('class loaded successfully \n','path:',self.BASE_DIR)
        

def main():
    g = GitUtil(os.path.dirname(os.path.abspath(__file__)))
    print("adding files")
    files = g.add()  # change the number to filter files on size , size in bytes
    print('committing files')
    g.commit(files)
    print('done')


if __name__ == '__main__':
    main()
