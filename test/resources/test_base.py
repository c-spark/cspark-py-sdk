import pytest
from cspark.sdk import SparkSdkError, Uri, UriParams

BASE_URL = 'https://excel.test.coherent.global/tenant-name'


def test_build_url_from_partial_resources():
    assert (
        Uri.partial('folders/f/services/s', base_url=BASE_URL, endpoint='execute').value
        == 'https://excel.test.coherent.global/tenant-name/api/v3/folders/f/services/s/execute'
    )
    assert (
        Uri.partial('proxy/custom-endpoint', base_url=BASE_URL).value
        == 'https://excel.test.coherent.global/tenant-name/api/v3/proxy/custom-endpoint'
    )


def test_handle_extra_slashes_in_partial_resources():
    assert (
        Uri.partial('/folders/f/services/s/', base_url=BASE_URL, endpoint='execute').value
        == 'https://excel.test.coherent.global/tenant-name/api/v3/folders/f/services/s/execute'
    )
    assert (
        Uri.partial('/public/version/123/', base_url=BASE_URL).value
        == 'https://excel.test.coherent.global/tenant-name/api/v3/public/version/123'
    )


def test_build_url_from_uri_params():
    assert (
        Uri.of(UriParams(folder='f', service='s'), base_url=BASE_URL, endpoint='execute').value
        == 'https://excel.test.coherent.global/tenant-name/api/v3/folders/f/services/s/execute'
    )
    assert (
        Uri.of(None, base_url=BASE_URL, version='api/v4', endpoint='execute').value
        == 'https://excel.test.coherent.global/tenant-name/api/v4/execute'
    )
    assert (
        Uri.of(UriParams(public=True), base_url=BASE_URL, version='api/v4', endpoint='execute').value
        == 'https://excel.test.coherent.global/tenant-name/api/v4/public/execute'
    )
    assert (
        Uri.of(
            UriParams(folder='low', service='priority', version_id='high-priority'),
            base_url=BASE_URL,
            endpoint='execute',
        ).value
        == 'https://excel.test.coherent.global/tenant-name/api/v3/version/high-priority/execute'
    )
    assert (
        Uri.of(UriParams(version_id='123'), base_url=BASE_URL).value
        == 'https://excel.test.coherent.global/tenant-name/api/v3/version/123'
    )
    assert (
        Uri.of(UriParams(service_id='456'), base_url=BASE_URL).value
        == 'https://excel.test.coherent.global/tenant-name/api/v3/service/456'
    )
    assert (
        Uri.of(UriParams(proxy='custom-endpoint'), base_url=BASE_URL).value
        == 'https://excel.test.coherent.global/tenant-name/api/v3/proxy/custom-endpoint'
    )
    assert (
        Uri.of(UriParams(proxy='custom-endpoint', public=True), base_url=BASE_URL).value
        == 'https://excel.test.coherent.global/tenant-name/api/v3/public/proxy/custom-endpoint'
    )
    assert (
        Uri.of(UriParams(proxy='/custom-endpoint///', public=True), base_url=BASE_URL).value
        == 'https://excel.test.coherent.global/tenant-name/api/v3/public/proxy/custom-endpoint'
    )


def test_decode_string_uri():
    assert Uri.decode('folders/f/services/s') == UriParams(folder='f', service='s')
    assert Uri.decode('f/s') == UriParams(folder='f', service='s')
    assert Uri.decode('f/s[1.0]') == UriParams(folder='f', service='s', version='1.0')
    assert Uri.decode('folders/f/services/s[1.2.3]') == UriParams(folder='f', service='s', version='1.2.3')
    assert Uri.decode('service/456') == UriParams(service_id='456')
    assert Uri.decode('version/123') == UriParams(version_id='123')
    assert Uri.decode('proxy/custom-endpoint') == UriParams(proxy='custom-endpoint')
    assert Uri.decode('/f/s/') == UriParams(folder='f', service='s')
    assert Uri.decode('f/s/') == UriParams(folder='f', service='s')
    assert Uri.decode('///f//s//') == UriParams(folder='f', service='s')
    assert Uri.decode('/f/s[]/') == UriParams(folder='f', service='s')
    assert Uri.decode('') == UriParams()
    assert Uri.decode('//f/') == UriParams()
    assert Uri.decode('//f') == UriParams()
    assert Uri.decode('///') == UriParams()


def test_throw_error_on_invalid_uri():
    with pytest.raises(SparkSdkError):
        Uri.validate('')
    with pytest.raises(SparkSdkError):
        Uri.validate('f//')
    with pytest.raises(SparkSdkError):
        Uri.validate(UriParams(version='1.0'))


def test_uri_params_as_service_uri():
    assert UriParams(folder='f', service='s').service_uri == 'f/s'
    assert UriParams(folder='f', service='s', version='1.2.3').service_uri == 'f/s[1.2.3]'
    assert UriParams(service_id='456').service_uri == 'service/456'
    assert UriParams(version_id='123').service_uri == 'version/123'
    assert UriParams().service_uri == ''


def test_uri_params_pick_class_props():
    assert UriParams(folder='f', service='s', version='1.2.3').pick('folder') == UriParams(folder='f')
    assert UriParams(folder='f', service='s').pick('service') == UriParams(service='s')
    assert UriParams(folder='f', service='s').pick('folder', 'service') == UriParams(folder='f', service='s')
    assert UriParams(folder='f', service='s').pick('folder', 'service', 'version') == UriParams(folder='f', service='s')


def test_uri_params_omit_class_props():
    assert UriParams(folder='f', service='s', version='1.2.3').omit('folder') == UriParams(service='s', version='1.2.3')
    assert UriParams(folder='f', service='s').omit('service') == UriParams(folder='f')
    assert UriParams(folder='f', service='s').omit('folder', 'service') == UriParams()
    assert UriParams(folder='f', service='s').omit('folder', 'service', 'version') == UriParams()
