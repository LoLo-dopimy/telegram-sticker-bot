from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from PIL import Image
from rembg import remove
import cv2

TOKEN = "7953143058:AAFQ6FIvFfd0f4nhDlZhnkIbPzo8w8G_MWk"

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    file = await update.message.photo[-1].get_file()
    await file.download_to_drive("photo.jpg")

    # قراءة الصورة
    img = cv2.imread("photo.jpg")

    # تحويلها إلى كرتونية
    cartoon = cv2.stylization(img, sigma_s=150, sigma_r=0.25)
    cv2.imwrite("cartoon.jpg", cartoon)

    # إزالة الخلفية
    with open("cartoon.jpg", "rb") as i:
        input_image = i.read()

    output_image = remove(input_image)

    with open("no_bg.png", "wb") as o:
        o.write(output_image)

    # تجهيز الملصق
    img = Image.open("no_bg.png").convert("RGBA")
    img.thumbnail((512, 512))

    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))

    x = (512 - img.width) // 2
    y = (512 - img.height) // 2

    canvas.paste(img, (x, y), img)

    canvas.save("sticker.webp", "WEBP")

    await update.message.reply_sticker(open("sticker.webp", "rb"))

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.PHOTO, photo))

app.run_polling()