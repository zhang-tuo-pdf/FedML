import argparse
import json
import os
import shutil
import time
import uuid

import requests
from ...core.distributed.communication.mqtt.mqtt_manager import MqttManager

from ...core.distributed.communication.s3.remote_storage import S3Storage

from .device_client_constants import ClientConstants
from ...core.common.singleton import Singleton
from .modelops_configs import ModelOpsConfigs
from .device_model_deployment import get_model_info, run_http_inference_with_lib_http_api
from .device_server_constants import ServerConstants


class FedMLModelObject(object):
    def __init__(self, model_json):
        self.id = model_json["id"]
        self.model_name = model_json["modelName"]
        self.model_type = model_json["modelType"]
        self.model_url = model_json["modelUrl"]
        self.commit_type = model_json["commitType"]
        self.description = model_json["description"]
        self.latest_model_version = model_json["latestModelVersion"]
        self.createTime = model_json["createTime"]
        self.update_time = model_json["updateTime"]
        self.owner = model_json["owner"]
        self.github_link = model_json["githubLink"]
        self.parameters = model_json["parameters"]
        self.model_version = model_json["modelVersion"]
        self.file_name = model_json["fileName"]
        self.is_init = model_json["isInit"]

    def show(self, prefix=""):
        print("{}model name: {}, model id: {}, "
              "model version: {}, model url: {}".format(prefix,
                                                        self.model_name, self.id,
                                                        self.model_version,
                                                        self.model_url))


class FedMLModelList(object):
    def __init__(self, model_list_json):
        self.total_num = model_list_json["total"]
        self.total_page = model_list_json["totalPage"]
        self.page_num = model_list_json["pageNum"]
        self.page_size = model_list_json["pageSize"]
        model_list_data = model_list_json["data"]
        self.model_list = list()
        for model_obj_json in model_list_data:
            model_obj = FedMLModelObject(model_obj_json)
            self.model_list.append(model_obj)
