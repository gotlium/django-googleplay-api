from setuptools import setup, find_packages
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
    packages=find_packages(exclude=['demo']),
    package_data={'djgpa': [
        'android-checkin/*.jar',
        'static/djgpa/admin/js/djgpa.js',
    ]},
    include_package_data=True,
    install_requires=[
        'gdata',
        'django-preferences',
        'protobuf',
        'pycurl',
        'lxml',
        'grab',
    ],
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
