import mama
import os
from mama.utils.system import console
from mama.utils.gnu_project import BuildProduct
from mama.artifactory import artifactory_fetch_and_reconfigure

# Explore Mama docs at https://github.com/RedFox20/Mama
class netsnmp(mama.BuildTarget):

    local_workspace = 'packages'

    def init(self):
        self.netsnmp = self.gnu_project('net-snmp', '5.9.4',
            url='http://kratt.codefox.ee/linux/{{project}}.tar.gz',
            build_products=[
                BuildProduct('{{installed}}/include', '{{build}}', is_dir=True),
                BuildProduct('{{installed}}/lib/libnetsnmp.a', '{{build}}/lib/libnetsnmp.a'),
                BuildProduct('{{installed}}/lib/libnetsnmpmibs.a', '{{build}}/lib/libnetsnmpmibs.a'),
                BuildProduct('{{installed}}/lib/libnetsnmphelpers.a', '{{build}}/lib/libnetsnmphelpers.a'),
                BuildProduct('{{installed}}/bin/snmpget', '{{build}}/bin/snmpget'),
                BuildProduct('{{installed}}/bin/snmpset', '{{build}}/bin/snmpset'),
                BuildProduct('{{installed}}/bin/snmpwalk', '{{build}}/bin/snmpwalk'),
                BuildProduct('{{installed}}/bin/snmpbulkget', '{{build}}/bin/snmpbulkget'),
            ])

    def settings(self):
        self.config.prefer_gcc(self.name)
        if self.mips:
            self.config.set_mips_toolchain('mipsel')

    def build(self):
        if self.dep.can_fetch_artifactory(True, 'BUILD'):
            fetched, _ =  artifactory_fetch_and_reconfigure(self)
            if fetched:
                console('lib/libnetsnmp.a already built', color='green')

        if self.netsnmp.should_build():
            opts  = '--disable-shared --enable-static '
            opts += '--disable-scripts --disable-manuals --disable-mibs '
            opts += '--disable-ipv6 --disable-embedded-perl --without-pcre '
            self.netsnmp.build(opts)
            self.netsnmp.deploy_all_products()
        else:
            console('lib/libnetsnmp.a already built', color='green')

    def package(self):
        self.export_include('include', build_dir=True)
        self.export_asset('bin/snmpget', category='bin', build_dir=True)
        self.export_asset('bin/snmpset', category='bin', build_dir=True)
        self.export_asset('bin/snmpwalk', category='bin', build_dir=True)
        self.export_asset('bin/snmpbulkget', category='bin', build_dir=True)

        self.export_lib('lib/libnetsnmp.a', build_dir=True)
        self.export_lib('lib/libnetsnmpmibs.a', build_dir=True)
        self.export_lib('lib/libnetsnmphelpers.a', build_dir=True)
