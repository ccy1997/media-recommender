import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='media-recommender',
    version='0.0.1',
    author='Chung Yin Cheung',
    author_email='cxc574@student.bham.ac.uk',
    description='Media Recommender provides recommendation for movies, videos games and books',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://git-teaching.cs.bham.ac.uk/mod-ug-proj-2018/cxc574',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ],
)