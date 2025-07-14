import subprocess
import json
import platform

with open("data/config.json", 'r') as config_file:
    config = json.load(config_file)

os_release = platform.system()

match os_release:
    case "Windows":
        BIN_PATH = "C:/msys64/ucrt64/bin"
        LIB_PATH = "C:/msys64/ucrt64/bin"

        BINS = ["gdbus", "gspawn-win64-helper", "gspawn-win64-helper-console"]
        LIBS = ["libgio-2.0-0", "libgdk_pixbuf-2.0-0", "libgtk-4-1", "libcairo-script-interpreter-2", "libjson-glib-1.0-0", "libgraphene-1.0-0", "libepoxy-0", "liblzo2-2", "libadwaita-1-0", "libappstream-5", "libcurl-4", "libxml2-2", "libxmlb-2", "libyaml-0-2", "libcares-2", "libpsl-5", "libunistring-5", "libssh2-1", "libidn2-0", "libnghttp2-14", "libnghttp3-9", "libpango-1.0-0", "libpangocairo-1.0-0", "libpangoft2-1.0-0", "libpangowin32-1.0-0", "libharfbuzz-gobject-0", "libharfbuzz-subset-0", "libthai-0", "libfribidi-0", "libdatrie-1"]

        BIN_EXT = ".exe"
        LIB_EXT = ".dll"
    case "Linux":
        BIN_PATH = ""
        LIB_PATH = ""

        BINS = ["gdbus"]
        LIBS = []

        BIN_EXT = ""
        LIB_EXT = ".so"
    case "Darwin":
        BIN_PATH = "/opt/homebrew/bin"
        LIB_PATH = "/opt/homebrew/lib"

        BINS = ["gdbus"]
        LIBS = ["libgio-2.0.0", "libgdk_pixbuf-2.0.0", "libgtk-4.1", "libcairo-script-interpreter.2", "libjson-glib-1.0.0", "libgraphene-1.0.0", "libepoxy.0", "liblzo2.2", "libadwaita-1.0", "libappstream.5", "libxmlb.2", "libyaml-0.2", "libunistring.5", "libssh2.1", "libnghttp2.14", "libpango-1.0.0", "libpangocairo-1.0.0", "libpangoft2-1.0.0", "libharfbuzz-gobject.0", "libharfbuzz-subset.0", "libfribidi.0"] # "libcurl.4", "libxml2.2", "libcares.2", "libpsl.5", "libidn2.0", "libnghttp3.9", "libthai.0", "libdatrie.1"

        BIN_EXT = ""
        LIB_EXT = ".dylib"

# Configuration des chemins
#MSYS64_BIN_PATH = "C:/msys64/usr/bin"
#MSYS64_UCRT64_BIN_PATH = "C:/msys64/ucrt64/bin"

APP_NAME = "Lazuli Launcher"
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
    "--windows-console-mode=disable",
    "--follow-imports",
