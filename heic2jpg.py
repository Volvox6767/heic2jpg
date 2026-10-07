#!/usr/bin/env python3
"""
heic2jpg - Convert iPhone HEIC/HEIF photos to JPG. Offline, in bulk, no uploads.

EN: Your iPhone saves photos as .HEIC, your PC / web portal / friend's phone
    cannot open them. This converts a whole folder to normal .JPG in one
    command - 100% offline. GPS/EXIF metadata is always stripped (privacy).
TR: iPhone fotograflariniz .HEIC ama bilgisayariniz acmiyor mu? Tum klasoru
    tek komutla normal .JPG'ye cevirir - %100 cevrimdisi. GPS/EXIF her zaman
    silinir (gizlilik).
"""

import argparse
import os
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

AUTHOR = "Ahmet Gedik"
INSTAGRAM = "https://www.instagram.com/ahmetgedik67"
VERSION = "1.0.0"

EXTS = [".heic", ".heif", ".avif"]


def human(n):
    n = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1000 or unit == "TB":
            return f"{int(n)} B" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1000


def find_ffmpeg():
    p = shutil.which("ffmpeg")
    if p:
        return p
    try:
        import imageio_ffmpeg  # optional fallback: pip install imageio-ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def collect(paths, recursive):
    found = []
    for p in paths:
        if os.path.isfile(p):
            found.append(p)
        elif os.path.isdir(p):
            if recursive:
                for root, _dirs, files in os.walk(p):
                    for f in files:
                        if os.path.splitext(f)[1].lower() in EXTS:
                            found.append(os.path.join(root, f))
            else:
                for f in sorted(os.listdir(p)):
                    fp = os.path.join(p, f)
                    if os.path.isfile(fp) and os.path.splitext(f)[1].lower() in EXTS:
                        found.append(fp)
        else:
            print(f"  ? not found, skipping / bulunamadi, atlandi: {p}")
    return sorted(found)


def convert(ff, src, dst, quality):
    """Encode first video stream of a still image container to JPEG."""
    q = max(2, min(31, round((100 - quality) * 0.31)))
    cmd = [
        ff, "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
        "-i", src,
        "-frames:v", "1", "-map", "0:v:0",
        "-q:v", str(q),
        "-map_metadata", "-1",   # strip ALL metadata (GPS/EXIF) / tum metadata silinir
        dst,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        msg = (proc.stderr or "").strip().splitlines()
        raise RuntimeError(msg[-1] if msg else f"ffmpeg exit {proc.returncode}")


def main():
    ap = argparse.ArgumentParser(
        prog="heic2jpg",
        description="Convert HEIC/HEIF photos to JPG - offline, in bulk. / "
                    "HEIC/HEIF fotoraflari cevrimdisi ve toplu olarak JPG'ye cevirir.",
        epilog=f"Made with \u2764 by {AUTHOR} - {INSTAGRAM}\nVersion {VERSION} (MIT)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("inputs", nargs="+", metavar="FILE/FOLDER",
                    help="HEIC files and/or folders / HEIC dosyalari ve/veya klasorler")
    ap.add_argument("--out", metavar="DIR", help="write JPGs to DIR instead of next to source / JPG'ler farkli klasore")
    ap.add_argument("--quality", type=int, default=92, help="JPEG quality 1-100 (default 92) / JPEG kalitesi")
    ap.add_argument("--recursive", action="store_true", help="scan folders recursively / klasorleri recursive tara")
    ap.add_argument("--overwrite", action="store_true", help="overwrite existing JPGs / varsa uzerine yaz")
    ap.add_argument("--apply", action="store_true",
                    help="really convert (default: dry-run preview) / gerceklestir (varsayilan: onizleme)")
    ap.add_argument("--version", action="version", version=f"heic2jpg {VERSION}")
    args = ap.parse_args()

    ff = find_ffmpeg()
    if not ff:
        print("ERROR: ffmpeg not found. / HATA: ffmpeg bulunamadi.")
        print("  Install / Kurulum:")
        print("    Windows : winget install Gyan.FFmpeg   (or: pip install imageio-ffmpeg)")
        print("    macOS   : brew install ffmpeg")
        print("    Linux   : sudo apt install ffmpeg")
        sys.exit(1)

    files = collect(args.inputs, args.recursive)
    if not files:
        print("No HEIC/HEIF/AVIF files found / HEIC/HEIF/AVIF dosyasi bulunamadi.")
        sys.exit(1)

    out_dir = os.path.abspath(args.out) if args.out else None
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    print(f"Found {len(files)} file(s) / {len(files)} dosya bulundu")

    plan = []  # (src, dst, src_size)
    skipped = 0
    for src in files:
        stem = os.path.splitext(os.path.basename(src))[0]
        dst = os.path.join(out_dir, stem + ".jpg") if out_dir else \
              os.path.join(os.path.dirname(os.path.abspath(src)), stem + ".jpg")
        if os.path.abspath(src) == os.path.abspath(dst):  # paranoid: never in-place
            continue
        if os.path.exists(dst) and not args.overwrite:
            skipped += 1
            print(f"  - exists, skip / zaten var, atlandi: {dst}")
            continue
        plan.append((src, dst, os.path.getsize(src)))

    if not plan:
        print("\nNothing to convert. Cevrilecek dosya yok.")
        sys.exit(0)

    if not args.apply:
        for src, dst, sz in plan:
            print(f"  [dry] {os.path.basename(src)} ({human(sz)}) -> {os.path.basename(dst)}")
        print(f"\nDRY-RUN: {len(plan)} file(s) would be converted to JPG "
              f"(quality {args.quality}, metadata stripped).")
        print("ONIZLEME: uygulamak icin / to apply:  --apply")
        sys.exit(0)

    ok = fail = in_bytes = out_bytes = 0
    for src, dst, sz in plan:
        try:
            convert(ff, src, dst, args.quality)
            out_sz = os.path.getsize(dst)
            in_bytes += sz
            out_bytes += out_sz
            ok += 1
            print(f"  \u2714 {os.path.basename(src)} -> {os.path.basename(dst)}: {human(sz)} -> {human(out_sz)}")
        except Exception as e:
            fail += 1
            print(f"  \u2718 {os.path.basename(src)}: {e}")

    print(f"\nDone: {ok} converted, {fail} failed, {skipped} skipped "
          f"({human(in_bytes)} -> {human(out_bytes)}).")
    if fail:
        sys.exit(2)
    print(f"\nMade with \u2764 by {AUTHOR} - {INSTAGRAM}")


if __name__ == "__main__":
    main()
