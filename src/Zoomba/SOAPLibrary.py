import json
from robot.libraries.BuiltIn import BuiltIn
from suds.plugin import DocumentPlugin
from suds.client import Client
from suds import WebFault

zoomba = BuiltIn()


class _ObjectNamespacePlugin(DocumentPlugin):
    """_ObjectNamespacePlugin

        This class contains a plugin for use in fixing broken WSDL Namespaces.\n
        defaultNamespace: (string) The default namespace found in the primary WSDL\n


    """
    defaultNamespace = None

    def loaded(self, context):
        """loaded. A plugin run after loading the WSDL but before using it to construct a client.\n
            context: (string) The Raw WSDL and imported schema.\n
        """
        if self.defaultNamespace is None:
            start = context.document.find(b'targetNamespace')
            first_quote = int(context.document.find(b'"', start)) + 1
            second_quote = int(context.document.find(b'"', first_quote))
            self.defaultNamespace = context.document[first_quote:second_quote]
        elif b'tns' not in context.document or b'targetNamespace' not in context.document:
            document_split = context.document.split(b'xmlns', 1)
            context.document = document_split[0]+b'xmlns:tns="'+self.defaultNamespace+b'" targetNamespace="' + self.defaultNamespace + b'" xmlns'+document_split[1]
            number_of_types = context.document.count(b'type="')
            start_location = context.document.find(b'type="')
            for x in range(number_of_types):
                end_type = context.document.find(b'"', start_location+len(b'type="'))
                if b':' not in context.document[start_location:end_type]:
                    change_type = context.document[start_location:end_type]
                    change_type = change_type.replace(b'"', b'"tns:')
                    context.document = context.document[:start_location] + change_type + context.document[end_type:]
                start_location = context.document.find(b'type="', start_location+1)


class SOAPLibrary(object):
    """Zoomba SOAP Library

        This class is the base Library used to generate automated SOAP Tests in the Zoomba Automation Framework.

    """

    @staticmethod
    def create_soap_session_and_fix_wsdl(host=None, endpoint=None, alias=None, **kwargs):
        """Create Soap Session. This Keyword utilizes the WSDL and directly accesses calls from sudsLibrary.\n
            host: (string) The host url.\n
            endpoint: (string) SOAP API endpoint containing the actions to be referenced.\n
            alias: (string} Sets the alias for the SudsLibrary Framework
            **kwargs: (optional) Parameters that could be included to add options to client creation.
            Current supported parameters are:\n
                set_location: http address\n
        """
        pluginInstance = _ObjectNamespacePlugin()
        plugin_client = Client(host+endpoint + '?WSDL', plugins=[pluginInstance])
        suds_library = BuiltIn().get_library_instance("SudsLibrary")
        suds_library._add_client(plugin_client, alias)
        if 'set_location' in kwargs:
            suds_library.set_location(kwargs['set_location'])

    @staticmethod
    def create_soap_session(host=None, endpoint=None, alias=None, **kwargs):
        """ Create Soap Session. This Keyword utilizes the WSDL to create a soap client.\n
            host: (string) The host url.\n
            endpoint: (string) SOAP API endpoint containing the actions to be referenced.\n
            **kwargs: (optional) Parameters that could be included to add options to client creation.
            Current supported parameters are:\n
                set_location: http address\n
        """
        suds_library = BuiltIn().get_library_instance("SudsLibrary")
        if alias is not None:
            suds_library.create_soap_client(host+endpoint+'?WSDL', alias)
        else:
            suds_library.create_soap_client(host+endpoint+'?WSDL')
        if 'set_location' in kwargs:
            suds_library.set_location(kwargs['set_location'])

    def create_soap_session_and_set_location(self, host=None, endpoint=None, alias=None, set_location=None, fix=False):
        """ Create Soap Session and Set Location. In addition to the client creation, this keyword sets the location
            as specified.\n
            host: (string) The host url.\n
            endpoint: (string) SOAP API endpoint containing the actions to be referenced.\n
            set_location: (string) If set will overwrite the WSDL location with specified address.\n
            If set to None will replace location with host and endpoint specified\n
        """
        if set_location is None:
            set_location = host+endpoint
        if fix:
            self.create_soap_session_and_fix_wsdl(host, endpoint, alias, set_location=set_location)
        else:
            self.create_soap_session(host, endpoint, alias, set_location=set_location)

    @staticmethod
    def call_soap_method_with_list_object(action=None, soap_object=None):
        """ Call Soap Method. Calls soap method with list object \n
            action: (string) SOAP Action to be called.\n
            soap_object: (list) Soap Object in list format, list must be ordered wrt schema\n
        """
        suds_library = BuiltIn().get_library_instance("SudsLibrary")
        response = suds_library.call_soap_method(action, *soap_object)
        return response

    @staticmethod
    def call_soap_method_with_object(action=None, **soap_object):
        """ Call Soap Method with dictionary object. Calls soap method \n
            action: (string) SOAP Action to be called.\n
            soap_object: (dict) Soap Object in dict format, dict must contain all required parts of schema object. \n
        """
        suds_library = BuiltIn().get_library_instance("SudsLibrary")
        client = suds_library._client()
        method = getattr(client.service, action)
        try:
            received = method(**soap_object)
        except WebFault as e:
            received = e.fault
        return received

    @staticmethod
    def create_wsdl_objects(wsdl_type=None, object_dict=None):
        """ Create Wsdl Objects. This Keyword utilizes the WSDL to create a WSDL object based on the information
            provided.\n
            wsdl_type: (string) Wsdl object to be created.\n
            object_dict: (dict) Python Dictionary containing values and nested dictionaries with construction similar to
            wsdl defined objects.\n
            return: (response object) Returns the SOAP client object.\n
        """
        client = BuiltIn().get_library_instance("SudsLibrary")._client()
        request_object = client.factory.create(wsdl_type)
        _build_wsdl_objects(client, request_object, object_dict)
        return request_object

    @staticmethod
    def convert_soap_response_to_json(soap_response=None):
        """ Convert Soap Response To Dictionary: This keyword builds a dictionary from the sudsLibrary response\n
            json_actual_response: (request response object) The response from an API.\n
            return: There is no actual returned output, other than error messages when comparisons fail.\n
        """
        a = _build_dict_from_response(soap_response)
        return json.dumps(a)


