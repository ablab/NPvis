def readFile(in_file, out_filename):
    with open(out_filename, "wb") as fw:
        for chunk in in_file.chunks():
            fw.write(chunk)