"""List your cloud phone instances and query one in detail.

Set VMOS_ACCESS_KEY / VMOS_SECRET_KEY in the environment first.
"""
from vmos import VMOSClient

with VMOSClient() as client:
    # Full account pad list (live-verified)
    pads = client.phone.user_pad_list()
    print("userPadList ->", [p.get("padCode") for p in pads])

    # Paginated list with status flags.
    # NOTE: documented, but the production gateway may still 404 this one
    # (docs ahead of deployment) - prefer user_pad_list() above.
    # page = client.instance.pad_detail(rows=20)

    # Detail for a single instance
    # info = client.phone.pad_info("AC32010180421")
    # print(info["padType"], info["country"])
