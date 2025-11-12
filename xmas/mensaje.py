from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap, random, datetime, imageio

# === CONFIGURACIÓN GLOBAL ===
WIDTH, HEIGHT = 1080, 1920
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf" # Cambia si tienes otra fuente
SNOW_COLOR = (168, 216, 255)

# === UTILIDADES ===
def current_date():
    return datetime.datetime.now().strftime("%-d %b %Y").upper()

def draw_message(draw, text, date_text, font_text, font_date):
    # Ajustar texto
    wrapped_text = textwrap.fill(text, width=30)
    bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font_text, spacing=15)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    bubble_padding = 80
    bubble_w = text_w + bubble_padding
    bubble_h = text_h + bubble_padding
    bubble_x = (WIDTH - bubble_w) / 2
    bubble_y = (HEIGHT - bubble_h) / 2 + 150

    # Fecha
    date_bbox = draw.textbbox((0, 0), date_text, font=font_date)
    date_w = date_bbox[2] - date_bbox[0]

    draw.text(((WIDTH - date_w) / 2, 120), date_text, font=font_date, fill=(150, 150, 150))

    # Burbuja
    draw.rounded_rectangle(
        [bubble_x, bubble_y, bubble_x + bubble_w, bubble_y + bubble_h],
        radius=60,
        fill=(32, 32, 32)
    )

    # Texto
    draw.multiline_text(
        (bubble_x + bubble_padding / 2, bubble_y + bubble_padding / 2),
        wrapped_text, font=font_text, fill=(255, 255, 255), spacing=15
    )
    return bubble_x, bubble_y, bubble_w, bubble_h

# === VERSIÓN BASE ===
def generate_base_message(text):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    font_date = ImageFont.truetype(FONT_PATH, 50)
    font_text = ImageFont.truetype(FONT_PATH, 60)
    draw_message(draw, text, current_date(), font_text, font_date)

    img.save("mensaje_base.png")
    print("✅ mensaje_base.png creado.")

# === VERSIÓN NIEVE (GIF) ===
def generate_snow_animation(text, frames=36):
    img_base = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
    draw_base = ImageDraw.Draw(img_base)
    font_date = ImageFont.truetype(FONT_PATH, 50)
    font_text = ImageFont.truetype(FONT_PATH, 60)

    bubble_x, bubble_y, bubble_w, bubble_h = draw_message(draw_base, text, current_date(), font_text, font_date)

    snowflakes = [[random.randint(0, WIDTH), random.randint(-HEIGHT, HEIGHT), random.uniform(1, 3)] for _ in range(250)]
    accumulation = [0] * WIDTH
    frames_list = []

    for _ in range(frames):

        frame = img_base.copy()
        draw = ImageDraw.Draw(frame)

        for flake in snowflakes:
            flake[1] += flake[2]
            if flake[1] > HEIGHT:
                flake[0] = random.randint(0, WIDTH)
                flake[1] = random.uniform(-50, 0)

            if bubble_y - 3 < flake[1] < bubble_y + 3 and bubble_x < flake[0] < bubble_x + bubble_w:
                accumulation[int(flake[0])] = min(accumulation[int(flake[0])] + 1, 40)
                flake[1] = random.uniform(-30, 0)

            draw.ellipse((flake[0], flake[1], flake[0] + 3, flake[1] + 3), fill=SNOW_COLOR)

        for x in range(int(bubble_x), int(bubble_x + bubble_w)):
            acc_height = accumulation[x] if x < len(accumulation) else 0
            if acc_height > 0:
                draw.line((x, bubble_y - acc_height, x, bubble_y), fill=SNOW_COLOR)

        frame = frame.filter(ImageFilter.GaussianBlur(radius=0.6))
        frames_list.append(frame)

    imageio.mimsave("mensaje_nieve.gif", frames_list, duration=0.12)
    print("✅ mensaje_nieve.gif creado.")

# === VERSIÓN NAVIDAD (GORRO + NIEVE) ===
def generate_christmas_theme(text):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_date = ImageFont.truetype(FONT_PATH, 50)
    font_text = ImageFont.truetype(FONT_PATH, 60)
    bubble_x, bubble_y, bubble_w, bubble_h = draw_message(draw, text, current_date(), font_text, font_date)

    # === Colocar el gorro sobre la burbuja ===
    gorro = Image.open("gorro_navidad.png").convert("RGBA")

    # Escalarlo proporcionalmente a la burbuja (por ejemplo, 70% del ancho de la burbuja)
    scale = 0.1
    new_size = (int(gorro.width * scale), int(gorro.height * scale))
    gorro = gorro.resize(new_size, Image.LANCZOS)

    # (Opcional) Rotar ligeramente el gorro para que caiga hacia la izquierda
    gorro = gorro.rotate(-10, expand=True)

    # Calcular posición para que se apoye justo encima de la burbuja
    hat_x = int(bubble_x + (bubble_w) - gorro.width*0.6)  # centrado horizontalmente
    hat_y = int(bubble_y - (gorro.height)*0.5)  # justo encima del borde superior

    # Pegar con transparencia
    img.paste(gorro, (hat_x, hat_y), gorro)


    # Nieve estática ligera
    for _ in range(180):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.uniform(2, 4)
        draw.ellipse((x, y, x + size, y + size), fill=SNOW_COLOR)

    img.save("mensaje_navidad.png")
    print("✅ mensaje_navidad.png creado.")

# === FUNCIÓN PRINCIPAL ===
def generate_all(text):
    generate_base_message(text)
    generate_snow_animation(text)
    generate_christmas_theme(text)

# === EJECUCIÓN ===
if __name__ == "__main__":
    mensaje = input("Escribe tu mensaje: ")
    generate_all(mensaje)
    print("\n🎄 ¡Todas las versiones se han generado con éxito!")
