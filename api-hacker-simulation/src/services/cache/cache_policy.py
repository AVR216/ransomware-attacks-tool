from enum import Enum

class CachePolicyEnumType(Enum):
    """Cache policies"""
    STATIC = 'static'
    PARAMETERIZED = 'parameterized'
    METADATA = 'metadata'
