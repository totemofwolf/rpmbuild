# php55 spec file, used to drive rpmbuild

%define version 5.5.38
%define release 1

%define php_install_dir /production/server/php

Name: php
Version: %{version}
Release: %{release}
Summary: PHP Hypertext Preprocessor
URL: http://cn2.php.net/distributions/%{name}-%{version}.tar.gz
Source: %{name}-%{version}.tar.gz
#BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

License:    GPL
Group: Development/Languages
#Vendor:     php.net

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
  --enable-opcache \
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
  --with-jpeg-dir \
  --with-freetype-dir \
  --with-xpm-dir \
  --with-png-dir \
  --with-gettext \
  --with-iconv \
  --with-libxml-dir=/usr \
  --with-mcrypt \
  --with-mhash \
  --with-mysql=mysqlnd \
  --with-mysqli=mysqlnd \
  --with-openssl \
  --with-pdo-mysql=mysqlnd \
  --with-xmlrpc \
  --with-zlib \
  --without-pear

make ZEND_EXTRA_LIBS='-liconv' %{_smp_mflags}

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
%{php_install_dir}
/etc/init.d/php-fpm

# -----
#%{_bindir}/*
#%{_sbindir}/*
#%{_includedir}/*
#%{_libdir}/*
#%{_datadir}/*
#%{_initrddir}/*
#%post
#%/sbin/chkconfig --add php-fpm
#%/sbin/chkconfig --level 2345 php-fpm on
#%preun
#if [ "$1" = 0 ] ; then
#    /sbin/service php-fpm stop > /dev/null 2>&1
#    /sbin/chkconfig --del php-fpm
#fi
#exit 0
#%postun
#if [ "$1" -ge 1 ]; then
#    /sbin/service php-fpm condrestart > /dev/null 2>&1
#fi
#exit 0
#install -Dp -m0755 sapi/fpm/init.d.php-fpm.in %{buildroot}%{_initrddir}/php-fpm
#install -Dp -m0644 ./php.ini-production ${RPM_BUILD_ROOT}/usr/local/etc
#rpm -ivh libiconv-1.13.1-1.x86_64.rpm
#%{!?without-iconv:BuildRequires: libiconv >= 1.13.1}
#%{!?without-iconv:Requires:}
