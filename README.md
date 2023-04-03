# RSA

### How to use
```shell
$python main.py --help
usage: main.py [-h] [-k KEY] [-i INPUT] [-o OUTPUT] {encrypt,decrypt,generate}

positional arguments:
  {encrypt,decrypt,generate}
                        Command

options:
  -h, --help            show this help message and exit
  -k KEY, --key KEY     Key
  -i INPUT, --input INPUT
                        Input File
  -o OUTPUT, --output OUTPUT
                        Output File
```
commands encrypt, decrypt require input and output flags.  
key - private or public key depending on command.  
if key wasn't provided - public and private key will be shown.  

### Example

```shell
$ cat example.txt
Hello World!
$ python main.py generate
public key: 142483236927903109-220526264977705303
private key: 130637071013791229-220526264977705303
$ python main.py encrypt --key 130637071013791229-220526264977705303 --input example.txt --output example1.txt
$ python main.py decrypt --key 142483236927903109-220526264977705303 --input example1.txt --output example2.txt
```
