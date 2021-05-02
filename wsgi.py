from query_processing import app
# from OpenSSL import SSL
# context = ssl.SSLContext()
# context.load_cert_chain('fullchain.pem', 'privkey.pem')

if __name__ == '__main__':
    app.run(host="0.0.0.0", ssl_context=('cert.pem', 'key.pem'))
