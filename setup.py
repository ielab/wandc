from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='wandc',
    version='0.0.2',
    packages=find_packages(),
    url='https://github.com/ielab/wandc',
    license='Apache 2.0',
    author='Shengyao Zhuang',
    author_email='s.zhuang@uq.edu.au',
    description='A wandb and codecarbon wrapper that logs water and carbon consumption for your experiments on cloud.',
    python_requires='>=3.8',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "wandb",
        "codecarbon",
    ]
)