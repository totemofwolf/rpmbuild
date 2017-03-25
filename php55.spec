# php55 spec file, used to drive rpmbuild

%define version 5.5.38
%define so_version 5
%define release 0
%define svc_name php-fpm

#
# Define vendor type
#

%if "%{_vendor}" == "suse" || "%{_vendor}" == "pc"
%define VENDOR SuSE
%else
%define VENDOR %_vendor
%endif

Summary: PHP: Hypertext Preprocessor
Name: php
Version: %{version}
Release: %{release}
URL: http://www.php.net/get/php-%{version}.tar.gz/from/a/mirror
Source: php-5.5.38.tar.gz

License:    GPL
Group: Development/Languages
Vendor:     php.net
Packager: gk.wl@qq.com
BuildRoot:	%{_tmppath}/%{name}-%(id -un)
# BuildRoot: /var/tmp/php-%{version}
# Source0: http://www.php.net/get/php-%{version}.tar.gz/from/a/mirror
# Copyright:  The PHP license (see "LICENSE" file included in distribution)
# Icon: php.gif

#
# Include dependencies manually
#
BuildRequires: bison >= 2.4.0

%{?with-ldap:BuildRequires: openldap-devel >= 2.4.40}
%{?with-ldap:Requires: openldap >= 2.4.40}

%{?with-ldap-sasl:BuildRequires: cyrus-sasl-ldap >= 2.1.23}
#%{?with-ldap-sasl:Requires: }

%{?with-openssl:BuildRequires: openssl-devel >= 1.0.1e-48}
%{?with-openssl:Requires: openssl >= 1.0.1e-48}

# rpm -ivh libiconv-1.13.1-1.x86_64.rpm
%{!?without-iconv:BuildRequires: libiconv >= 1.13.1}
#%{!?without-iconv:Requires:}

# libgd = gd + gd-devel
%{?with-gd:BuildRequires: libgd >= 2.2.2}
#%{?with-gd:Requires:}


#
# Description
#

%description
PHP is an HTML-embedded scripting language. Much of its syntax is
borrowed from C, Java and Perl with a couple of unique PHP-specific
features thrown in. The goal of the language is to allow web
developers to write dynamically generated pages quickly.

#
# Build
#
%prep

%setup -q

%build
set -x
# ./buildconf
./configure --prefix=/usr/local --disable-debug --disable-fileinfo --disable-ipv6 --disable-maintainer-zts --enable-bcmath --enable-calendar --enable-fpm --enable-ftp --enable-gd-jis-conv --enable-gd-native-ttf --enable-inline-optimization --enable-mbregex --enable-mbstring --enable-opcache --enable-pcntl --enable-shmop --enable-soap --enable-sockets --enable-static --enable-sysvsem --enable-wddx --enable-xml --enable-zip --with-config-file-path=/usr/local/php/etc --with-curl --with-gd=/usr/local/libgd --with-gettext --with-iconv --with-libxml-dir=/usr --with-mcrypt --with-mhash --with-mysql=mysqlnd --with-mysqli=mysqlnd --with-openssl --with-pdo-mysql=mysqlnd --with-xmlrpc --with-zlib --without-pear

# centos7+
# --with-fpm-systemd

# with-openssl=/usr/include/openssl
# figure out configure options options based on what packages are installed
# to override, use the OVERRIDE_OPTIONS environment variable.  To add
# extra options, use the OPTIONS environment variable.
#test rpm -q MySQL-devel >&/dev/null && OPTIONS="$OPTIONS --with-mysql=shared"
#test rpm -q solid-devel >&/dev/null && OPTIONS="$OPTIONS --with-solid=shared,/home/solid"
#test rpm -q postgresql-devel >&/dev/null && OPTIONS="$OPTIONS --with-pgsql=shared"
#test rpm -q expat >&/dev/null && OPTIONS="$OPTIONS --with-xml=shared"
#if test "x$OVERRIDE_OPTIONS" = "x"; then
#    ./configure --prefix=/usr --with-apxs=$APXS $OPTIONS
#else
#    ./configure $OVERRIDE_OPTIONS
#fi

make ZEND_EXTRA_LIBS='-liconv' -j4

#
# Installation section
#

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
make DESTDIR=$RPM_BUILD_ROOT install

# Install man page
%__install -c -d -m 755 %{buildroot}%{_mandir}/man8
%__install -c -m 755 %{name}.8 %{buildroot}%{_mandir}/man8

# Install binary

# Install init script
%__install -c -d -m 755 %{buildroot}/etc/init.d
%__install -c -m 755 sapi/fpm/init.d.%{svc_name} %{buildroot}/etc/init.d/%{svc_name}
#php.ini-production
#./sapi/fpm/php-fpm.conf


#
# Clean section
#

%clean
[ %{buildroot} != "/" ] && rm -rf %{buildroot}
make clean

#
# Handle the init script
#

/sbin/chkconfig --add %{svc_name}
%if "%{VENDOR}" == "SuSE"
/etc/init.d/openvpn restart
%else
/sbin/service %{svc_name} restart
%endif
%preun
if [ "$1" = 0 ]
then
	%if "%{VENDOR}" == "SuSE"
	/etc/init.d/openvpn stop
	%else
	/sbin/service %{svc_name} stop
	%endif
	/sbin/chkconfig --del %{svc_name}
fi


#
# Files section
#

%files
%defattr (-,root,root)
%doc LICENSE INSTALL NEWS README.md
%{_mandir}/man8/%{name}.8*
/etc/init.d/%{name}
#/usr/local/php/

# Install extra %doc stuff
%doc README.*
