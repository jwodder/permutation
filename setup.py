import errno
from   os.path    import dirname, join
import re
from   setuptools import setup

with open(join(dirname(__file__), 'permutation.py')) as fp:
    for line in fp:
        m = re.search(r'^\s*__version__\s*=\s*([\'"])([^\'"]+)\1\s*$', line)
        if m:
            version = m.group(2)
            break
    else:
        raise RuntimeError('Unable to find own __version__ string')

try:
    with open(join(dirname(__file__), 'README.rst')) as fp:
        long_desc = fp.read()
except EnvironmentError as e:
    if e.errno == errno.ENOENT:
        long_desc = None
    else:
        raise

setup(
    name='permutation',
    version=version,
    py_modules=['permutation'],
    license='MIT',
    author='John Thorvald Wodder II',
    author_email='permutation@varonathe.org',
    ###keywords='',
    description='Permutations of finitely many positive integers',
    long_description=long_desc,
    url='https://github.com/jwodder/permutation',

    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',

    install_requires=[],

    classifiers=[
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        'License :: OSI Approved :: MIT License',

        ###
    ],
)
