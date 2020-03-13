# aruba.tipsconfig

This collection implements modules to communicate with Clearpass' XML API, a.k.a. tipsconfig.
The module parameters are used to build and XML snippet sent to the API as a request. The API returns a response as an XML snippet. Its up to the caller to parse the XML response for further use.

For more details about the API, see [the complete doumentation](https://community.arubanetworks.com/aruba/attachments/aruba/aaa-nac-guest-access-byod/17921/1/ClearPass%20Configuration%20API%20Guide%20(1).pdf).

The XML API gives read and write access to configuration elements such as Services, Auth Sources and Enforcement Profiles, that cannot be accessed through the more recently developed REST API.

The purpose of these modules is to allow management of Clearpass' configuration as code, with version-controlled templated XML files.