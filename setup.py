from setuptools import setup
from djgpa import VERSION


setup(
    name='django-googleplay-api',
    version=".".join(map(str, VERSION)),
    description='Google Play API, with configuration on Django.',
    keywords="django googleplay api",
    long_description=open('README.rst').read(),
    author="GoTLiuM InSPiRiT",
    author_email='gotlium@gmail.com',
    url='http://github.com/gotlium/django-googleplay-api',
    packages=['djgpa'],
    include_package_data=True,
    install_requires=[
        'setuptools', 'gdata', 'django', 'django-preferences', 'protobuf'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
