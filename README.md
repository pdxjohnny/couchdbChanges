openssl genrsa -out private.pem 1024
openssl rsa -pubout -in private.pem -out public.pem
