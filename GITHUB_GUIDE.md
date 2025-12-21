# 📤 Guía para Subir el Proyecto a GitHub

Esta guía te ayudará a subir tu proyecto BCV API a GitHub paso a paso.

## 📋 Prerequisitos

1. Tener Git instalado en tu computadora
2. Tener una cuenta en GitHub
3. Estar en el directorio del proyecto

## 🚀 Pasos para Subir a GitHub

### 1️⃣ Verificar que Git esté instalado

```powershell
git --version
```

Si no está instalado, descárgalo de: https://git-scm.com/

### 2️⃣ Inicializar el repositorio Git (si no está inicializado)

```powershell
git init
```

### 3️⃣ Configurar tu información de Git (si es la primera vez)

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

### 4️⃣ Agregar todos los archivos al staging

```powershell
git add .
```

### 5️⃣ Hacer el primer commit

```powershell
git commit -m "Initial commit: BCV USD API con scraper y FastAPI"
```

### 6️⃣ Crear un repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `bcv-usd-api` (o el que prefieras)
3. Descripción: "API REST para obtener el tipo de cambio USD/Bs del BCV"
4. Selecciona "Public" o "Private"
5. **NO** marques "Add a README file" (ya tienes uno)
6. Click en "Create repository"

### 7️⃣ Conectar tu repositorio local con GitHub

Copia el comando que GitHub te muestra, será algo como:

```powershell
git remote add origin https://github.com/TU-USUARIO/bcv-usd-api.git
```

### 8️⃣ Cambiar a la rama main (si es necesario)

```powershell
git branch -M main
```

### 9️⃣ Subir el código a GitHub

```powershell
git push -u origin main
```

Te pedirá tu usuario y contraseña de GitHub (o token de acceso personal).

---

## 🔐 Autenticación con GitHub

Si te pide autenticación, tienes dos opciones:

### Opción A: GitHub CLI (Recomendado)
```powershell
# Instalar GitHub CLI
winget install --id GitHub.cli

# Autenticarte
gh auth login
```

### Opción B: Token de Acceso Personal
1. Ve a: https://github.com/settings/tokens
2. Click en "Generate new token (classic)"
3. Selecciona los permisos: `repo`
4. Copia el token
5. Úsalo como contraseña cuando Git te lo pida

---

## ✅ Verificar que se subió correctamente

1. Ve a tu repositorio en GitHub: `https://github.com/TU-USUARIO/bcv-usd-api`
2. Deberías ver todos tus archivos
3. El README.md se mostrará automáticamente en la página principal

---

## 📝 Comandos Útiles para Futuras Actualizaciones

```powershell
# Ver el estado de los archivos
git status

# Agregar archivos modificados
git add .

# Hacer commit de los cambios
git commit -m "Descripción de los cambios"

# Subir los cambios a GitHub
git push

# Ver el historial de commits
git log --oneline
```

---

## 🎯 Estructura Final en GitHub

Tu repositorio tendrá:

```
bcv-usd-api/
├── README.md              ← Documentación principal (se ve en GitHub)
├── LICENSE                ← Licencia MIT
├── .gitignore            ← Archivos a ignorar
├── requirements.txt       ← Dependencias
├── bcv_scraper.py        ← Scraper principal
├── api_server.py         ← API REST
├── ejemplo_uso.py        ← Ejemplos completos
├── ejemplo_uso_simple.py ← Ejemplo simple
└── test_api.py           ← Tests de la API
```

---

## 💡 Tips Adicionales

### Agregar un badge de "último commit"
Agrega esto al README.md:
```markdown
![GitHub last commit](https://img.shields.io/github/last-commit/TU-USUARIO/bcv-usd-api)
```

### Agregar descripción y topics en GitHub
1. Ve a tu repositorio
2. Click en ⚙️ (Settings) al lado de "About"
3. Agrega descripción y topics: `python`, `fastapi`, `api`, `venezuela`, `bcv`, `scraping`

### Habilitar GitHub Pages (opcional)
Si quieres documentación web:
1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: main → /docs

---

## 🆘 Solución de Problemas

### Error: "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/TU-USUARIO/bcv-usd-api.git
```

### Error: "failed to push some refs"
```powershell
git pull origin main --rebase
git push -u origin main
```

### Olvidé agregar el .gitignore antes del primer commit
```powershell
git rm -r --cached .
git add .
git commit -m "Agregar .gitignore"
git push
```

---

## 🎉 ¡Listo!

Tu proyecto ahora está en GitHub y otros pueden:
- ⭐ Darle estrella
- 🍴 Hacer fork
- 📥 Clonarlo
- 🐛 Reportar issues
- 🔧 Contribuir con pull requests
