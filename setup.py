from setuptools import setup, find_packages
setup(
    name='cli_code',
    version='0.0.3',
    packages=find_packages(),
    entry_points={
        'console_scripts':
            [
                'cli_convert_jupyter   = cli_code.cli_convert_ipynb:main',
                'cli_repo_install      = cli_code.cli_env_autoinstall:main',
                'cli_github_search     = cli_code.cli_github_search:main',
                'cli_env_module_parser = cli_code.cli_module_parser:main',
                'cli_download          = cli_code.cli_download:main',
                'cli_repo_check        = cli_code.cli_repo_check:main',
                'cli_conda_merge       = cli_code.cli_conda_merge:main',
                'cli_doc               = cli_code.cli_doc_auto.main:main',
                'cli_json          = cli_code.cli_json:main',
                'cli_format        = cli_code.cli_format:main',

            ],
    },
    license='MIT',
    description='A simple commandline utility for python scripts.',
    keywords=['PYTHON', 'CLI', 'UTILITIES'],
    install_requires=[
        'pypandoc',
        'nbformat',
        'nbconvert',
        'tqdm',
        'beautifulsoup4',
        'requests',
        'lxml',
        'simplejson',
        'pandas',
        'pyyaml'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)

# author='YOUR NAME',
# author_email='your.email@domain.com',
# url='https://github.com/xCodeR01/cli_convert_ipynb',
# download_url='https://github.com/xCodeR01/cli_convert_ipynb/archive/v_01.tar.gz',
# scripts=['cli_code/cli_convert_ipynb.py'],
