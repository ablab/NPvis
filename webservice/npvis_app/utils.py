import os.path
import shutil

from npvis.settings import DATA_PATH

def readFile(in_file, out_filename):
    with open(out_filename, "wb") as fw:
        for chunk in in_file.chunks():
            fw.write(chunk)

def get_or_create_session(request):
    session_key = request.session.session_key
    if not session_key or not request.session.exists(session_key):
        tries = 10
        for i in range(tries):
            request.session.create()
            break

        session_key = request.session.session_key

    session_key = "S" + session_key
    if not os.path.exists(os.path.join(DATA_PATH, session_key)):
        os.mkdir(os.path.join(DATA_PATH, session_key))
    return session_key


def clear_session_dir(request):
    session_key = get_or_create_session(request)
    shutil.rmtree(os.path.join(DATA_PATH, session_key))