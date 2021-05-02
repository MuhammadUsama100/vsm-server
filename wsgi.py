from query_processing import app
from OpenSSL import SSL
# context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('server.crt')

if __name__ == '__main__':
    app.run(host="0.0.0.0", ssl_context='adhoc')
