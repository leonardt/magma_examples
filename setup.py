from setuptools import setup

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

DESCRIPTION = """\
Magma port of https://github.com/ucb-bar/chisel-tutorial
"""

setup(
    name='magma_examples',
    version='0.0.1',
    description=DESCRIPTION,
    scripts=[],
    packages=[
        "magma_examples",
    ],
    install_requires=[
        "magma-lang",
        "mantle",
        "fault"
    ],
    license='BSD License',
    url='https://github.com/leonardt/magma_examples',
    author='Leonard Truong',
    author_email='lenny@cs.stanford.edu',
    python_requires='>=3.8',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown"
)
