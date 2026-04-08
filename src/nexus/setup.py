from setuptools import setup

package_name = 'nexus'

setup(
    name=package_name,
    version='0.1.0',
    packages=[
        package_name,
        f'{package_name}.nodes',
        f'{package_name}.nodes.common',
        f'{package_name}.validation',
    ],
    data_files=[
        ('share/ament_index/resource_index/packages', [f'resource/{package_name}']),
        (f'share/{package_name}', ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='twrappe',
    maintainer_email='twrappe@example.com',
    description='NEXUS system-level AI validation framework',
    license='MIT',
    entry_points={
        'console_scripts': [
            'hil_validator = nexus.validation.hil_validator:main',
        ],
    },
)
