# net-snmp
net-snmp package for mamabuild

## Adding to your project
```
class myproject(mama.BuildTarget):
    def dependencies(self):
        self.add_git('netsnmp', 'https://github.com/RedFox20/net-snmp.git')
```
