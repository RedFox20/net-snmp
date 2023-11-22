import mama
from mama.utils.system import console
from mama.utils.gnu_project import BuildProduct

# Explore Mama docs at https://github.com/RedFox20/Mama
class netsnmp(mama.BuildTarget):

    local_workspace = 'packages'

    def init(self):
        self.netsnmp = self.gnu_project('net-snmp', '5.9.4',
            url='http://kratt.codefox.ee/linux/{{project}}.tar.gz',
            build_products=[
                BuildProduct('{{installed}}/lib/libnetsnmp.a', None),
            ])

    def settings(self):
        self.config.prefer_gcc(self.name)
        if self.mips:
            self.config.set_mips_toolchain('mipsel')

    def build(self):
        if self.netsnmp.should_build():
            opts  = '--disable-shared --enable-static '
            opts += '--disable-scripts --disable-manuals --disable-mibs '
            opts += '--disable-ipv6 --disable-embedded-perl --without-pcre '
            self.netsnmp.build(opts)
        else:
            console('lib/libnetsnmp.a already built', color='green')

    def package(self):
        self.export_include('net-snmp-built/include', build_dir=True)
        self.export_asset('net-snmp-built/bin/snmpget', category='bin', build_dir=True)
        self.export_asset('net-snmp-built/bin/snmpset', category='bin', build_dir=True)

        self.export_lib('net-snmp-built/lib/libnetsnmp.a', build_dir=True)
        self.export_lib('net-snmp-built/lib/libnetsnmpmibs.a', build_dir=True)
        self.export_lib('net-snmp-built/lib/libnetsnmphelpers.a', build_dir=True)
