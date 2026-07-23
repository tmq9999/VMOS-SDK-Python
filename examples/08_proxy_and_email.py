"""Proxy services and email verification examples."""
from vmos import VMOSClient

with VMOSClient() as client:
    # --- Dynamic proxy ---
    regions = client.dynamic_proxy.get_dynamic_proxy_region()
    print("dynamic proxy regions:", regions)
    balance = client.dynamic_proxy.query_current_traffic_balance()
    print("traffic balance:", balance)

    # --- Static residential proxy ---
    goods = client.static_proxy.proxy_good_list()
    print("static proxy goods:", goods)

    # --- Email verification service ---
    services = client.email.get_email_service_list()
    print("email services:", services)
