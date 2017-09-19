from ebay.utils import set_config_file
from ebay.shopping import FindHalfProducts

set_config_file("ZiaoChen-SKUInfoR-SBX-65d7a0307-0843993d")
print FindHalfProducts("pen","false","10","JSON")
