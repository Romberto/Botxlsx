import os


async def remove_json(dir_path):
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for file in filenames:
            if file.startswith('file') and file.endswith('.xlsx') or file.endswith('.pdf'):
                os.remove(dir_path + '/' + file)


def delimiter_volume(s: str):

    b = s[::-1]

    res1 = ' '.join([b[i:i + 3] for i in range(0, len(b), 3)])[::-1]
    return res1