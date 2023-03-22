#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import looker_sdk

if __name__ == "__main__":
    sdk = looker_sdk.init40()

    alerts = sdk.search_alerts(all_owners=True)
    users = sdk.all_users(fields="id, is_disabled")

    disabled_user_ids = [u.get("id") for u in users if u.get("is_disabled")]

    for a in alerts:
        if a.get("owner_id") in disabled_user_ids:
            print(a)
            print()
