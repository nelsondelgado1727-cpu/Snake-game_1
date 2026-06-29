"""
JUEGO DE LA SERPIENTE (SNAKE)
================================


"""

import tkinter as tk   # Librería para crear la ventana y los gráficos
import random           # Librería para generar números aleatorios (posición de la comida)


ANCHO_TABLERO = 400      # Ancho de la ventana de juego en píxeles
ALTO_TABLERO = 400       # Alto de la ventana de juego en píxeles
TAMANIO_CELDA = 20       # Tamaño de cada cuadro de la serpiente/comida
VELOCIDAD_MS = 120       # Milisegundos entre cada movimiento (más bajo = más rápido)

# -------------------------------------------------------------------
# VARIABLES GLOBALES DEL JUEGO
# (aquí se guarda "lo que está pasando" en la partida)
# -------------------------------------------------------------------
segmentos_serpiente = []   # Lista de posiciones (x, y) que ocupa la serpiente
direccion_actual = "Right" # Hacia dónde se mueve la serpiente: Up, Down, Left, Right
comida_x = 0                # Posición X de la comida
comida_y = 0                # Posición Y de la comida
puntaje = 0                 # Puntos que lleva el jugador
juego_terminado = False     # True cuando la serpiente choca


# -------------------------------------------------------------------
# FUNCIONES DEL JUEGO
# -------------------------------------------------------------------

def iniciar_juego():
    """Prepara todo para empezar (o reiniciar) una partida nueva."""
    global segmentos_serpiente, direccion_actual, puntaje, juego_terminado

    # La serpiente empieza en el centro del tablero, con 3 cuadritos
    x_centro = ANCHO_TABLERO // 2
    y_centro = ALTO_TABLERO // 2
    segmentos_serpiente = [
        (x_centro, y_centro),
        (x_centro - TAMANIO_CELDA, y_centro),
        (x_centro - TAMANIO_CELDA * 2, y_centro),
    ]

    direccion_actual = "Right"
    puntaje = 0
    juego_terminado = False

    generar_comida()


def generar_comida():
    """Elige una posición aleatoria para la comida, que no caiga
    encima de la serpiente."""
    global comida_x, comida_y

    posicion_libre = False
    while not posicion_libre:
        x = random.randrange(0, ANCHO_TABLERO, TAMANIO_CELDA)
        y = random.randrange(0, ALTO_TABLERO, TAMANIO_CELDA)

        if (x, y) not in segmentos_serpiente:
            posicion_libre = True

    comida_x = x
    comida_y = y


def cambiar_direccion(evento):
    """Se ejecuta cuando el jugador presiona una flecha del teclado.
    Evita que la serpiente se devuelva sobre sí misma (por ejemplo,
    si va a la derecha, no puede girar instantáneamente a la izquierda)."""
    global direccion_actual

    nueva_direccion = evento.keysym  # "Up", "Down", "Left" o "Right"

    opuestas = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}

    if opuestas.get(nueva_direccion) != direccion_actual:
        direccion_actual = nueva_direccion


def mover_serpiente():
    """Calcula la nueva posición de la cabeza y mueve el resto del cuerpo."""
    global segmentos_serpiente

    x_cabeza, y_cabeza = segmentos_serpiente[0]

    if direccion_actual == "Up":
        nueva_cabeza = (x_cabeza, y_cabeza - TAMANIO_CELDA)
    elif direccion_actual == "Down":
        nueva_cabeza = (x_cabeza, y_cabeza + TAMANIO_CELDA)
    elif direccion_actual == "Left":
        nueva_cabeza = (x_cabeza - TAMANIO_CELDA, y_cabeza)
    else:  # "Right"
        nueva_cabeza = (x_cabeza + TAMANIO_CELDA, y_cabeza)

    # Agregamos la nueva cabeza al inicio de la lista
    segmentos_serpiente.insert(0, nueva_cabeza)

    # Si la serpiente comió, no se elimina la cola (así crece).
    # Si no comió, se elimina la cola para que no crezca infinitamente.
    if nueva_cabeza == (comida_x, comida_y):
        global puntaje
        puntaje += 4
        generar_comida()
    else:
        segmentos_serpiente.pop()


