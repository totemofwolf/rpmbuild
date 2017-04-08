%define version @VERSION@
%define so_version 5
%define release 0

Name: php
Summary: PHP: Hypertext Preprocessor
Group: Development/Languages
Version: %{version}
Release: %{release}
Copyright: The PHP license (see "LICENSE" file included in distribution)
Source: http://www.php.net/get/php-%{version}.tar.gz/from/a/mirror
Icon: php.gif
URL: http://www.php.net/
Packager: PHP Group <group@php.net>

BuildRoot: /var/tmp/php-%{version}

%description
PHP is an HTML-embedded scripting language. Much of its syntax is
borrowed from C, Java and Perl with a couple of unique PHP-specific
features thrown in. The goal of the language is to allow web
developers to write dynamically generated pages quickly.

%prep

%setup

%build
set -x
./buildconf
./configure --prefix=/usr --with-apxs \
	--disable-debug \
	--with-xml=shared \

# figure out configure options options based on what packages are installed
# to override, use the OVERRIDE_OPTIONS environment variable.  To add
# extra options, use the OPTIONS environment variable.

#test rpm -q MySQL-devel >&/dev/null && OPTIONS="$OPTIONS --with-mysql=shared"
#test rpm -q solid-devel >&/dev/null && OPTIONS="$OPTIONS --with-solid=shared,/home/solid"
#test rpm -q postgresql-devel >&/dev/null && OPTIONS="$OPTIONS --with-pgsql=shared"
test rpm -q expat >&/dev/null && OPTIONS="$OPTIONS --with-xml=shared"

if test "x$OVERRIDE_OPTIONS" = "x"; then
    ./configure --prefix=/usr --with-apxs=$APXS $OPTIONS
else
    ./configure $OVERRIDE_OPTIONS
fi

php_install_dir=/production/server/php

./configure \
--prefix=$php_install_dir \
--with-config-file-path=$php_install_dir/etc \
--with-config-file-scan-dir=$php_install_dir/etc/php.d \
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
--with-gd=/usr/local/libgd \
--with-gettext \
--with-iconv \
--with-libxml-dir=/usr \
--with-mcrypt \
--with-mhash \
--with-mysqli=mysqlnd \
--with-openssl \
--with-pdo-mysql=mysqlnd \
--with-xmlrpc \
--with-xpm-dir=/usr/lib64 \
--with-freetype-dir=/usr/lib64 \
--with-webp-dir=/usr/lib64 \
--with-jpeg-dir=/usr/lib64 \
--with-png-dir=/usr/lib64 \
--with-zlib \
--without-pear

make ZEND_EXTRA_LIBS='-liconv' -j4
