from conans import ConanFile, tools

class FipscanisterConan ( ConanFile ):
    name = "fipscanister"
    version = '2.0.16'
    license = "OpenSSL"
    description = "OpenSSL fipscanister module"
    settings = "os", "compiler", "arch"
    options = {
        "no_asm": [ True, False ],
    }
    default_options = "no_asm=False"

    def configure ( self ):
        del self.settings.compiler.libcxx

    def build_requirements ( self ):
        if self.settings.compiler == "Visual Studio":
            self.build_requires ( "strawberryperl/5.26.0@conan/stable" )
            if not self.options.no_asm and self.settings.arch in [ "x86", "x86_64" ]:
                self.build_requires ( "nasm/2.13.01@conan/stable" )

    def source ( self ):
        url = "https://www.openssl.org/source/openssl-fips-{0}.tar.gz".format ( self.version )
        self.output.info ( "Downloading: %s" % url )
        tools.get ( url )
        print ( "" )

    def build ( self ):
        with tools.environment_append (
            {
                "FIPSDIR": self.package_folder,
            }
        ):
            if self.settings.os == "Windows":
                self.build_windows ( )
            else:
                self.build_with_configure ( self.noasm )

    def run_in_src ( self, command ):
        with tools.chdir ( "openssl-fips-{0}".format ( self.version ) ):
            self.run ( command )

    @property
    def noasm ( self ):
        return "no-asm" if self.options.no_asm else ""

    def build_with_configure ( self, config_options_string ):
        if self.should_configure:
            self.run_in_src ( "./config %s" % config_options_string )
        if self.should_build:
            self.run_in_src ( "make" ) 
        if self.should_install:
            self.run_in_src ( "make install" )

    def build_windows ( self ):
        arch_fix = ""
        if self.settings.arch == "x86_64":
            arch_fix = "set PROCESSOR_ARCHITECTURE=AMD64 && "
        self.run_in_src ( arch_fix + "ms\\do_fips " + self.noasm )

    def package_info ( self ):
        self.env_info.FIPSDIR = self.package_folder
