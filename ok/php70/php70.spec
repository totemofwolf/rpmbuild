# php70 spec file, used to drive rpmbuild

%define version 7.0.18
%define so_version 7
%define release 1

%define php_install_dir /production/server/php

Name: php
Summary: PHP: Hypertext Preprocessor

License:    GPL
Group: Development/Languages
Version: %{version}
Release: %{release}

URL: http://cn2.php.net/distributions/%{name}-%{version}.tar.gz
Source: %{name}-%{version}.tar.gz

Packager: PHP Group <group@php.net>
#BuildRoot: /var/tmp/php-%{version}
#URL: http://www.php.net/

#
# Description
#

%description
PHP is an HTML-embedded scripting language. Much of its syntax is
borrowed from C, Java and Perl with a couple of unique PHP-specific
features thrown in. The goal of the language is to allow web
developers to write dynamically generated pages quickly.

#
# Include dependencies manually
#

BuildRequires: bison >= 2.4.0
BuildRequires: libcurl-devel

%{?with-ldap:BuildRequires: openldap-devel >= 2.4.40}
%{?with-ldap:Requires: openldap >= 2.4.40}

%{?with-ldap-sasl:BuildRequires: cyrus-sasl-ldap >= 2.1.23}
#%{?with-ldap-sasl:Requires: }

%{?with-openssl:BuildRequires: openssl-devel >= 1.0.1e-48}
%{?with-openssl:Requires: openssl >= 1.0.1e-48}


# libgd = gd + gd-devel
%{?with-gd:BuildRequires: libgd >= 2.2.2}

#
# Build
#

%prep
%setup -q -n %{name}-%{version}

%build
./configure \
  --prefix=%{php_install_dir} \
  --with-config-file-path=%{php_install_dir}/etc \
  --with-config-file-scan-dir=%{php_install_dir}/etc/php.d \
  --disable-debug \
  --disable-fileinfo \
  --disable-ipv6 \
  --disable-maintainer-zts \
  --enable-bcmath \
  --enable-calendar \
  --enable-fpm \
  --enable-ftp \
  --enable-gd-jis-conv \
  --enable-gd-native-ttf \
  --enable-inline-optimization \
  --enable-mbregex \
  --enable-mbstring \
  --enable-mysqlnd \
  --enable-pcntl \
  --enable-shmop \
  --enable-soap \
  --enable-sockets \
  --enable-static \
  --enable-sysvsem \
  --enable-wddx \
  --enable-xml \
  --enable-zip \
  --with-curl \
  --with-gd=/usr \
  --with-gettext \
  --with-iconv \
  --with-libxml-dir=/usr \
  --with-mcrypt \
  --with-mhash \
  --with-mysqli=mysqlnd \
  --with-openssl \
  --with-pdo-mysql=mysqlnd \
  --with-xmlrpc \
  --with-xpm-dir \
  --with-freetype-dir \
  --with-webp-dir \
  --with-jpeg-dir \
  --with-png-dir \
  --with-zlib \
  --without-pear

make ZEND_EXTRA_LIBS='-liconv' %{_smp_mflags}

# --datarootdir=/usr/share \
# --includedir=/usr/local/include \

# --target=x86_64-redhat-linux-gnu \
# --build=x86_64-redhat-linux-gnu \
# --host=x86_64-redhat-linux-gnu \
# --
# checking build system type... x86_64-unknown-linux-gnu
# checking host system type... x86_64-unknown-linux-gnu
# checking target system type... x86_64-unknown-linux-gnu

#
# Installation section
#

%install
mkdir -pv %{buildroot}%{_initrddir}
%{__make} install INSTALL_ROOT="%{buildroot}"

# Install init script
%__install -c -d -m 755 %{buildroot}/etc/init.d
%__install -c -m 755 sapi/fpm/init.d.php-fpm %{buildroot}/etc/init.d/php-fpm
# sapi/fpm/php-fpm.service
%__install -c -d -m 755 %{buildroot}/production/server/php/etc
%__install -c -m 644 php.ini-production %{buildroot}/production/server/php/etc/php.ini-production

#
# Clean section
#

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
make distclean

#
# Handle the init script
#

%post
/sbin/chkconfig --add php-fpm

%preun
/etc/init.d/php-fpm stop
/sbin/chkconfig --del php-fpm

#
# Files section
#

%files
%defattr(-,root,root,-)
/production/server/php
/etc/init.d/php-fpm

# ---
#if test "x$OVERRIDE_OPTIONS" = "x"; then
#    ./configure --prefix=/usr --with-apxs=$APXS $OPTIONS
#else
#    ./configure $OVERRIDE_OPTIONS
#fi
