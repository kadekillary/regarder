#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import string
import json
from os import remove, mkdir

import looker_sdk
import jsonpickle

#  import boto3

#  S3_BUCKET = ""
#  S3_KEY = ""

FOLDERNAME = "disabled_schedules"

if __name__ == "__main__":
    sdk = looker_sdk.init40()
    #  s3 = boto3.client("s3")

    users = sdk.all_users(fields="id, is_disabled")
    schedules = sdk.all_scheduled_plans(all_users=True)

    disabled_user_ids = [u.get("id") for u in users if u.get("is_disabled")]
    disabled_schedule_count = 0

    mkdir(FOLDERNAME)

    for s in schedules:
        if s.get("user_id") in disabled_user_ids:
            # need to be an admin to delete other users schedules
            sched_id = s["scheduled_plan_destination"][0].scheduled_plan_id
            # create filename
            name = (
                s.name.lower()
                .translate(str.maketrans("", "", string.punctuation))
                .replace(" ", "_")
                .replace("__", "_")
            )
            created = s.created_at.date().isoformat()
            user = s.user.display_name.lower().replace(" ", "_")

            filename = f"{FOLDERNAME}/{name}__on__{created}__by__{user}.json"

            # need jsonnpickle since sdk returns a complex object
            # not json serializable
            s_to_json = jsonpickle.encode(s, unpicklable=False)

            print(f"writing: {filename}")

            with open(filename, "w") as f:
                json.dump(s_to_json, f)

            # log schedule to s3
            #  s3.put_object(Body=s_to_json, Bucket=S3_BUCKET, Key=f"{S3_KEY}/{filename}")

            remove(filename)

            print(f"deleting schedule #{disabled_schedule_count}: {s.name}")
            try:
                sdk.delete_scheduled_plan(sched_id)
            except Exception as e:
                print(f"error deleting schedule: {e}")
            disabled_schedule_count += 1
