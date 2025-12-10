# SmashPoint

Sistema de gestión de torneos con fase de grupos y eliminación.

- Guía de entorno: `CONFIGURACION_ENTORNO.md`
- Documentación de implementación: `DOCUMENTACION_IMPLEMENTACION.md`
- Ejemplo CSV: `samples/jugadores_ejemplo.csv`

Inicio rápido (Windows / PowerShell):

```powershell
cd "c:\Users\alexa\Downloads\SmashPoint (1)\SMASHPOINT"
python -m venv venv; .\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
