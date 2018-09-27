import os
import xmlrpc.client
from subprocess import Popen, PIPE
import shutil


pypi = xmlrpc.client.ServerProxy('https://pypi.org')

DIRECTORIES_TO_SEARCH_FORM = [
    os.path.join('.'),
    os.path.join('pyforms-web'),
    os.path.join('pyforms-gui'),
    os.path.join('pyforms-terminal'),
]

CURRENT_DIRECTORY = os.getcwd()


Popen(['pip','install','--upgrade','setuptools','wheel','twine']).communicate()

def version_compare(a, b):

    a = a.split('.')
    b = b.split('.')

    for a_value, b_value in zip(a, b):
        a_value = int(a_value)
        b_value = int(b_value)
        
        if a_value>b_value:
            return -1
        elif a_value<b_value:
            return 1

    if len(a)>len(b):
        return -1
    elif len(a)<len(b):
        return 1

    return 0




for dir_name in DIRECTORIES_TO_SEARCH_FORM:
    dir_path = os.path.abspath(dir_name)
    print('---', dir_path)
    if not os.path.isdir(dir_path): continue

    setup_filepath = os.path.join(dir_path, 'setup.py')
    if not os.path.isfile(setup_filepath): continue

    os.chdir(dir_path)

    version = Popen(["python", setup_filepath, '--version'], stdout=PIPE).stdout.read()
    version = version.strip().decode()
    
    package_name = Popen(["python", setup_filepath, '--name'], stdout=PIPE).stdout.read()
    package_name = package_name.strip().decode().replace(' ', '-')

    remote_version = pypi.package_releases(package_name)
    
    print( dir_name, version, remote_version )

    
    if len(remote_version)==0 or version_compare(version, remote_version[0])<0:
        print('UPLOADING PYPI')

        if os.path.isdir('./dist'):
            shutil.rmtree('./dist')
        Popen(['python', 'setup.py', 'sdist', 'bdist_wheel']).communicate()
        Popen(['twine', 'upload', os.path.join('dist','*')]).communicate()

    
    os.chdir(CURRENT_DIRECTORY)



"""




    def get_pypi_distribution(self, name):

        new_version = self.pypi.package_releases(name)
        if not new_version:
            new_version = self.pypi.package_releases(name.capitalize())

        if new_version is None: return new_version

        new_version  = new_version[0]
        all_versions = self.pypi.package_releases(name, True)
        data = self.pypi.release_data(name, new_version)


        return new_version, all_versions, data.get('summary', '')
"""
