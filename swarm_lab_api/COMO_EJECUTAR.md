# Cómo ejecutar la API (Swarm Lab)

## 1. Crear el entorno virtual (solo la primera vez)

### Linux
```bash
cd swarm_lab_api
python3 -m venv venv
# O si usas la misma ruta que start_atriz_lab.sh:
# python3 -m venv ~/catkin_ws/swarm_lab_env
```

### Windows (PowerShell)
```powershell
cd swarm_lab_api
python -m venv venv
# O con una versión concreta (recomendado 3.8–3.12):
# py -3.12 -m venv venv
```

---

## 2. Activar el entorno

**Sí hay que activar el entorno antes de instalar dependencias y de arrancar la API.**

### Linux
```bash
cd swarm_lab_api
source venv/bin/activate
# O si creaste el venv en catkin_ws:
# source ~/catkin_ws/swarm_lab_env/bin/activate
```

Verás algo como `(venv)` o `(swarm_lab_env)` al inicio del prompt.

### Windows (PowerShell)
```powershell
cd swarm_lab_api
.\venv\Scripts\Activate.ps1
```

En CMD:
```cmd
cd swarm_lab_api
venv\Scripts\activate.bat
```

---

## 3. Instalar dependencias (con el entorno activado)

```bash
pip install -r requirements.txt
```

---

## 4. Arrancar la API (con el entorno activado)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

En Windows con una versión concreta de Python (sin venv propio):
```powershell
py -3.12 -m uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

---

## Resumen del orden

1. Crear el entorno (solo una vez): `python -m venv venv`
2. **Activar el entorno:** `source venv/bin/activate` (Linux) o `.\venv\Scripts\Activate.ps1` (Windows)
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar: `uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload`
