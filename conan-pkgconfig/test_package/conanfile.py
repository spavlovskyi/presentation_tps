from conans import ConanFile

class PkgconfigTestConan ( ConanFile ):
    settings = "arch", "os_build"
    generators = "virtualrunenv"
    no_copy_source = True
    def test ( self ):
        if self.settings.os_build == "Windows":
            self.run ( "pkg-config --version" )
