# 🦆 Duck Hunt AI - Hand Tracking Edition

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MediaPipe](https://img.shields.io/badge/AI-MediaPipe-green.svg)](https://mediapipe.dev/)
[![Pygame](https://img.shields.io/badge/Game-Pygame-orange.svg)](https://www.pygame.org/)

Una versión moderna y tecnológica del clásico **Duck Hunt**, donde tú eres el controlador. Utiliza inteligencia artificial y visión por computadora para detectar tus manos y permitirte cazar patos con gestos reales.

---

## 🚀 Características

-   **Control por Gestos**: Olvídate del ratón. Usa tu dedo índice para apuntar y el pulgar para disparar.
-   **IA en Tiempo Real**: Desarrollado con **MediaPipe Hand Landmarker** para una detección de manos precisa y fluida.
-   **Interfaz Moderna**: Pantalla de inicio minimalista y profesional construida con **Flet**.
-   **Retro-Gaming**: Sonidos y mecánicas que rinden homenaje al juego original.
-   **Auto-Configuración**: El sistema descarga automáticamente los modelos de IA necesarios al iniciar por primera vez.

---

## 🛠️ Tecnologías Utilizadas

-   **Python**: Lenguaje principal.
-   **Pygame**: Motor para la lógica del juego y renderizado 2D.
-   **MediaPipe**: Framework de Google para la detección de puntos clave de la mano.
-   **OpenCV**: Gestión de la cámara y procesamiento de imágenes.
-   **Flet**: Interfaz de usuario (UI) para el menú de inicio.
-   **Numpy**: Procesamiento matemático eficiente.

---

## 📋 Requisitos Previos

-   Python 3.10 o superior instalado.
-   Una cámara web funcional.
-   Conexión a internet (solo para la primera ejecución, para descargar el modelo de IA).

---

## 📦 Instalación y Uso

### 1. Clonar o descargar el repositorio
Asegúrate de tener todos los archivos en una carpeta local.

### 2. Instalar dependencias
Abre tu terminal en la carpeta del proyecto y ejecuta:
```bash
pip install -r requirements.txt
```

### 3. Iniciar el juego
Ejecuta el lanzador oficial:
```bash
python game/home.py
```

---

## 🎮 ¿Cómo se juega?

El juego utiliza el modelo de visión por computadora para rastrear tu mano derecha o izquierda:

1.  **Apuntar**: Mueve tu **dedo índice** frente a la cámara para mover la mira en la pantalla.
2.  **Disparar**: Junta la punta de tu **dedo pulgar** con el dedo índice (gesto de "pinch" o gatillo).
3.  **Vidas**: Tienes 3 vidas. Cada pato que escape te costará una vida.
4.  **Teclas rápidas**:
    -   `Q`: Salir del juego en cualquier momento.
    -   `R`: Reiniciar la partida (en la pantalla de Game Over).

---

## 📁 Estructura del Proyecto

-   `game/home.py`: Pantalla de inicio y lanzador del juego.
-   `game/main.py`: Lógica principal del juego y detección de IA.
-   `game/AvesSprites.py`: Gestión de las animaciones y comportamiento de los patos.
-   `requirements.txt`: Lista de librerías necesarias.
-   `img/` y `sound/`: Recursos visuales y auditivos.

---

## 👨‍💻 Créditos

Desarrollado como un experimento de integración de IA y videojuegos.
- **Modelos de IA**: Google MediaPipe.
- **Motor**: Pygame Community.

---
¡Buena suerte en la caza! 🦆🎯
