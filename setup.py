from setuptools import setup, find_packages

# python setup.py bdist bdist_wheel


with open('README.MD', 'r',encoding='utf-8') as f:
    desp = f.read()
    f.close()

setup(
    name='wxnotify',
    version='0.0.1',
    description='A simple wechat notification',
    long_description=desp,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    author='skygongque',
    author_email='1243650225@qq.com',
    include_package_data=True,
    install_requires=['requests'],
    packages=find_packages()
)
