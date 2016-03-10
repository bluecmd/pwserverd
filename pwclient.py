import pwservice_pb2
import sys

from grpc.beta import implementations


TIMEOUT_SECONDS = 10


def run():
  with open('server.crt') as f:
    trusted_certs = f.read()
  credentials = implementations.ssl_channel_credentials(
          trusted_certs, None, None)
  channel = implementations.secure_channel(sys.argv[1], 1337, credentials)
  stub = pwservice_pb2.beta_create_PasswordService_stub(channel)
  response = stub.ChangePassword(pwservice_pb2.ChangePasswordRequest(
      user='testuser', old_password='helloworld', new_password='newworld'),
      TIMEOUT_SECONDS)
  if not response.success:
    print 'Password change failed:', response.message
  else:
    print 'Password changed'


if __name__ == '__main__':
  run()
