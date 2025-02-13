"""
ViUR-user-module-related tools and widgets.
"""
from . import html5
from .icons import Icon
from .config import conf


@html5.tag("flare-avatar")
class Avatar(Icon):
	"""
	Icon-Component that represents a user avatar.

	When the user is not, it is automatically fetched into the cache for further usage.
	"""

	def __init__(self):
		super().__init__()
		self.user = None
		self.fallbackClass = None

	def _setValue(self, value):
		if isinstance(value, dict) and "key" in value:
			if "image" not in value:
				value = value["key"]

		# request missing data
		if isinstance(value, str):
			conf["flare.cache"].request({
					"module": "!user",
					"action": "view",
					"params": value
				},
				finishHandler=self._onUserAvailable
			)
		# try to set Image
		elif isinstance(value, dict) and all([k in value for k in ["key", "image"]]) and value["image"]:
			self.user = value
			if self.fallbackClass:
				self.removeClass(self.fallbackClass)
			super()._setValue(value["image"])
		else:
			# if not fallback use initials
			if not self.fallbackIcon and isinstance(value, dict) and all(
					[k in value for k in ["key", "firstname", "lastname"]]):
				super()._setTitle(" ".join([value["firstname"], value["lastname"]]))
			# if a fallback is set use this instead
			elif self.fallbackIcon:
				if self.fallbackClass:
					self.addClass(self.fallbackClass)
				super()._setValue(self.fallbackIcon)
			# if no fallback und no first- and lastname available use hardcoded icon
			else:
				super()._setValue("icon-user")

	def _onUserAvailable(self, res):
		if res["user"]:
			self["value"] = res["user"]

	def _setFallbackclass(self, value):
		self.fallbackClass = value


@html5.tag("flare-username")
class Username(html5.Div):
	"""
	Div-Tag that represents a user name.

	When the user is not, it is automatically fetched into the cache for further usage.
	"""
	_leafTag = True

	def __init__(self):
		super().__init__()
		self.user = None

	def _setValue(self, value):
		self.removeAllChildren()

		if isinstance(value, dict) and not all([k in value for k in ["key", "firstname", "lastname"]]):
			value = value["key"]

		if isinstance(value, str):
			conf["flare.cache"].request({
					"module": "!user",
					"action": "view",
					"params": value
				},
				finishHandler=self._onUserAvailable
			)

		elif isinstance(value, dict) and "key" in value:
			self.user = value

			if all([k in value for k in ["firstname", "lastname"]]):
				self.appendChild(" ".join([value["firstname"], value["lastname"]]))
			else:
				self.appendChild(value["key"])

		else:
			self.appendChild("???")  # I cannot render this user

	def _onUserAvailable(self, res):
		self["value"] = res["user"]
