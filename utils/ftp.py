import ftplib
from ssl import SSLSocket
from io import StringIO, BytesIO
import csv


class ReusedSslSocket(SSLSocket):
    def unwrap(self):
        pass


class MyFTP_TLS(ftplib.FTP_TLS):
    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(
                conn,
                server_hostname=self.host,
                session=self.sock.session
            )
            conn.__class__ = ReusedSslSocket
        return conn, size




def get_ftp_file_as_buffer(hostname, file_path, user, pswd, debug=False):
    ftps = MyFTP_TLS(hostname)
    if debug:
        ftps.set_debuglevel(2)
    ftps.login(user, pswd)
    ftps.prot_p()
    print(ftps.dir())
    ftps.cwd('/')
    buffer = BytesIO()
    ftps.retrbinary('RETR /{file_path}'.format(**locals()), buffer.write)
    buffer.seek(0)
    return buffer
