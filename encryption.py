import base64
import math
import sys

# Decodes a base 64 number
def base64decode(num):
	temp = int.from_bytes(base64.b64decode(num), "little")
	return temp

# Encrypts a message and returns the cipher text
def encrypt(e, n, msg):
	m = int.from_bytes(msg.encode(), 'little')
	c = pow(m, e, n)
	b64m = base64.b64encode(c.to_bytes(math.ceil(c.bit_length() / 8), 'little'))
	return b64m.decode()

# Decrypts a cipher text and returns the message
def decrypt(d, n, msg):
	c = base64.b64decode(msg.encode())
	c = int.from_bytes(c, 'little')
	m = pow(c, d, n)

	msg = m.to_bytes(math.ceil(m.bit_length() / 8), 'little')
	msg = msg.decode()
	return msg

try:
	puKey = open("public.key", "r")
	prKey = open("private.key", "r")

	public = puKey.readline()
	private = prKey.readline()

	e, n = public[:len(public) // 2], public[len(public) // 2:]
	d = private[:len(private) // 2]
	e = base64decode(e)
	n = base64decode(n)
	d = base64decode(d)

	input2 = sys.argv[1]
	if (input2 == "-h"):
		print("-e for encrypt\n-d for decrypt\n-s for sign")
		print("example input: -e input_file output_file")
		exit()

	input_file = sys.argv[2]
	with open(input_file, "r") as file:
		m = file.read()
		if not m:
			print("Error: File is empty")
			exit()

		if (input2 == "-e"):
			msg = encrypt(e, n, m)
		elif (input2 == "-d"):
			msg = decrypt(d, n, m)
		elif (input2 == "-s"):
			msg = encrypt(d, n, m)
		else:
			print("Invalid parameters use -h for help")
			exit()

		output_file = open(sys.argv[3], "w")
		output_file.write(str(msg))
except Exception:
	print("Invalid parameters use -h for help")