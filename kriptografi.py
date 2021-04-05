import random # Eğer yapabiliyorsak random kendimiz üretelim

def okek(a, b):
  """Ortak katlarının en küçüğünü bulan fonksiyon"""
  return a * b // obeb(a, b)

def obeb(a, b):
  """Ortak bölenlerinin en büyüğünü bulan fonksiyon"""
  if a == 0:
    return b
  return obeb(b % a, a)

def isprime(a): #64 bitte çözüm üretemiyor değişmesi gerekli
  """bir sayının asal olup olmadığını kontrol eden fonksiyon"""
  i = 3
  if(a < 2):
    return False
  if a != 2 and a % 2 == 0:
    return False
  while i <= a ** (1 / 2):
    if a % i == 0:
      return False
    i += 2
  return True

def stringBinary(metin):
  """String değerini binary ye çeviren fonksiyon"""
  binaryMetin = ""
  for i in metin:
    binaryMetin += "".join(f"{ord(i):08b}")
  return binaryMetin

def integerBinary(n):
  """Integer değerini binary ye çeviren fonksiyon"""
  nBinary = ""
  nBinary = str(bin(n))[2:] # 0b olmadan
  return nBinary

def binaryString(binary):
  """Binary değerini string e çeviren fonksiyon"""
  blok = []
  metin = ""
  for i in range(0, len(binary), 8):
    blok.append(binary[i:i+8])
  for char in blok:
    metin += chr(int(char, 2))
  return metin

def ayniMi(plaintext, plaintext2):
  """İki text dosyasının içeriğinin aynı olup olmadığını True/False döndüren fonksiyon"""
  f = open(plaintext, "r")
  metin = f.read()
  f.close()

  f = open(plaintext2, "r")
  metin2 = f.read()
  f.close()

  if(metin == metin2):
    return True
  return False

# -----------------------------------

def keygen(n):
  """n bite yakın asal sayı 2^(n-1) ile 2^n arasında üretiliyor."""
  while True:
    p = random.randrange(2 ** (n - 1), 2 ** n)
    if(isprime(p)):
      break
  while True:
    q = random.randrange(2 ** (n - 1), 2 ** n)
    if(isprime(q)):
      if(q == p):
        continue
      break
  acikAnahtar = p ** 2 * q
  gizliAnahtar = pow(acikAnahtar, -1, okek(p - 1, q - 1))

  f = open("publickey.txt", "w+")
  f.write(str(acikAnahtar))
  f.close()

  f = open("privatekey.txt", "w+")
  f.write(str(gizliAnahtar) + " " + str(p) + " " + str(q))
  f.close()

# -----------------------------------

def encrypt(plaintext, publickey):
  try:
    f = open(publickey, "r")
    acikAnahtar = int(f.read())
  except IOError:
    print("Publickey bulunamıyor. keygen fonksiyonunu çalıştırınız.")
  finally:
    f.close()

  try:
    f = open(plaintext, "r")
    duzMetin = f.read()
  except IOError:
    print("Düz metin bulunamıyor. plaintext.txt oluşturun.")
  finally:
    f.close()

  f = open("ciphertext.txt", "w+")
  binaryMetin = stringBinary(duzMetin)
  metinDecimal = int(binaryMetin, 2)
  ciphertext = str(pow(metinDecimal, acikAnahtar, acikAnahtar))
  f.write(ciphertext)
  f.close()

# -----------------------------------

def decrypt(ciphertext, privatekey):
  try:
    f = open(privatekey, "r")
    dizi = []
    for i in f.read().split():
      dizi.append(i)
    gizliAnahtar = int(dizi[0])
    p = int(dizi[1])
    q = int(dizi[2])
  except IOError:
    print("Privatekey bulunamıyor. keygen fonksiyonunu çalıştırınız.")
  finally:
    f.close()

  try:
    f = open(ciphertext, "r")
    ciphertext = int(f.read())
  except IOError:
    print("ciphertext bulunamıyor. encrypt fonksiyonunu çalıştırınız.")
  finally:
    f.close()

  f = open("plaintext2.txt", "w+")
  n =  pow(ciphertext, gizliAnahtar, p*q)
  nBinary = integerBinary(n)
  
  if(len(nBinary) % 8 != 0):
    nBinary = "0" + nBinary

  metin = binaryString(nBinary)
  f.write(metin)
  f.close()

  
  print("plaintxt ile plaintext2 özdeş mi: " , ayniMi("plaintext.txt", "plaintext2.txt"))


# -----------------------------------

n = int(input("Anahtar uzunluğu giriniz: "))

keygen(n)
encrypt("plaintext.txt","publickey.txt")
decrypt("ciphertext.txt", "privatekey.txt")
