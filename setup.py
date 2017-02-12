import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = [
    'django>=1.9,<1.10',
    'psycopg2>=2.6,<2.7',
    'django-grappelli>=2.8,<2.9',
    'django-countries>=4.0,<4.1',
    'django-braces>=1.9,<1.10',
    'djangorestframework>=3.3,<3.4',
    'django-rest-swagger>=0.3,<0.4',
    'django-filter>=0.11,<0.12',
    'django-extensions>=1.7,<1.8',
    'django-haystack>=2.5,<2.6',
    'django-mptt>=0.8,<0.9',
    'django-tables2>=1.0,<1.1',
    'django-registration>=2.0,<2.1',
    'django-crispy-forms>=1.6,<1.7',
    'whoosh>=2.7,<2.8',
    'pyisbn>=1.0,<1.1',
    'requests>=2.9,<3.0',
]

setup(
    name='oils',
    version='0.0.1',
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    license='MIT License',  # example license
    description='Integrated Library Apps',
    long_description=README,
    url='https://github.com/9gix/oils/',
    author='Eugene',
    author_email='yeo.eugene.oey@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
