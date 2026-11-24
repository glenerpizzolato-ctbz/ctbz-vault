"""Deixa no GIF do WhatsApp Web só o painel da conversa com o bot (remove a lista de chats).
Quadros de tela cheia: recorta a partir de 33,5% da largura. Quadros de zoom (menores, no canto): já mostram só o chat; são ampliados.
Uso: crop_gif.py <src> <dst>"""
import sys
from PIL import Image, ImageSequence
im = Image.open(sys.argv[1]); W, H = im.size; x0 = int(W * 0.335); TW, TH = W - x0, H
out = []
for f in ImageSequence.Iterator(im):
    fr = f.convert("RGB")
    bbox = Image.eval(fr.convert("L"), lambda p: 255 if 8 < p < 245 else 0).getbbox() or (0, 0, W, H)
    if bbox[2] - bbox[0] < 0.75 * W:  # quadro de zoom no canto
        bx = list(bbox); bx[0] += int((bbox[2]-bbox[0]) * 0.09); sub = fr.crop(tuple(bx)); r = min(TW / sub.width, TH / sub.height); sub = sub.resize((int(sub.width * r), int(sub.height * r)))
        tgt = Image.new("RGB", (TW, TH), (17, 27, 33)); tgt.paste(sub, ((TW - sub.width) // 2, (TH - sub.height) // 2))
    else:
        tgt = fr.crop((x0, 0, W, H))
    out.append((tgt.convert("P", palette=Image.ADAPTIVE), f.info.get("duration", 800)))
out[0][0].save(sys.argv[2], save_all=True, append_images=[x for x, _ in out[1:]], duration=[d for _, d in out], loop=0)
import os; [os.remove(p) for p in __import__("glob").glob(sys.argv[2] + ".*.png")]
ims = [out[i][0].convert("RGB") for i in range(len(out))]
cols = 4; rows = (len(ims) + cols - 1) // cols; tw, th = TW // 4, TH // 4
sheet = Image.new("RGB", (tw * cols, th * rows)); [sheet.paste(x.resize((tw, th)), ((i % cols) * tw, (i // cols) * th)) for i, x in enumerate(ims)]
sheet.save(sys.argv[2] + ".sheet.png"); print(len(out), "frames ->", sys.argv[2] + ".sheet.png")
