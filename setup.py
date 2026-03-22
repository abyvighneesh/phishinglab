from setuptools import setup, find_packages

setup(
    name='phishlab',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'flask==3.0.0',
        'Werkzeug==3.0.1',
        'requests==2.31.0',
        'beautifulsoup4==4.12.2',
        'python-whois==0.8.0',
        'tldextract==5.1.1',
        'Flask-SQLAlchemy==3.0.5',
        'Flask-Login==0.6.3',
        'reportlab==4.0.4',
        'python-dateutil==2.8.2',
        'gunicorn==21.2.0',
        'python-dotenv==1.0.0',
    ],
    python_requires='>=3.11',
)
