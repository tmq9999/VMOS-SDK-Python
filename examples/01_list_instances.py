"""List your cloud phone instances and query one in detail.

Set VMOS_ACCESS_KEY / VMOS_SECRET_KEY in the environment first.
"""
from vmos import VMOSClient

with VMOSClient() as client:
    # Paginated instance list with status flags
    page = client.instance.pad_detail(rows=20)
    print("padDetail ->", page)

    # Full account pad list
    pads = client.phone.user_pad_list()
    print("userPadList ->", pads)

    # Detail for a single instance
    # info = client.phone.pad_info("AC32010180421")
    # print(info["padType"], info["country"])
