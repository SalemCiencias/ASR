from setuptools import setup

package_name = 'escucha'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='eragond',
    maintainer_email='eragond@ciencias.unam.mx',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'boton = escucha.nodo_escucha:main',
            'cliente = escucha.cliente_escucha:main',
        ],
    },
)
