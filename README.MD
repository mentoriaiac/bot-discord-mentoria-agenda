# Bot Google Calendar para Discord

Bot simples que obtem os reuniões agendadadas do dia envia uma notifiação em uma canal no discord, ou pode ser chamado, por comando, solicitando a agenda do dia.

## Requisitos

- Crie um BOT no[Portal de desenvolvimento doDiscord](https://discord.com/developers/applications)

- Python >= 3.6 
- Pip3 >= 18.0

## Config.json e key.json

[Crie uma conta e serviços]("https://developers.google.com/identity/protocols/oauth2/service-account#creatinganaccount")
**Importante**: Restrinja a sua service account com as permissões abaixo:

|                            |    Scope | Meaning |
|-----------------------|-----------|-------------------|
||  https://www.googleapis.com/auth/calendar | read/write access to Calendars
||  https://www.googleapis.com/auth/calendar.readonly | read-only access to Calendars
||  https://www.googleapis.com/auth/calendar.events | read/write access to Events
||  https://www.googleapis.com/auth/calendar.events.readonly | read-only access to Events
||  https://www.googleapis.com/auth/calendar.settings.readonly | read-only access to Settings
||  https://www.googleapis.com/auth/calendar.addons.execute | run as a Calendar add-on

Renomei os arquivos, key.json.example e config.json.example para key.json e config.json.

Ajustes o valores do config.json com as informações do seu bot, criado em passo anterior.
Substitua os valores de key.json pelo conteundo da arquivo da service account criado acima.

## Local 

1. `sudo apt install -y python3-venv`
2. `python3 -m venv my_env`
3. `source my_env/bin/activate`
4. `pip3 install -r requirements.txt`

### Docker

1. `docker build -t calendarbot:0.1 . `
2. `docker run -d calendarbot:0.1`
