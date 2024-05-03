from setuptools import setup, find_packages

setup(
    name='stock-data-query',
    version='0.1',
    packages=find_packages(),
    description='Your package description',
    author='Your Name',
    author_email='your.email@example.com',
    url='http://example.com',
    test_suite='tests',  # 指定測試目錄
    tests_require=['unittest'],  # 測試所需的依賴
    install_requires=[
        'psycopg2-binary',
    ],
)