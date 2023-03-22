#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import namedtuple

import looker_sdk

look_fields = ["id", "title", "user_id", "created_at", "last_accessed_at", "view_count"]

Look = namedtuple("Look", look_fields)

if __name__ == "__main__":
    sdk = looker_sdk.init40()

    users = sdk.all_users(fields="id, is_disabled")
    looks = sdk.all_looks()

    disabled_user_ids = [u.get("id") for u in users if u.get("is_disabled")]
    disabled_looks_count = 0

    for l in looks:
        # delete look if user is disabled
        # delete look if last_accessed_at is more than 30 days ago
        # delete look if view_count low
        look = Look._make(l.get(key) for key in look_fields)
        print(look)
        print()
        # sdk.delete_look(look.id)
