import pamela as pam
import pwservice_pb2
import signal
import time

from grpc.beta import implementations
from grpc.beta import interfaces


class PasswordServer(pwservice_pb2.BetaPasswordServiceServicer):

  def ChangePassword(self, request, context):
    try:
      pam.authenticate(request.user, request.old_password, 'login')
      # User is authenticated, change the password
      pam.change_password(request.user, request.new_password, 'login')
      return pwservice_pb2.PamReply(success=True)
    except pam.PAMError, e:
      return pwservice_pb2.PamReply(success=False, message=e.message)


def serve():
  with open('server.key') as f:
    private_key = f.read()
  with open('server.crt') as f:
    certificate_chain = f.read()

  server = pwservice_pb2.beta_create_PasswordService_server(PasswordServer())
  server_credentials = implementations.ssl_server_credentials(
      ((private_key, certificate_chain,),))
  server.add_secure_port('[::]:1337', server_credentials)
  server.start()
  try:
    while True:
      signal.pause()
  except KeyboardInterrupt:
    pass
  server.stop(0)

if __name__ == '__main__':
  serve()
