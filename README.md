# heic2jpg 📱➡️🖼️

**EN | Convert iPhone HEIC photos to normal JPG — in bulk, offline, no uploads.**
**TR | FotoÇevir — iPhone HEIC fotoğraflarını normal JPG'ye çevirir — toplu, çevrimdışı, yükleme yok.**

Your iPhone saves photos as `.HEIC`. Your Windows PC, your web portal, your
friend's Android — none of them open it. One command converts a whole folder.
GPS/EXIF metadata is **always stripped** — your location never travels with the file.

iPhone'unuz fotoğrafları `.HEIC` kaydediyor; Windows bilgisayarınız, web
portalı, arkadaşınızın Android'i açmıyor. Tek komut tüm klasörü çevirir.
GPS/EXIF metadata **her zaman silinir** — konumunuz dosyayla asla yolculuk etmez.

```bash
python heic2jpg.py ./DCIM                    # EN: preview | TR: önizleme
python heic2jpg.py ./DCIM --apply            # EN: convert all | TR: hepsini çevir
python heic2jpg.py IMG_1234.HEIC --apply     # EN: single file | TR: tek dosya
python heic2jpg.py ./Photos --recursive --out ./JPGs --apply
```

```
✔ IMG_0001.HEIC -> IMG_0001.jpg: 2.1 MB -> 780.3 KB
✔ IMG_0002.HEIC -> IMG_0002.jpg: 1.9 MB -> 690.5 KB
Done: 24 converted, 0 failed (52.3 MB -> 18.4 MB).
```

---

## 🇬🇧 English

### Why?

Every iPhone user eventually hits ".HEIC hell": a website rejects the upload,
the school portal wants JPG, Windows shows a black thumbnail, grandma's
computer can't open the photo at all. Online converters make you **upload
private photos to strangers' servers** (with file-count limits on free tiers).

`heic2jpg` converts everything locally with one command. No uploads, no
watermarks, no file limits.

### Privacy

**EXIF metadata (GPS location, camera serial, timestamps) is stripped by
default.** Add `--keep-exif` only if you really need it.

### Features

- Whole folders, `--recursive`, or single files
- `--out DIR` to collect results in one place
- JPEG quality control (`--quality`, default 92)
- Rotation is applied automatically (no sideways photos)
- `.avif` support included (ffmpeg 7+ decodes it)
- Dry-run preview by default — nothing is written until `--apply`
- Never overwrites: existing JPGs are skipped unless `--overwrite`

### Install

**1. ffmpeg** on your PATH:

```bash
# Windows
winget install Gyan.FFmpeg
# macOS
brew install ffmpeg
# Linux
sudo apt install ffmpeg
```

**2. Download `heic2jpg.py`** — that's the whole app:

```bash
curl -LO https://raw.githubusercontent.com/Volvox6767/heic2jpg/main/heic2jpg.py
```

No `pip install`. Single file, zero Python dependencies.

### Usage

```
python heic2jpg.py FILE/FOLDER... [--out DIR] [--quality N] [--recursive]
                   [--keep-exif] [--overwrite] [--apply]

FILE/FOLDER...   HEIC files and/or folders / dosyalar ve klasörler
--out DIR        write JPGs to DIR instead of next to source
--quality N      JPEG quality (default 92)
--recursive      scan folders recursively
--keep-exif      keep metadata (default: strip GPS/camera info)
--overwrite      overwrite existing JPGs
--apply          really convert (default: dry-run preview)
```

### FAQ

**Does it upload my photos anywhere?** No. 100% local.

**What about Live Photos / videos?** Out of scope — this converts image files only. (Use picfit to resize the JPGs afterwards.)

**AVIF?** Yes — ffmpeg 7+ decodes AVIF and HEIC alike.

---

## 🇹🇷 Türkçe

### Neden?

Her iPhone kullanıcısı er ya da geç ".HEIC cehennemine" çarpar: site yüklemeyi
reddeder, okul portalı JPG ister, Windows siyah küçük resim gösterir,
büyükanenin bilgisayarı fotoğrafı hiç açamaz. Online dönüştürücüler ise özel
fotoğraflarınızı **yabancıların sunucularına yüklemenizi** ister (ücretsiz
sürümlerde dosya sayısı limiti vardır).

`heic2jpg` her şeyi yerel olarak, tek komutla çevirir. Yükleme yok, filigran
yok, dosya limiti yok.

### Gizlilik

**EXIF metadata'sı (GPS konumu, kamera seri no, tarihler) her zaman silinir** —
ffmpeg `-map_metadata -1` ile çıktıdan tüm metadata atılır.

### Özellikler

- Tüm klasör, `--recursive` ya da tek dosya
- Sonuçları tek yerde toplamak için `--out KLASÖR`
- JPEG kalite kontrolü (`--quality`, varsayılan 92)
- Döndürme otomatik uygulanır (yana yatık fotoğraf çıkmaz)
- `.avif` desteği (ffmpeg 7+ çözer)
- Varsayılan dry-run önizleme — `--apply` gelene kadar hiçbir şey yazılmaz
- Asla üzerine yazmaz: var olan JPG'ler `--overwrite` olmadan atlanır

### Kurulum

**1. ffmpeg** PATH'te olsun:

```bash
# Windows
winget install Gyan.FFmpeg
# macOS
brew install ffmpeg
# Linux
sudo apt install ffmpeg
```

**2. `heic2jpg.py` dosyasını indirin** — uygulamanın tamamı bu tek dosya:

```bash
curl -LO https://raw.githubusercontent.com/Volvox6767/heic2jpg/main/heic2jpg.py
```

`pip install` gerekmez. Tek dosya, sıfır Python bağımlılığı.

### Kullanım

```
python heic2jpg.py DOSYA/KLASÖR... [--out KLASÖR] [--quality N] [--recursive]
                   [--overwrite] [--apply]

DOSYA/KLASÖR...   HEIC dosyaları ve/veya klasörleri
--out KLASÖR      JPG'ler kaynak yanına değil KLASÖR'e yazılır
--quality N       JPEG kalitesi 1-100 (varsayılan 92)
--recursive       klasörleri alt klasörlerle birlikte tara
--overwrite       var olan JPG'lerin üzerine yaz
--apply           gerçekten çevir (varsayılan: dry-run önizleme)
```

### SSS

**Fotoğraflar bir yere yükleniyor mu?** Hayır. %100 yerel.

**Live Photo / videolar?** Kapsam dışı — bu araç yalnızca görsel dosyaları çevirir. (Sonrasında JPG'leri küçültmek için picfit kullanın.)

**AVIF?** pillow-heif sürümünüz destekliyorsa o da çevrilir.

---

Made with ❤ by **Ahmet Gedik** — [instagram.com/ahmetgedik67](https://www.instagram.com/ahmetgedik67)
Follow on Instagram for more free everyday tools.
Daha fazla ücretsiz günlük araç için Instagram'da takip edin.

License / Lisans: [MIT](LICENSE)
