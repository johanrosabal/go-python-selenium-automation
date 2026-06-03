from core.ui.common.base_test import BaseTest as GenericBaseTest
from core.utils.test_decorators import project_config
from applications.web.demo2.app.demo2_app import Demo2App

@project_config(app_name="demo2", app_class=Demo2App)
class Demo2BaseTest(GenericBaseTest):
    """
    Base test for Demo2.
    Inherits setup/teardown and driver management from the core GenericBaseTest.
    """
    pass
