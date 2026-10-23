import subprocess
import sys
import os
import shutil

def kill_running_exe():
    try:
        subprocess.run(["taskkill", "/f", "/im", "TrackDrop.exe"], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Movcud islek proqramlari sonlandirmaga calisdiq.")
    except Exception:
        pass

def build():
    kill_running_exe()
    
    src_dir = os.path.dirname(os.path.abspath(__file__))  # C:\Users\nakid\Desktop\mp3app\src
    root_dir = os.path.dirname(src_dir)                   # C:\Users\nakid\Desktop\mp3app
    
    script_path = os.path.join(src_dir, "main.py")
    icon_path = os.path.join(root_dir, "web", "assets", "trackdrop_icon.ico")
    font_path = os.path.join(src_dir, "MontenegrinGothicOne-Regular.ttf")
    web_dir = os.path.join(root_dir, "web")
    
    # Kohne CaspianCrime ve lazimsiz fayllari silirik
    old_files = [
        os.path.join(root_dir, "CaspianCrime_Downloader.exe"),
        os.path.join(root_dir, "CaspianCrime_Downloader_Yeni.exe"),
        os.path.join(root_dir, "TrackDrop_Yeni.exe"),
        os.path.join(src_dir, "CaspianCrime_Downloader.spec")
    ]
    for f in old_files:
        if os.path.exists(f):
            try:
                os.remove(f)
                print(f"Kohnelmis fayl silindi: {os.path.basename(f)}")
            except Exception as e:
                print(f"Kohnelmis fayli silerken xeta: {e}")
                
    # Build qovlugunu temizleyirik
    build_dir = os.path.join(src_dir, "build")
    if os.path.exists(build_dir):
        try:
            shutil.rmtree(build_dir)
            print("Kohne build qovlugu silindi.")
        except Exception as e:
            print(f"Build qovlugu siline bilmedi: {e}")
            
    # PyInstaller emrleri
    # .venv Python interpreterini secmek ucun yoxlayiriq
    python_exe = sys.executable
    venv_python = os.path.join(root_dir, ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        python_exe = venv_python
        
    cmd = [
        python_exe, "-m", "PyInstaller",
        "--clean",
        "--onefile",
        "--noconsole",
        f"--icon={icon_path}",
        f"--add-data={icon_path};.",
        f"--add-data={font_path};.",
        f"--add-data={web_dir};web",
        "--name=TrackDrop",
        f"--distpath={root_dir}",
        f"--workpath={build_dir}",
        f"--specpath={src_dir}",
        script_path
    ]
    
    print("Icra edilen emr:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=src_dir)
    if result.returncode == 0:
        print("\n=== UGURLU ===")
        print("EXE fayli ugurla yaradildi!")
        print(f"Faylin yerlesdiyi yer: {os.path.join(root_dir, 'TrackDrop.exe')}")
    else:
        print("\n=== XETA ===")
        print("EXE faylinin yigilmasi zamani xeta bas verdi.")

if __name__ == "__main__":
    build()
