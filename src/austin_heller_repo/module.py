from abc import ABC, abstractmethod


class ModuleMessage():

	def __init__(self, *, queue_guid: str, transmission_json: dict, source_device_guid: str, source_device_instance_guid: str, destination_device_guid: str, destination_device_instance_guid: str):

		self.__queue_guid = queue_guid
		self.__transmission_json = transmission_json
		self.__source_device_guid = source_device_guid
		self.__source_device_instance_guid = source_device_instance_guid
		self.__destination_device_guid = destination_device_guid
		self.__destination_device_instance_guid = destination_device_instance_guid

	def get_queue_guid(self) -> str:
		return self.__queue_guid

	def get_transmission_json(self) -> dict:
		return self.__transmission_json

	def get_source_device_guid(self) -> str:
		return self.__source_device_guid

	def get_source_device_instance_guid(self) -> str:
		return self.__source_device_instance_guid

	def get_destination_device_guid(self) -> str:
		return self.__destination_device_guid

	def get_destination_device_instance_guid(self) -> str:
		return self.__destination_device_instance_guid


class Module(ABC):

	def __init__(self, *, send_message_method, get_devices_by_purpose_method):

		self.__send_message_method = send_message_method
		self.__get_devices_by_purpose_method = get_devices_by_purpose_method

	def send(self, *, module_message: ModuleMessage):
		self.__send_message_method(module_message)

	def _get_devices_by_purpose(self, *, purpose_guid: str):
		return self.__get_devices_by_purpose_method(purpose_guid)

	@abstractmethod
	def receive(self, *, module_message: ModuleMessage):
		raise NotImplementedError()

	@abstractmethod
	def start(self):
		raise NotImplementedError()

	@abstractmethod
	def stop(self):
		raise NotImplementedError()

	@abstractmethod
	def get_purpose_guid(self) -> str:
		raise NotImplementedError()


class ModuleReference():

	def __init__(self):

		self.__module = None

	def set(self, *, module: Module):
		self.__module = module

	def get(self) -> Module:
		return self.__module
