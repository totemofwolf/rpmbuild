Name:       tengine
Version:    2.1.2
Release:    1
#Vendor:     Taobao
Summary:    GUN Tengine X86_64
License:    GPL
Source:     tengine-2.1.2.tar.gz
Group:      System Enviroment/Daemons
URL:        http://tengine.taobao.org/
#Packager:   gk.wl@qq.com
%description
Taobao tengine package


%prep
%setup -q
./configure --prefix=/usr/local/nginx --with-cc-opt='-O2 -fstack-protector --param=ssp-buffer-size=4 -Wformat -Werror=format-security -D_FORTIFY_SOURCE=2' --with-ld-opt='-Wl,-Bsymbolic-functions -Wl,-z,relro' --user=www --group=www --with-jemalloc --with-http_stub_status_module --with-openssl=/usr/local/src/sh-1.5.5/openssl-1.0.2j --with-http_gzip_static_module --with-http_concat_module --with-http_realip_module --with-http_v2_module --with-http_sysguard_module --with-syslog --with-http_secure_link_module --without-http-cache --without-poll_module --without-select_module --without-mail_pop3_module --without-mail_imap_module --without-mail_smtp_module

make
%install
make DESTDIR=$RPM_BUILD_ROOT install
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
make clean

%files
%defattr (-,root,root)
/usr/local/nginx/
