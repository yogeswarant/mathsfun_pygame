import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="maths-speed-test", # Replace with your own username
    version="0.0.1",
    author="Yogeswaran Thulasidoss",
    author_email="yogeeswaran@gmail.com",
    description="Maths speed test using PyGame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yogeswarant/mathsfun_pygame",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pygame', 'mathsfunlib'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['maths-speed-test=src.main:main'],
    }
)