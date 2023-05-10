def convertToBinary(filename):
    with open(filename, 'rb') as file:
        binarydata = file.read()
    return binarydata


def convertBinaryToFile(binarydata, filename):
    with open(filename, 'wb') as file:
        file.write(binarydata)