def hay_colision():
    """Revisa si la cabeza de la serpiente chocó con la pared o con
    su propio cuerpo. Devuelve True si el juego debe terminar."""
    x_cabeza, y_cabeza = segmentos_serpiente[0]

    # Choque con las paredes del tablero
    if x_cabeza < 0 or x_cabeza >= ANCHO_TABLERO:
        return True
    if y_cabeza < 0 or y_cabeza >= ALTO_TABLERO:
        return True

    # Choque con el propio cuerpo (el resto de la lista, sin la cabeza)
    if (x_cabeza, y_cabeza) in segmentos_serpiente[1:]:
        return True

    return False


def dibujar():
    """Borra el lienzo y vuelve a dibujar la comida, la serpiente y el puntaje."""
    lienzo.delete("all")  # Borra todo lo dibujado antes

    # Dibujar la comida (cuadro rojo)
    lienzo.create_rectangle(
        comida_x, comida_y,
        comida_x + TAMANIO_CELDA, comida_y + TAMANIO_CELDA,
        fill="red", outline=""
    )

    # Dibujar la serpiente (cuadros verdes)
    for (x, y) in segmentos_serpiente:
        lienzo.create_rectangle(
            x, y, x + TAMANIO_CELDA, y + TAMANIO_CELDA,
            fill="lightgreen", outline="darkgreen"
        )

    # Actualizar el texto del puntaje
    etiqueta_puntaje.config(text=f"Puntaje: {puntaje}")


def mostrar_mensaje_fin():
    """Muestra el mensaje de fin de juego en el centro del tablero."""
    lienzo.create_text(
        ANCHO_TABLERO / 2, ALTO_TABLERO / 2 - 10,
        text="¡Juego terminado!",
        fill="white", font=("Arial", 18, "bold")
    )
    lienzo.create_text(
        ANCHO_TABLERO / 2, ALTO_TABLERO / 2 + 20,
        text="Presiona ENTER para reiniciar",
        fill="white", font=("Arial", 12)
    )


def actualizar_juego():
    """Esta es la función principal del juego: se repite sola cada
    VELOCIDAD_MS milisegundos mientras el juego no haya terminado."""
    global juego_terminado

    if not juego_terminado:
        mover_serpiente()

        if hay_colision():
            juego_terminado = True
            dibujar()
            mostrar_mensaje_fin()
        else:
            dibujar()
            # Volvemos a llamar a esta misma función después de un tiempo
            ventana.after(VELOCIDAD_MS, actualizar_juego)


def tecla_enter(evento):
    """Si el juego terminó y el jugador presiona ENTER, se reinicia."""
    if juego_terminado:
        iniciar_juego()
        actualizar_juego()


# -------------------------------------------------------------------
# CONFIGURACIÓN DE LA VENTANA (esto se ejecuta una sola vez al inicio)
# -------------------------------------------------------------------

ventana = tk.Tk()
ventana.title("Juego de la Serpiente (Snake)")

etiqueta_puntaje = tk.Label(ventana, text="Puntaje: 0", font=("Arial", 14))
etiqueta_puntaje.pack()

lienzo = tk.Canvas(ventana, width=ANCHO_TABLERO, height=ALTO_TABLERO, bg="black")
lienzo.pack()

# Conectamos las teclas del teclado con sus funciones
ventana.bind("<Up>", cambiar_direccion)
ventana.bind("<Down>", cambiar_direccion)
ventana.bind("<Left>", cambiar_direccion)
ventana.bind("<Right>", cambiar_direccion)
ventana.bind("<Return>", tecla_enter)

# Empezamos el juego
iniciar_juego()
actualizar_juego()

# Esta línea mantiene la ventana abierta hasta que el usuario la cierre
ventana.mainloop()
