from query_processing import app
# from OpenSSL import SSL
# context = ssl.SSLContext()
# context.load_cert_chain('fullchain.pem', 'privkey.pem')

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
