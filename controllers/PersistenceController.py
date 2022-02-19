import pickle
from os import remove
from models.Records import Records
from discord import File


async def load_Records(server):
    #  If record doesn't exist
    if not server.record_Message:
        await save_Records({}, server)
        return {}
    
    file = await server.record_Message.attachments[0].to_file()
    file = file.fp

    data = pickle.load(file)
    records = Records(data['Records'], server)
    return records


async def save_Records(records, server):
    if server.record_Message:
        await server.record_Message.delete()
    data = {"Server_ID": server.ID, "Records": records}

    filepath = f"./{server.ID}"
    with open(filepath, mode="wb") as file:
        pickle.dump(data, file)


    file = File(filepath)
    await server.data_Channel.send(content=str(server.ID), file=file)
    remove(filepath)