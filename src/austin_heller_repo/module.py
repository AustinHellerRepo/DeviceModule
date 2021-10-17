from austin_heller_repo.socket import Semaphore


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


class Module():

	def __init__(self, *, device_guid: str, send_message_method, get_devices_by_purpose_method, on_ready_method):

		self.__device_guid = device_guid
		self.__send_message_method = send_message_method
		self.__get_devices_by_purpose_method = get_devices_by_purpose_method
		self.__on_ready_method = on_ready_method

		self.__device_instance_guid = None  # type: str
		self.__block_send_until_ready_semaphore = Semaphore()
		self.__block_receive_until_ready_semaphore = Semaphore()

		self.__initialize()

	def __initialize(self):

		self.__block_send_until_ready_semaphore.acquire()
		self.__block_receive_until_ready_semaphore.acquire()

	def _send(self, *, module_message: ModuleMessage):
		self.__block_send_until_ready_semaphore.acquire()
		self.__block_send_until_ready_semaphore.release()
		self.__send_message_method(module_message)

	def _get_devices_by_purpose(self, *, purpose_guid: str):
		return self.__get_devices_by_purpose_method(purpose_guid)

	def _get_device_guid(self) -> str:
		return self.__device_guid

	def _get_device_instance_guid(self) -> str:
		if self.__device_instance_guid is None:
			raise Exception(f"Must first signal ready by calling _ready method.")
		return self.__device_instance_guid

	def _ready(self):
		if self.__device_instance_guid is not None:
			raise Exception(f"Already marked as ready")
		else:
			self.__device_instance_guid = self.__on_ready_method()
			self.__block_send_until_ready_semaphore.release()

	# TODO override
	def _receive(self, *, module_message: ModuleMessage):
		raise NotImplementedError()

	def receive(self, *, module_message: ModuleMessage):
		self.__block_receive_until_ready_semaphore.acquire()
		self.__block_receive_until_ready_semaphore.release()
		self._receive(
			module_message=module_message
		)

	# TODO override
	def start(self):
		raise NotImplementedError()

	# TODO override
	def stop(self):
		raise NotImplementedError()

	# TODO override
	def get_purpose_guid(self) -> str:
		raise NotImplementedError()


class ModuleReference():

	def __init__(self):

		self.__module = None

	def set(self, *, module: Module):
		self.__module = module

	def get(self) -> Module:
		return self.__module
