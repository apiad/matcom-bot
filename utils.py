from json import load


# Gets general chats
def get_general_chats():
    groups_channels = "Canales y grupos oficiales de MATCOM\n\n"
    with open("chats_info.json") as info:
        data = load(info)
        groups_channels += "\n".join(data[1])
    return groups_channels


def get_specific_chats(text:str):
    result = ""
    with open("chats_info.json") as info:
        data = load(info)
        result += data[0][text] + "\n"
        result += "\n".join(data[2][text])
    return result