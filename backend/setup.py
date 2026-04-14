from setuptools import setup, find_packages

setup(
    name='booksage-ai',
    version='2.0.0',
    author='Md Emon Hasan',
    author_email='iconicemon01@gmail.com',
    description='AI-powered book recommendation system using FastAPI and React',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Md-Emon-Hasan/BookSage-AI',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.10',
    install_requires=[
        'fastapi>=0.109.0',
        'uvicorn[standard]>=0.27.0',
        'python-multipart>=0.0.6',
        'pydantic>=2.0.0',
        'httpx>=0.26.0',
        'scikit-learn>=1.4.0',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'scipy>=1.12.0',
        'jinja2>=3.1.0',
        'gunicorn>=21.0.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Framework :: FastAPI',
        'Operating System :: OS Independent',
    ],
)
