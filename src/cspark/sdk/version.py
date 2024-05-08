from sys import version_info

__all__ = ['__version__', 'sdk_version', 'about']

__version__ = '0.1.0-beta.0'

sdk_version = __version__

sdk_logger = f'CSPARK v{sdk_version}'

platform_info = f'Python {version_info.major}.{version_info.minor}.{version_info.micro}'

about = f'Coherent Spark SDK v{sdk_version} ({platform_info})'

sdk_ua_header = f'agent=cspark-py-sdk/{sdk_version}; env={platform_info}'