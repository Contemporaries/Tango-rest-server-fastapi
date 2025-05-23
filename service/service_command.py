# Author: HuangLi
# E-Mail: lihuang@ihep.ac.cn
# Version: 1.0.0
# Date: 3/27/2025

from tango import DeviceProxy
from config.log_config import get_logger
from exception.global_exception import GlobalException
from model.request_models import ResponseModel
from enums.enum_response import Code, Message, MCPPrompt
from tools.tool_dev_status import check_dev
from service.service_info import __get_device_command_list

logger = get_logger(__name__)


def get_command_list(device_name: str):
    """
    Get the command list of a device.

    :param device_name: The name of the device.
    :return: The command list of the device.
    """
    device_proxy = DeviceProxy(device_name)
    check_dev(device_name)
    return __get_device_command_list(device_proxy=device_proxy)


def execute_command(device_name: str, command_name: str, value: any):
    """
    Execute a command of a device.

    :param device_name: The name of the device.
    :param command_name: The name of the command.
    :param value: The value of the command.
    """
    try:
        logger.info(f"Executing command {command_name} of device {device_name}")
        device_proxy = DeviceProxy(device_name)
        check_dev(device_name)
        if value is "":
            value = None
        logger.info(f"Device {device_name} is checked")
        device_proxy.command_inout(command_name, value)
        return ResponseModel(
            code=Code.SUCCESS.value,
            success=True,
            message=Message.SUCCESS.value,
            data=None,
        )
    except Exception as e:
        logger.error(
            f"Error executing command {command_name} of device {device_name}: {e}"
        )
        raise GlobalException(MCPPrompt.NOT_FOUND_COMMAND.name, str(e))


def init_device(device_name: str):
    """
    Initialize a device.

    :param device_name: The name of the device.
    """
    try:
        logger.info(f"Initializing device {device_name}")
        device_proxy = DeviceProxy(device_name)
        check_dev(device_name)
        logger.info(f"Device {device_name} is checked")
        device_proxy.command_inout("init")
        return ResponseModel(
            code=Code.SUCCESS.value,
            success=True,
            message=Message.SUCCESS.value,
            data=None,
        )
    except Exception as e:
        logger.error(f"Error initializing device {device_name}: {e}")
        raise GlobalException(MCPPrompt.NOT_FOUND_DEVICE.name, str(e))
