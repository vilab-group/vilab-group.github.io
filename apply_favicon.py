#!/usr/bin/env python3
"""
apply_favicon.py — 로고 파일 하나로 사이트에 필요한 아이콘 전부를 생성합니다.

    python3 apply_favicon.py my-logo.png
    python3 apply_favicon.py favicon.ico --plate "#FFFFFF"

권장 원본: 512x512 이상 PNG(배경 투명) 또는 SVG를 래스터화한 PNG.
원본이 작으면 확대해서 만들지만, 큰 사이즈에서 흐려집니다.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "assets" / "img"


def load_largest(path: Path) -> Image.Image:
    """ICO는 여러 해상도를 품고 있으므로 가장 큰 것을 꺼냅니다."""
    im = Image.open(path)
    if im.format == "ICO":
        sizes = sorted(im.info.get("sizes", [im.size]))
        im.size = sizes[-1]
        im.load()
    return im.convert("RGBA")


def fit(src: Image.Image, size: int, pad: float, plate=None) -> Image.Image:
    """정사각 캔버스 중앙에 배치. plate가 있으면 불투명 배경을 깝니다."""
    inner = max(1, int(round(size * (1 - 2 * pad))))
    art = src.resize((inner, inner), Image.LANCZOS)
    if src.width < inner:  # 확대했다면 약간 선명하게
        art = art.filter(ImageFilter.UnsharpMask(radius=1.2, percent=70, threshold=2))
    out = Image.new("RGBA", (size, size), plate or (0, 0, 0, 0))
    off = (size - inner) // 2
    out.alpha_composite(art, (off, off))
    return out


def hex_rgba(s: str):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="로고 파일 (png / ico / jpg)")
    ap.add_argument("--plate", default="#FFFFFF",
                    help="apple-touch-icon 배경색. iOS는 투명을 검정으로 칠하므로 필요합니다.")
    ap.add_argument("--pad", type=float, default=0.10,
                    help="touch icon 여백 비율 (기본 0.10)")
    a = ap.parse_args()

    src_path = Path(a.source)
    if not src_path.exists():
        print(f"파일을 찾을 수 없습니다: {src_path}", file=sys.stderr)
        return 1

    src = load_largest(src_path)
    plate = hex_rgba(a.plate)
    IMG.mkdir(parents=True, exist_ok=True)

    if max(src.size) < 512:
        print(f"! 원본이 {src.size[0]}x{src.size[1]}입니다. 512x512 이상을 쓰면 "
              f"큰 아이콘이 훨씬 선명해집니다.")

    # 탭 아이콘 — 투명 배경 유지
    fit(src, 16, 0.0).save(IMG / "favicon-16.png")
    fit(src, 32, 0.0).save(IMG / "favicon-32.png")
    fit(src, 64, 0.0).save(IMG / "favicon.ico",
                           sizes=[(16, 16), (32, 32), (48, 48)])
    fit(src, 64, 0.0).save(ROOT / "favicon.ico",
                           sizes=[(16, 16), (32, 32), (48, 48)])

    # Safari 북마크 / iOS 홈 화면 — 반드시 불투명, 모서리는 iOS가 깎습니다
    fit(src, 180, a.pad, plate).convert("RGB").save(IMG / "apple-touch-icon.png")

    # Android / PWA
    fit(src, 192, a.pad, plate).convert("RGB").save(IMG / "icon-192.png")
    fit(src, 512, a.pad, plate).convert("RGB").save(IMG / "icon-512.png")

    # 헤더 로고 — 밝은 남색 배경 위에 얹히므로 투명 유지
    fit(src, 128, 0.0).save(IMG / "brand-mark.png")

    print("생성 완료:")
    for p in ["favicon.ico"]:
        print(f"  {p:34s} {(ROOT / p).stat().st_size:>7,}B")
    for p in ["favicon-16.png", "favicon-32.png", "favicon.ico",
              "apple-touch-icon.png", "icon-192.png", "icon-512.png",
              "brand-mark.png"]:
        print(f"  assets/img/{p:23s} {(IMG / p).stat().st_size:>7,}B")
    print("\n확인: python3 build_preview.py 후 preview.html 열기")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