def _build_dict_from_response(soap_response=None):
    """
    Build Dict From Response: This keyword builds a dictionary from the sudsLibrary response.\n
    :param soap_response: sudsLibrary response.\n
    :return: python dictionary.\n
    """
    try:
        response_dictionary = dict(soap_response)
    except:  # lgtm [py/catch-base-exception]
        zoomba.log(message='Argument Passed Was Not Iterable', level='INFO')
        return soap_response
    new_response = {}

    for index in range(len(response_dictionary)):
        key, value = response_dictionary.popitem()
        if isinstance(value, list):
            temp_list = []
            for item in value:
                if str(type(item)) == "<type 'instance'>" or 'sudsobject' in str(type(item)):
                    temp_item = _build_dict_from_response(item)
                    temp_list.append(temp_item)
                else:
                    temp_list.append(str(item))
            new_response[key] = temp_list
        elif str(type(value)) == "<type 'instance'>" or 'sudsobject' in str(type(value)):
            temp_dict = _build_dict_from_response(value)
            new_response[key] = temp_dict
        else:
            new_response[key] = str(value)
    return new_response


def _build_wsdl_objects(client=None, request_object=None, object_dict=None):
    """ Build Wsdl Objects. This Keyword utilizes the WSDL to build a wsdl object in a recursive manner.\n
        client: (SudsLibrary._client() instance) The current client session.\n
        request_object: (SudsLibrary._client.factory() instance) Wsdl object to be built.\n
        object_dict: (dict) Dictionary containing data to create request_object.\n

    """
    for key, value in object_dict.items():
        if isinstance(value, dict):
            try:
                temp_object = _wsdl_sub_builder(client, value)
                request_object.__setattr__(key, temp_object)
            except BaseException as ex:   #lgtm [py/catch-base-exception]
                if ex:
                    zoomba.log('Failed to define wsdl_object_type for child object. [' + key + ']', level='ERROR')
        elif isinstance(value, list):
            temp_list = []
            for item in value:
                if isinstance(item, dict):
                    temp_object = _wsdl_sub_builder(client, item)
                    temp_list.append(temp_object)
                else:
                    temp_list.append(item)
            request_object.__setattr__(key, temp_list)
        else:
            request_object.__setattr__(key, value)


def _wsdl_sub_builder(client=None, object_dict=None):
    """
    Wsdl Sub Builder. This Keyword creates children objects for wsdl objects.\n
    client: (SudsLibrary._client() instance) The current client session.\n
    object_dict:  (dict) Dictionary containing data to create request_object.\n
    (method only) wsdl_object_type: Wsdl object Type of wsdl sub-object.\n
    return: returns child object\n
    """
    sub_type = object_dict.pop('wsdl_object_type')
    temp_object = client.factory.create(sub_type)
    _build_wsdl_objects(client, temp_object, object_dict)
    return temp_object
