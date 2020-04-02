import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pubsub-ce-send",
    version="0.1.0",
    author="Alberto Degli Esposti",
    author_email="alberto@airspot.tech",
    description="Send cloudevents via pubsub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="python pubsub cloudevent",
    url="https://github.com/ade8850/pubsub-ce-send.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License"
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'pubsub-ce-send = pubsub_ce_send:main',
        ],
    },
    install_requires=[
        'google-cloud-pubsub',
    ],
    tests_require=[
        'pytest==5.3.5',
    ],
    python_requires='>=3.6',
)
