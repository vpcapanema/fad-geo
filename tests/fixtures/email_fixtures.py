from unittest.mock import MagicMock

def email_service_fixture():
    email_service = MagicMock()
    email_service.send_email.return_value = True
    return email_service

def test_send_email(email_service_fixture):
    result = email_service_fixture.send_email("test@example.com", "Subject", "Body")
    assert result is True

def test_send_email_failure(email_service_fixture):
    email_service_fixture.send_email.side_effect = Exception("Email sending failed")
    try:
        email_service_fixture.send_email("test@example.com", "Subject", "Body")
    except Exception as e:
        assert str(e) == "Email sending failed"