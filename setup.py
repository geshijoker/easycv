from setuptools import setup, find_packages

# Read the contents of requirements.txt
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='easycv',
    version='0.0',
    packages=find_packages(),
    description='A Python package for easily customize cover letters.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ge Shi',
    author_email='geshijoker@gmail.com',
    url='https://github.com/geshijoker/easycv',
    license='MIT',
    install_requires=required_packages,  # Include requirements from requirements.txt
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL-3.0 license',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)