#    "--no-deployment-flag=self-execution",

    # Information sur l'application
    f"--output-filename={APP_NAME}{BIN_EXT}",
    f"--product-version={LAUNCHER_VERSION}",
    #f"--windows-file-description={APP_NAME} {LAUNCHER_VERSION}{LAUNCHER_RELEASE_TYPE}",
    f"--windows-icon-from-ico={ICON_PATH}",
    f"--output-dir=./dist",

    # ------------------------------------------------------------------------------------
    # > -- PACKAGES -- <
    # ------------------------------------------------------------------------------------

    "--include-package=gi",
    "--include-package-data=minecraft_launcher_lib",
    
    # ------------------------------------------------------------------------------------
    # > -- LIBRAIRIES -- <
    # ------------------------------------------------------------------------------------
        
    #f"--include-data-files={LIB_PATH}/libgio-2.0-0{LIB_EXT}=libgio-2.0-0{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libgdk_pixbuf-2.0-0{LIB_EXT}=libgdk_pixbuf-2.0-0{LIB_EXT}",
    #f"--include-data-files={BIN_PATH}/gdbus{BIN_EXT}=gdbus{BIN_EXT}",
    #f"--include-data-files={BIN_PATH}/gspawn-win64-helper{BIN_EXT}=gspawn-win64-helper{BIN_EXT}",
    #f"--include-data-files={BIN_PATH}/gspawn-win64-helper-console{BIN_EXT}=gspawn-win64-helper-console{BIN_EXT}",

    # ------------------------------------------------------------------------------------
    # > -- LIBGTK -- <
    # ------------------------------------------------------------------------------------

    #f"--include-data-files={LIB_PATH}/libgtk-4-1{LIB_EXT}=libgtk-4-1{LIB_EXT}",

    # Dépendances de libgtk
    #f"--include-data-files={LIB_PATH}/libcairo-script-interpreter-2{LIB_EXT}=libcairo-script-interpreter-2{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libjson-glib-1.0-0{LIB_EXT}=libjson-glib-1.0-0{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libgraphene-1.0-0{LIB_EXT}=libgraphene-1.0-0{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libepoxy-0{LIB_EXT}=libepoxy-0{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/librsvg-2-2{LIB_EXT}=librsvg-2-2{LIB_EXT}",

    # Dépendances de libgtk > libcairo
    #f"--include-data-files={LIB_PATH}/liblzo2-2{LIB_EXT}=liblzo2-2{LIB_EXT}",

    # ------------------------------------------------------------------------------------
    # > -- LIBADWAITA -- <
    # ------------------------------------------------------------------------------------
    
    #f"--include-data-files={LIB_PATH}/libadwaita-1-0{LIB_EXT}=libadwaita-1-0{LIB_EXT}",

    # Dépendances de libadwaita
    #f"--include-data-files={LIB_PATH}/libappstream-5{LIB_EXT}=libappstream-5{LIB_EXT}",
    
    # Dépendances de libadwaita > libappstream
    #f"--include-data-files={LIB_PATH}/libcurl-4{LIB_EXT}=libcurl-4{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libgettextlib-0-24{LIB_EXT}=libgettextlib-0-24{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libgettextpo-0{LIB_EXT}=libgettextpo-0{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libgettextsrc-0-24{LIB_EXT}=libgettextsrc-0-24{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libxml2-2{LIB_EXT}=libxml2-2{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libxmlb-2{LIB_EXT}=libxmlb-2{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libyaml-0-2{LIB_EXT}=libyaml-0-2{LIB_EXT}",

    # Dépendances de libadwaita > libappstream > libcurl
    #f"--include-data-files={LIB_PATH}/libcares-2{LIB_EXT}=libcares-2{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libpsl-5{LIB_EXT}=libpsl-5{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libunistring-5{LIB_EXT}=libunistring-5{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libssh2-1{LIB_EXT}=libssh2-1{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libidn2-0{LIB_EXT}=libidn2-0{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libnghttp2-14{LIB_EXT}=libnghttp2-14{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libnghttp3-9{LIB_EXT}=libnghttp3-9{LIB_EXT}",

    # ------------------------------------------------------------------------------------
    # > -- LIBPANGO -- <
    # ------------------------------------------------------------------------------------

    #f"--include-data-files={LIB_PATH}/libpango-1.0-0{LIB_EXT}=libpango-1.0-0{LIB_EXT}",

    # Dépendances de libpango
    #f"--include-data-files={LIB_PATH}/libpangocairo-1.0-0{LIB_EXT}=libpangocairo-1.0-0{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libpangoft2-1.0-0{LIB_EXT}=libpangoft2-1.0-0{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libpangowin32-1.0-0{LIB_EXT}=libpangowin32-1.0-0{LIB_EXT}",

    #f"--include-data-files={LIB_PATH}/libharfbuzz-gobject-0{LIB_EXT}=libharfbuzz-gobject-0{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libharfbuzz-subset-0{LIB_EXT}=libharfbuzz-subset-0{LIB_EXT}",

    #f"--include-data-files={LIB_PATH}/libthai-0{LIB_EXT}=libthai-0{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libfribidi-0{LIB_EXT}=libfribidi-0{LIB_EXT}",

    # Dépendances de libpango > libthai
    #f"--include-data-files={LIB_PATH}/libdatrie-1{LIB_EXT}=libdatrie-1{LIB_EXT}",

    # ------------------------------------------------------------------------------------
    # > -- LIBSOUP -- <
    # ------------------------------------------------------------------------------------

    #f"--include-data-files={LIB_PATH}/libsoup-3.0-0{LIB_EXT}=libsoup-3.0-0{LIB_EXT}",

    # Dépendances de libsoup
    #f"--include-data-files={LIB_PATH}/libproxy-1{LIB_EXT}=libproxy-1{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libgnutls-30{LIB_EXT}=libgnutls-30{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libproxy-1{LIB_EXT}=libproxy-1{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libsqlite3-0{LIB_EXT}=libsqlite3-0{LIB_EXT}",

    # Dépendances de libsoup > glib-networking
    #f"--include-data-files={BIN_PATH}/brotli{BIN_EXT}=brotli{BIN_EXT}",
    #f"--include-data-files={LIB_PATH}/libgmp-10{LIB_EXT}=libgmp-10{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libtasn1-6{LIB_EXT}=libtasn1-6{LIB_EXT}",
    #f"--include-data-files={LIB_PATH}/libnettle-8{LIB_EXT}=libnettle-8{LIB_EXT}",

    # ------------------------------------------------------------------------------------
    # > -- DATAS -- <
    # ------------------------------------------------------------------------------------

    #f"--include-data-dir={BIN_PATH}/share/glib-2.0/schemas=share/glib-2.0/schemas",
    "--include-data-dir=data/background=data/background",
    "--include-data-files=data/oracles.gresource=data/oracles.gresource",
]

for bin in BINS:
    nuitka_cmd.append(f"--include-data-files={BIN_PATH}/{bin}{BIN_EXT}={bin}{BIN_EXT}")

for lib in LIBS:
    nuitka_cmd.append(f"--include-data-files={LIB_PATH}/{lib}{LIB_EXT}={lib}{LIB_EXT}")

nuitka_cmd.append(SOURCE_FILE)

# Exécution avec gestion d'erreur
try:
    subprocess.run(gresources_cmd, check=True)
    subprocess.run(nuitka_cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"\033[91mErreur de compilation : {e}\033[0m")
    exit(1)
