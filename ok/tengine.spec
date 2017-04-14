# This is a sample spec file for test rpm package
%define _user      www
%define _group     www
%define version    2.1.2

Name:       tengine
Version:    %{version}
Release:    1
Vendor:     Taobao
Summary:    GUN Tengine X86_64
License:    GPL
Source:     tengine-%{version}.tar.gz
Group:      Application/WebServer
URL:        http://tengine.taobao.org/
# Packager:   gk.wl@qq.com

BuildRequires: autoconf
BuildRequires: automake

BuildRequires: openssl-devel
Requires: openssl

BuildRequires: pcre-devel
Requires: pcre

BuildRequires: libxml2-devel
Requires: libxml2

BuildRequires: libxslt-devel
Requires: libxslt

BuildRequires: zlib-devel
Requires: zlib

BuildRequires: jemalloc-devel
Requires: jemalloc

Requires: libX11
Requires: libX11-common
Requires: libXau
Requires: libjpeg-turbo
Requires: libpng
Requires: libxcb
Requires: fontconfig

%description
Taobao tengine package

# yum install jemalloc-devel pcre-devel zlib-devel openssl-devel

%prep
%setup -q
./configure \
  --prefix=/production/server/nginx \
  --with-cc-opt='-O2 -fstack-protector --param=ssp-buffer-size=4 -Wformat -Werror=format-security -D_FORTIFY_SOURCE=2' \
  --with-ld-opt='-Wl,-Bsymbolic-functions -Wl,-z,relro' \
  --user=www \
  --group=www \
  --with-jemalloc \
  --with-http_dyups_module \
  --with-http_stub_status_module \
  --with-http_ssl_module \
  --with-http_gzip_static_module \
  --with-http_concat_module \
  --with-http_realip_module \
  --with-http_v2_module \
  --with-http_sysguard_module \
  --with-http_secure_link_module \
  --with-syslog \
  --without-http-cache \
  --without-poll_module \
  --without-select_module \
  --without-mail_pop3_module \
  --without-mail_imap_module \
  --without-mail_smtp_module \
  --with-cpu-opt=opteron

# --pid-path=/var/run/nginx.pid \
# --with-pcre-jit \
# --with-cpu-opt=opteron \
# --with-http_spdy_module replaced by httpv2

# --with-http_lua_module \
# export LUAJIT_LIB=/usr/local/lib
# export LUAJIT_INC=/usr/local/include/luajit-2.0
# make clean; CC=clang; CFLAGS="-g -O0" ./configure --prefix=$PWD/out --enable-mods-static=all --with-ld-opt="-Wl,-rpath,/usr/local/lib" --with-debug --with-http_upstream_check_module --with-http_v2_module --with-http_dyups_module --with-http_dyups_lua_api --with-http_sysguard_module --add-module=/home/lhanjian/ali/tengine_now/ngx_devel_kit-master && make -j4

make %{?_smp_mflags}


#
# Installation section
#

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Install link
# %__install -c -d -m 755 %{buildroot}/production/server/tengine-2.1.2

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
make clean

%pre
grep -q ^%{_group}: /etc/group || /usr/sbin/groupadd %{_group}
grep -q ^%{_user}: /etc/passwd || /usr/sbin/useradd -g %{_group} -M -s /sbin/nologin -M %{_user}
# rm -fv /production/server/nginx
# ln -sf /production/server/tengine-2.1.2 /production/server/nginx

%files
%defattr (-,root,root)
/production/server/nginx
# /production/server/tengine-2.1.2

%changelog
