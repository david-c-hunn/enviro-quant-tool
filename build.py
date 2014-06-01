from pybuilder.core import init, use_plugin

# Install the following packages if they are not already present
use_plugin("python.core")
use_plugin("python.coverage")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")


default_task = "publish"

@init
def initialize(project):
	pass