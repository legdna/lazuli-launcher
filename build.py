import subprocess
import json

with open("data/config.json", 'r') as config_file:
    config = json.load(config_file)

# Configuration des chemins
MSYS64_PATH = "C:/msys64/ucrt64"
MSYS64_BIN_PATH = "C:/msys64/usr/bin"
MSYS64_UCRT64_BIN_PATH = "C:/msys64/ucrt64/bin"

APP_NAME = "Oraclès Launcher"
LAUNCHER_VERSION = config["launcher"]["VERSION"]
LAUNCHER_RELEASE_TYPE = config["launcher"]["RELEASE_TYPE"]
ICON_PATH = "data/oracles.ico"
SOURCE_FILE = "src/oracles.py"

# Commande GResources
gresources_cmd = [
    "glib-compile-resources",
    "--target=data/oracles.gresource",
    "--sourcedir=data",
    "data/oracles.gresource.xml"
]

# Commande Nuitka
nuitka_cmd = [
    "nuitka",
#    "--onefile",
    "--standalone",
#    "--windows-disable-console",
    "--follow-imports",

    # Information sur l'application
    f"--output-filename={APP_NAME}.exe",
    f"--product-version={LAUNCHER_VERSION}",
    #f"--windows-file-description={APP_NAME} {LAUNCHER_VERSION}{LAUNCHER_RELEASE_TYPE}",
    f"--windows-icon-from-ico={ICON_PATH}",

    # ------------------------------------------------------------------------------------
    # > -- PACKAGES -- <
    # ------------------------------------------------------------------------------------

    "--include-package=gi",
    "--include-package-data=minecraft_launcher_lib",
    
    # ------------------------------------------------------------------------------------
    # > -- LIBRAIRIES -- <
    # ------------------------------------------------------------------------------------

    f"--include-data-files={MSYS64_PATH}/bin/libgio-2.0-0.dll=libgio-2.0-0.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libgdk_pixbuf-2.0-0.dll=libgdk_pixbuf-2.0-0.dll",
    f"--include-data-files={MSYS64_PATH}/bin/gdbus.exe=gdbus.exe",

    # ------------------------------------------------------------------------------------
    # > -- LIBGTK -- <
    # ------------------------------------------------------------------------------------

    f"--include-data-files={MSYS64_PATH}/bin/libgtk-4-1.dll=libgtk-4-1.dll",

    # Dépendances de libgtk
    f"--include-data-files={MSYS64_PATH}/bin/libcairo-script-interpreter-2.dll=libcairo-script-interpreter-2.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libjson-glib-1.0-0.dll=libjson-glib-1.0-0.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libgraphene-1.0-0.dll=libgraphene-1.0-0.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libepoxy-0.dll=libepoxy-0.dll",
    #f"--include-data-files={MSYS64_PATH}/bin/librsvg-2-2.dll=librsvg-2-2.dll",

    # Dépendances de libgtk > libcairo
    f"--include-data-files={MSYS64_PATH}/bin/liblzo2-2.dll=liblzo2-2.dll",

    # ------------------------------------------------------------------------------------
    # > -- LIBADWAITA -- <
    # ------------------------------------------------------------------------------------
    
    f"--include-data-files={MSYS64_PATH}/bin/libadwaita-1-0.dll=libadwaita-1-0.dll",

    # Dépendances de libadwaita
    f"--include-data-files={MSYS64_PATH}/bin/libappstream-5.dll=libappstream-5.dll",
    
    # Dépendances de libadwaita > libappstream
    f"--include-data-files={MSYS64_PATH}/bin/libcurl-4.dll=libcurl-4.dll",
    #f"--include-data-files={MSYS64_PATH}/bin/libgettextlib-0-24.dll=libgettextlib-0-24.dll",
    #f"--include-data-files={MSYS64_PATH}/bin/libgettextpo-0.dll=libgettextpo-0.dll",
    #f"--include-data-files={MSYS64_PATH}/bin/libgettextsrc-0-24.dll=libgettextsrc-0-24.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libxml2-2.dll=libxml2-2.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libxmlb-2.dll=libxmlb-2.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libyaml-0-2.dll=libyaml-0-2.dll",

    # Dépendances de libadwaita > libappstream > libcurl
    f"--include-data-files={MSYS64_PATH}/bin/libcares-2.dll=libcares-2.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libpsl-5.dll=libpsl-5.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libunistring-5.dll=libunistring-5.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libssh2-1.dll=libssh2-1.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libidn2-0.dll=libidn2-0.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libnghttp2-14.dll=libnghttp2-14.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libnghttp3-9.dll=libnghttp3-9.dll",

    # ------------------------------------------------------------------------------------
    # > -- LIBPANGO -- <
    # ------------------------------------------------------------------------------------

    f"--include-data-files={MSYS64_PATH}/bin/libpango-1.0-0.dll=libpango-1.0-0.dll",

    # Dépendances de libpango
    f"--include-data-files={MSYS64_PATH}/bin/libpangocairo-1.0-0.dll=libpangocairo-1.0-0.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libpangoft2-1.0-0.dll=libpangoft2-1.0-0.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libpangowin32-1.0-0.dll=libpangowin32-1.0-0.dll",

    f"--include-data-files={MSYS64_PATH}/bin/libharfbuzz-gobject-0.dll=libharfbuzz-gobject-0.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libharfbuzz-subset-0.dll=libharfbuzz-subset-0.dll",

    f"--include-data-files={MSYS64_PATH}/bin/libthai-0.dll=libthai-0.dll",
    f"--include-data-files={MSYS64_PATH}/bin/libfribidi-0.dll=libfribidi-0.dll",

    # Dépendances de libpango > libthai
    f"--include-data-files={MSYS64_PATH}/bin/libdatrie-1.dll=libdatrie-1.dll",

    # ------------------------------------------------------------------------------------
    # > -- DATAS -- <
    # ------------------------------------------------------------------------------------

    #f"--include-data-dir={MSYS64_PATH}/share/glib-2.0/schemas=share/glib-2.0/schemas",
    "--include-data-dir=data/background=data/background",
    "--include-data-files=data/oracles.gresource=data/oracles.gresource",

    SOURCE_FILE
]

# Exécution avec gestion d'erreur
try:
    subprocess.run(gresources_cmd, check=True)
    subprocess.run(nuitka_cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"\033[91mErreur de compilation : {e}\033[0m")
    exit(1)
