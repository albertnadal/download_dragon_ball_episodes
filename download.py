import requests
import json

print("Descarregant els episodis de la temporada 1 de Bola de Drac...\n")

url = "https://www.3cat.cat/api/3cat/dades/?queryKey=%5B%22tira%22%2C%7B%22url%22%3A%22%2F%2Fapi.3cat.cat%2Fvideos%3F_format%3Djson%26no_agrupacio%3DPUAGR_LLSIGN%26tipus_contingut%3DPPD%26items_pagina%3D16%26pagina%3D1%26sdom%3Dimg%26version%3D2.0%26cache%3D180%26https%3Dtrue%26master%3Dyes%26programatv_id%3D48836%26ordre%3Dcapitol%26temporada%3DPUTEMP_1%26ordre%3Dcapitol%26temporada%3DPUTEMP_1%22%7D%5D"

episodes_info = requests.get(url)

if episodes_info.status_code == 200:
    data = episodes_info.json()

    print(f"Hi ha disponibles {data['resposta']['items']['num']} episodis per descarregar.\n")

    for video_info in data['resposta']['items']['item']:
        print(f"Descarregant {video_info['titol']}... ", flush=True, end="")

        episode_info = requests.get(f"https://api-media.3cat.cat/pvideo/media.jsp?media=video&versio=vast&idint={video_info['id']}&profile=pc_3cat&format=dm")
        episode_data = episode_info.json()

        if episode_data['media']['format'] != "MP4":
            print("[ ERROR: No hi ha disponible el video en format MP4 per a aquest episodi ]", flush=True)
        else:
            video_url = next((url_data['file'] for url_data in episode_data['media']['url'] if url_data['label'] == "720p"), None)
            if video_url is None:
                print("[ ERROR: No existeix el video en resolucio 720p ]")
            else:
                video_content = requests.get(video_url)

                with open(f"{video_info['titol']}.mp4", "wb") as file:
                    file.write(video_content.content)

                print(" [ DONE ]", flush=True)
