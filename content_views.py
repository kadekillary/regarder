#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import looker_sdk

if __name__ == "__main__":
    sdk = looker_sdk.init40()
    content_views = sdk.search_content_views(all_time=True)

    # content is look and dashboards?

    for c in content_views:
        print(c)
        print()
