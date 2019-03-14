# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import requests
import json

class OctosmashPlugin(octoprint.plugin.StartupPlugin, octoprint.plugin.SettingsPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.EventHandlerPlugin, octoprint.plugin.ProgressPlugin):

	def get_settings_defaults(self):
		return dict(
			auth_token="",
			url=""
		)

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]

	def on_after_startup(self):
		self._logger.info(self._settings.get(["url"]))

	def on_event(self, event, payload):
		if event == 'PrinterStateChanged':
			data = { 
				"status": payload["state_id"], 
				"moreinfo": payload["state_string"]
			}
			self.call(data)
		elif event == 'PrintStarted':
			data = { 
				"status": "printing",
				"moreinfo": str(payload["path"]), 
				"value": "0"
			}
			self.call(data)

	def on_print_progress(self, storage, path, progress):
		data = { 
			"status": "printing", 
			"moreinfo": str(path), 
			"value": str(progress)
		}
		self.call(data)

	def call(self, data):

		auth_token = self._settings.get(["auth_token"])
		url = self._settings.get(["url"])

		printer_name = self._printer_profile_manager.get_current()["name"]

		data["auth_token"] = auth_token
		data["title"] = printer_name

		response = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})

		self._logger.info(data)
		self._logger.info(response)


__plugin_name__ = "Octosmash"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = OctosmashPlugin()

