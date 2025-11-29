from setuptools import setup, find_packages

setup(
    name='claude_optimizer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'google-generativeai',
        'numpy',
        'pandas',
        'scipy', # Added scipy for Latin Hypercube Sampling
        'scikit-optimize', # Added for Bayesian Optimization
    ],
    entry_points={
        'console_scripts': [
            'claude-optimize=claude_optimizer.optimizer:optimize_wavelength_cli',
        ],
    },
    author='Your Name', # Replace with your name
    author_email='your.email@example.com', # Replace with your email
    description='A package to optimize Claude-light RGB values using Gemini API or LHS',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/claude_optimizer', # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
