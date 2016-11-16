import pytest

@pytest.mark.docker_images('webdevops/php-apache:')
@pytest.mark.flaky(reruns=10)
def test_php_fpm_socket(Socket):
    assert Socket("tcp://127.0.0.1:9000").is_listening
