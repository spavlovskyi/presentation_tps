from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
import os

class PkgconfigConan ( ConanFile ):
    name = "pkg-config"
    version = "0.28"
    license = "GPL 2"
    description = "pkg-config is a helper tool used " \
        "when compiling applications and libraries"
    settings = "os", "arch"

    def build ( self ):
        if self.settings.os != "Windows":
            raise ConanInvalidConfiguration ( 'windows-only' )
        if self.settings.arch not in [ 'x86', 'x86_64' ]:
            raise ConanInvalidConfiguration ( 'intel-only' )
        url = "https://sourceforge.net/projects/pkgconfiglite/files/{0}-1/" \
            "pkg-config-lite-{0}-1_bin-win32.zip/download".format ( self.version )
        self.output.info ( "Downloading: %s" % url )
        tools.get ( url )
        print ( "" )

    def package ( self ):
        self.copy (
            "pkg-config.exe",
            dst="bin",
            src="pkg-config-lite-{0}-1/bin".format ( self.version )
        )

    def package_info ( self ):
        bin_folder = os.path.join ( self.package_folder, "bin" )
        self.env_info.path.append ( bin_folder )
