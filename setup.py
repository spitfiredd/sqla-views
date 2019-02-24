import glob
import shutil
import os
from setuptools import setup, find_packages, Command


class CleanCommand(Command):
    '''clean up files created by running python setup.py sdists
    also cleans .pyc type files

    '''

    user_options = [("all", "a", "")]

    def initialize_options(self):
        self.all = True
        self._clean_me = []
        self._clean_trees = []
        self._clean_exclude = []
        self._base_path = os.path.abspath(os.path.dirname(__file__))

        for root, dirs, files in os.walk(self._base_path):
            for f in files:
                filepath = os.path.join(root, f)
                if filepath in self._clean_exclude:
                    continue

                if os.path.splitext(f)[-1] in ('.pyc', '.so', '.o', '.pyo',
                                               '.pyd', '.c', '.orig'):
                    self._clean_me.append(filepath)
            for d in dirs:
                if d == '__pycache__':
                    self._clean_trees.append(os.path.join(root, d))

        for d in ('build', 'dist', '*.egg-info'):
            if d == '*.egg-info':
                for i in glob.glob('*.egg-info'):
                    if os.path.exists(i):
                        self._clean_trees.append(i)
            elif os.path.exists(d):
                self._clean_trees.append(d)

    def finalize_options(self):
        pass

    def run(self):
        for clean_me in self._clean_me:
            try:
                os.unlink(clean_me)
            except Exception:
                pass
        for clean_tree in self._clean_trees:
            try:
                shutil.rmtree(clean_tree)
            except Exception:
                pass


setup(
    name='sqla-views',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/spitfiredd/sqla-views.git',
    author='Daniel Donovan',
    author_email='spitfiredd@gmail.com',
    include_package_data=True,
    install_requires=[
        'sqlalchemy',
    ],
    cmdclass={'clean': CleanCommand},
)
