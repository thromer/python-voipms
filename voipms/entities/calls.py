from datetime import datetime

from voipms.baseapi import BaseApi
from voipms.helpers import validate_date, convert_bool


class Calls(BaseApi):
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(Calls, self).__init__(*args, **kwargs)
        self.endoint = 'calls'

    def get_call_accounts(self, client=None):
        """
        Retrieves all Sub Accounts if no additional parameter is provided

        - Retrieves Reseller Client Accounts if Reseller Client ID is provided

        :param client: ID for a specific Reseller Client (Example: 561115)
        :type client: :py:class:`int`
        :returns: :py:class:`dict`
        """
        method = "getCallAccounts"

        parameters = {}
        if client:
            if not isinstance(client, int):
                raise ValueError("ID for a specific Reseller Client as int (Example: 561115)")
            else:
                parameters["client"] = client
        return self._voipms_client._get(method, parameters)

    def get_call_billing(self):
        """
        Retrieves a list of Call Billing Options

        :returns: :py:class:`dict`
        """
        method = "getCallBilling"

        return self._voipms_client._get(method)

    def get_call_types(self, client=None):
        """
        Retrieves a list of Call Types and All DIDs if no additional parameter is provided

        - Retrieves a list of Call Types and Reseller Client DIDs if a Reseller Client ID is provided

        :param client: ID for a specific Reseller Client (Example: 561115)
        :type client: :py:class:`int`
        :returns: :py:class:`dict`
        """
        method = "getCallTypes"

        parameters = {}
        if client:
            if not isinstance(client, int):
                raise ValueError("ID for a specific Reseller Client as int (Example: 561115)")
            else:
                parameters["client"] = client
        return self._voipms_client._get(method, parameters)

    def get_cdr(self, date_from, date_to, timezone,
                answered=False, noanswer=False, busy=False,
                failed=False, **kwargs):
        """
        Retrieves the Call Detail Records of all your calls

        :param date_from: [Required] Start Date for Filtering CDR (Example: '2010-11-30')
        :type date_from: :py:class:`str`
        :param date_to: [Required] End Date for Filtering CDR (Example: '2010-11-30')
        :type date_to: :py:class:`str`
        :param timezone: [Required] Adjust time of calls according to Timezome (Numeric: -12 to 13)
        :type timezone: :py:class:`int`
        :param answered:  Include Answered Calls to CDR (Default: False, Boolean: True/False)
        :type answered: :py:class:`bool`
        :param noanswer:  Include NoAnswered calls to CDR (Default: False, Boolean: True/False)
        :type noanswer: :py:class:`bool`
        :param busy:  Include Busy Calls to CDR (Default: False, Boolean: True/False)
        :type busy: :py:class:`bool`
        :param failed:  Include Failed Calls to CDR (Default: False, Boolean: True/False)
        :type failed: :py:class:`bool`

        :param **kwargs: All optional parameters
        :type **kwargs: :py:class:`dict`

        :param calltype:  Filters CDR by Call Type (Values from calls.get_call_types)
        :type calltype: :py:class:`str`
        :param callbilling:  Filter CDR by Call Billing (Values from calls.get_call_billing)
        :type callbilling: :py:class:`str`
        :param account:  Filter CDR by Account (Values from calls.get_call_accounts)
        :type account: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "getCDR"

        if not isinstance(date_from, str):
            raise ValueError("Start Date for Filtering CDR needs to be str (Example: '2010-11-30')")

        if not isinstance(date_to, str):
            raise ValueError("End Date for Filtering CDR needs to be str (Example: '2010-11-30')")

        date_from_object = validate_date(date_from)
        date_to_object = validate_date(date_to)
        if date_from_object > date_to_object:
            raise ValueError("The start date needs to be ealier or the same as the end date.")
        if date_to_object > datetime.now():
            raise ValueError("The end date can't be in the future.")

        if not isinstance(timezone, int):
            raise ValueError("Adjust time of calls according to Timezome needs to be int (Numeric: -12 to 13)")

        if not isinstance(answered, bool):
            raise ValueError("Include Answered Calls to CDR needs to be bool (Default: False, Boolean: True/False)")

        if not isinstance(noanswer, bool):
            raise ValueError("Include NoAnswered calls to CDR needs to be bool (Default: False, Boolean: True/False)")

        if not isinstance(busy, bool):
            raise ValueError("Include Busy Calls to CDR needs to be bool (Default: False, Boolean: True/False)")

        if not isinstance(failed, bool):
            raise ValueError("Include Failed Calls to CDR needs to be bool (Default: False, Boolean: True/False)")

        if not (answered or noanswer or busy or failed):
            raise ValueError("No Call Status was provided. One of the following parameters needs to be set to True: answered, noanswer, busy, failed")

        parameters = {
            "date_from": date_from,
            "date_to": date_to,
            "timezone": timezone,
            "answered": convert_bool(answered),
            "noanswer": convert_bool(noanswer),
            "busy": convert_bool(busy),
            "failed": convert_bool(failed),
        }

        if "calltype" in kwargs:
            if not isinstance(kwargs["calltype"], str):
                raise ValueError("Filters CDR by Call Type needs to be a str (Values from calls.get_call_types)")
            parameters["calltype"] = kwargs.pop("calltype")

        if "callbilling" in kwargs:
            if not isinstance(kwargs["callbilling"], str):
                raise ValueError("Filter CDR by Call Billing needs to be a str (Values from calls.get_call_billing)")
            parameters["callbilling"] = kwargs.pop("callbilling")

        if "account" in kwargs:
            if not isinstance(kwargs["account"], int):
                raise ValueError("Filter CDR by Account needs to be an in (Values from calls.get_call_accounts)")
            parameters["account"] = kwargs.pop("account")

        if len(kwargs) > 0:
            not_allowed_parameters = ""
            for key, value in kwargs.items():
                not_allowed_parameters += key + " "
            raise ValueError("Parameters not allowed: {}".format(not_allowed_parameters))

        return self._voipms_client._get(method, parameters)
