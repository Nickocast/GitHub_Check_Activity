import json
import requests


class GitHub_check:

    def check_activity(self):
        "Método que se encarga de buscar el usuario y motrar su actividad."
        while True:
            username = input("#github-checker/> ")

            if username:
                try:
                    url = f"https://api.github.com/users/{username}/events"

                    responce = requests.get(url)

                    if responce.status_code == 301:
                        print("El recurso solicitado se ha trasladado de forma permanente. Verifica si la URL está actualizada.")
                    elif responce.status_code == 304:
                        print("El recurso no ha cambiado desde la última vez que fue solicitado. No hay nuevos datos disponibles.")
                    elif responce.status_code == 403:
                        print("Acceso denegado. Es posible que no tengas permisos para acceder a este recurso.")
                    elif responce.status_code == 404:
                        print("No se encontró el recurso solicitado. Verifica el nombre de usuario o la URL.")

                    if responce.status_code == 200:
                        events = responce.json()

                        # Extrae cada dato necesario de su actividad:
                        repo_name = events[1]['repo']['name']
                        type_event = events[1]['type']
                        commits = events[1]['payload']['size']  # numeros de commits

                        # Imprime  tipo de evento, commits realizados y nombre de repositorio
                        print(f"## Tipo de evento: {type_event}, Commmits realizados: {commits}, Repositorio:  {repo_name}")

                        # Marca cambios realizados ultimamente
                        if events[0]['payload']:
                            # Incidencias:
                            issue_status = events[4]['payload']['action']  # Acción del evento (opened, closed, etc.)
                            # Traducción de la acción
                            traducciones = {
                                "opened": "Creó una nueva incidencia",
                                "closed": "Cerró una incidencia",
                                "reopened": "Reabrió una incidencia",
                            }
                            issue_traslated = traducciones.get(issue_status)
                            print(f"## {issue_traslated} en {repo_name}")

                        else:
                            print("## El usuario no realizó acciones ultimamente.")

                        # Marca si recibió alguna valoración
                        processed_events = set()

                        for event in events:
                            # Verifica si el evento es un WatchEvent
                            if event.get('type') == 'WatchEvent':
                                user = event['actor']['login']

                                # Se crea una clave para eliminar respuestas duplicadas
                                event_key = (repo_name, user)

                                # Verificar si este evento ya se procesó
                                if event_key not in processed_events:
                                    print(f"## El repositorio '{repo_name}' recibió una estrella de {user}.")
                                    processed_events.add(event_key)




                except Exception as e:
                    print(f"Error: {e}")

            else:
                print("Error en el CLI.")

app = GitHub_check()
app.check_activity()
