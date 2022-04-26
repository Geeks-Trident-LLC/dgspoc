"""Module containing logic for describe-get-system proof of concept."""

import time

from dgspoc.adaptor import Adaptor

from dgspoc.utils import DotObject
from dgspoc.utils import File
from dgspoc.utils import Misc

from dgspoc.exceptions import DurationArgumentError


class TestResourceCls:
    def __init__(self):
        self.resource = DotObject()
        self.curr_resource = DotObject()
        self.reference = ''
        self.kwargs = DotObject()

        self.status = False
        self.error = ''

    def connect(self, reference, **kwargs):
        self.reference = reference
        yaml_obj = File.get_result_from_yaml_file(reference, default=dict())
        self.resource.update(yaml_obj)
        self.kwargs.update(kwargs)
        return True

    def release(self):
        if self.error:
            print(self.error)
            return False
        return True

    def use_testcase(self, testcase):
        testcases = self.get('testcases')
        if testcase in testcases:
            self.curr_resource = DotObject(testcases.get(testcase))
            return True
        else:
            return False


class Dgs:
    """Describe-Get-System class"""
    resource = TestResourceCls()
    kwargs = DotObject()

    @classmethod
    def wait_for(cls, duration):
        """pausing method

        Parameters
        ----------
        duration (float): total seconds
        """

        is_number, number = Misc.try_to_get_number(duration, return_type=float)
        if is_number:
            time.sleep(number)
        else:
            failure = 'duration must be a number (unexpected: %s)' % duration
            raise DurationArgumentError(failure)

    @classmethod
    def connect_resource(cls, resource_ref, **kwargs):
        """generic connecting test resource

        Parameters
        ----------
        resource_ref (str): a file or database
        kwargs (dict): additional keyword arguments for connecting test resource

        Returns
        -------
        bool: True if successfully connected test resource, otherwise, False.
        """
        result = cls.resource.connect(resource_ref)
        cls.kwargs.update(kwargs)
        return result

    @classmethod
    def use_testcase(cls, testcase):
        """generic use testcase method

        Parameters
        ----------
        testcase (str): a test case resource in test resource

        Returns
        -------
        bool: True if successfully applied testcase from test resource, otherwise, False.
        """
        result = cls.resource.use_testcase(testcase)
        return result

    @classmethod
    def connect_device(cls, host, adaptor='unreal-device', **kwargs):
        """generic connecting device

        Parameters
        ----------
        host (str): address of device
        adaptor (str): connection adaptor.
        kwargs (dict): additional keyword arguments for connecting device

        Returns
        -------
        Adaptor: a device connection
        """

        connection = Adaptor(adaptor, host, **kwargs)
        connection.connect()
        return connection

    @classmethod
    def disconnect_device(cls, connection, **kwargs):
        """generic disconnecting device

        Parameters
        ----------
        connection (Adaptor): instance of device connection
        kwargs (dict): additional keyword arguments for disconnection device connection

        Returns
        -------
        bool: True if successfully disconnected device connection, otherwise, False.
        """
        result = connection.disconnect(**kwargs)
        return result

    @classmethod
    def release_device(cls, connection, **kwargs):
        """generic releasing device

        Parameters
        ----------
        connection (Adaptor): instance of device connection
        kwargs (dict): additional keyword arguments for releasing device connection

        Returns
        -------
        bool: True if successfully released device connection, otherwise, False.
        """
        result = connection.release(**kwargs)
        return result

    @classmethod
    def release_resource(cls):
        """generic method to release test resources

        Returns
        -------
        bool: True if successfully released test resource, otherwise, False.
        """
        result = cls.resource.release()
        return result

    @classmethod
    def execute_cmdline(cls, connection, cmdline, **kwargs):
        """generic device execution

        Parameters
        ----------
        connection (Adaptor): instance of device connection
        cmdline (str): command lines
        kwargs (dict): additional keyword arguments for command line execution

        Returns
        -------
        str: output of command line
        """
        result = connection.execute(cmdline, **kwargs)
        return result

    @classmethod
    def configure_device(cls, connection, cfg, **kwargs):
        """generic device configuration

        Parameters
        ----------
        connection (Adaptor): instance of device connection
        cfg (str): configuration lines
        kwargs (dict): additional keyword arguments for configuring device

        Returns
        -------
        str: the result of device configuration
        """
        result = connection.configure(cfg, **kwargs)
        return result

    @classmethod
    def reload_device(cls, connection, reload_command, **kwargs):
        """generic reloading device

        Parameters
        ----------
        connection (Adaptor): instance of device connection
        reload_command (str): reload command
        kwargs (dict): additional keyword arguments for reloading device

        Returns
        -------
        str: the result of reloading process
        """
        result = connection.reload(reload_command, **kwargs)
        return result
