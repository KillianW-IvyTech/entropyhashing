## **Hash Folder:**
Generates SHA-256 hashes for strings and files, and lets you know when errors occur (Ex. files does not exist) which is inside the hash folder.
### Commands:
``` python hash_tool.py -s "string" ``` generates SHA-256 hash for string \
``` python hash_tool.py -f ./document.pdf ``` generates SHA-256 hash for file
## **Cipher Folder:**
Uses a Caesar cipher to encrpyt and decrpyt input text, as well as files with text. To decrypt, you need to output from the encryption, and the number tied when input.
### Commands:
```python cipher_tool.py encrypt -s "Hello World" -k 4``` encrypts "Hello World" into "Lipps Asvph" \
```python cipher_tool.py decrypt -s "Lipps Asvph" -k 4``` decrypts "Lipps Asvph" back into "Hello World" \
```python cipher_tool.py encrypt -f cipher.txt -k 10 > encrypted.txt``` encrypts cipher.txt into new encrypted.txt file \
```python cipher_tool.py decrypt -f encrypted.txt``` decrypts the message back, i.e. what was originally in cipher.txt
## **Sign Folder:**
It is using the cryptography library in Python to first generate a key pair, a public a private one. Then it signs a file of choice, by hashing with SHA-256, and then encrypting that hash with the private key. 
Lastly, it decrypts the signature with the public key to make sure it matches the file's hash, making sure its not tampered with.
### Commands:
```python sign_tool.py keygen``` creates the public and private keys (.pem files) \
```python sign_tool.py sign -f message.txt``` signs the files (makes the .sig file) \
```python sign_tool.py verify -f message.txt -s message.txt.sig``` makes sure file wasnt tampered with
