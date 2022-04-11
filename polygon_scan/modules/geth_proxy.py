from .base import Base


class GethProxy(Base):
    """Helper class container for getproxy module's API calls"""

    params = {"module": "proxy"}
