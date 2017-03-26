# php55 spec file, used to drive rpmbuild

%define version 5.5.38
%define so_version 5
%define release 0
%define svc_name php-fpm

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
./configure --prefix=/usr/local/php --disable-debug --disable-fileinfo --disable-ipv6 --disable-maintainer-zts --enable-bcmath --enable-calendar --enable-fpm --enable-ftp --enable-gd-jis-conv --enable-gd-native-ttf --enable-inline-optimization --enable-mbregex --enable-mbstring --enable-opcache --enable-pcntl --enable-shmop --enable-soap --enable-sockets --enable-static --enable-sysvsem --enable-wddx --enable-xml --enable-zip --with-config-file-path=/usr/local/php/etc --with-curl --with-gd=/usr/local/libgd --with-gettext --with-iconv --with-libxml-dir=/usr --with-mcrypt --with-mhash --with-mysql=mysqlnd --with-mysqli=mysqlnd --with-openssl --with-pdo-mysql=mysqlnd --with-xmlrpc --with-zlib --without-pear

make ZEND_EXTRA_LIBS='-liconv' -j4

#
# Installation section
#

%install
rm -rf $RPM_BUILD_ROOT
make install DISTDIR=$RPM_BUILD_ROOT

rhel_cp() {
 base=$1
 mode=$2
 dst=$RPM_BUILD_ROOT/$(echo $base | sed 's,_,/,g')
 install -D -m $mode rhel/$base $dst
}

docdir=$RPM_BUILD_ROOT/usr/share/doc/php-%{version}
install -d -m 755 "$docdir"

# Install init script
%__install -c -d -m 755 %{buildroot}/etc/init.d
%__install -c -m 755 sapi/fpm/init.d.%{svc_name} %{buildroot}/etc/init.d/%{svc_name}
# Install man page
#install -m 0644 xxx "$docdir"
#install xxx $RPM_BUILD_ROOT/usr/share/php/
#%__install -c -d -m 755 %{buildroot}%{_mandir}/man8
#%__install -c -m 755 sapi/fpm/%{svc_name}.8 %{buildroot}%{_mandir}/man8
#php.ini-production
#./sapi/fpm/php-fpm.conf

#
# Clean section
#

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Ensure all required services are set to run
/sbin/chkconfig -add php-fpm
/sbin/chkconfig php-fpm on

%preun
if [ "$1" = "0" ]; then
    /sbin/service php-fpm stop
    /sbin/chkconfig --del php-fpm
fi


%postun
if [ "$1" = "0" ]; then

fi

exit 0

#
# Files section
#

%files
$defattr{-,root,root}
%doc LICENSE INSTALL NEWS README.md
%{_mandir}/man8/%{svc_name}.8*
/etc/init.d/php-fpm
#/etc/init.d/%{svc_name}
%config(noreplace) /usr/local/php/include/php/include
/usr/local/php/include/php/TSRM
/usr/local/php/include/php/TSRM/tsrm_config.w32.h
/usr/local/php/include/php/TSRM/tsrm_config_common.h
/usr/local/php/include/php/TSRM/tsrm_virtual_cwd.h
/usr/local/php/include/php/TSRM/tsrm_nw.h
/usr/local/php/include/php/TSRM/tsrm_win32.h
/usr/local/php/include/php/TSRM/readdir.h
/usr/local/php/include/php/TSRM/tsrm_config.h
/usr/local/php/include/php/TSRM/TSRM.h
/usr/local/php/include/php/TSRM/tsrm_strtok_r.h
/usr/local/php/include/php/main
/usr/local/php/include/php/main/SAPI.h
/usr/local/php/include/php/main/php_content_types.h
/usr/local/php/include/php/main/php_streams.h
/usr/local/php/include/php/main/php_main.h
/usr/local/php/include/php/main/php_memory_streams.h
/usr/local/php/include/php/main/php_globals.h
/usr/local/php/include/php/main/php_open_temporary_file.h
/usr/local/php/include/php/main/php.h
/usr/local/php/include/php/main/php_ini.h
/usr/local/php/include/php/main/php_version.h
/usr/local/php/include/php/main/php_reentrancy.h
/usr/local/php/include/php/main/php_network.h
/usr/local/php/include/php/main/php_getopt.h
/usr/local/php/include/php/main/php_compat.h
/usr/local/php/include/php/main/win32_internal_function_disabled.h
/usr/local/php/include/php/main/php_ticks.h
/usr/local/php/include/php/main/php_syslog.h
/usr/local/php/include/php/main/php_scandir.h
/usr/local/php/include/php/main/streams
/usr/local/php/include/php/main/streams/php_stream_transport.h
/usr/local/php/include/php/main/streams/php_stream_plain_wrapper.h
/usr/local/php/include/php/main/streams/php_stream_glob_wrapper.h
/usr/local/php/include/php/main/streams/php_stream_context.h
/usr/local/php/include/php/main/streams/php_stream_userspace.h
/usr/local/php/include/php/main/streams/php_streams_int.h
/usr/local/php/include/php/main/streams/php_stream_filter_api.h
/usr/local/php/include/php/main/streams/php_stream_mmap.h
/usr/local/php/include/php/main/php_output.h
/usr/local/php/include/php/main/php_variables.h
/usr/local/php/include/php/main/snprintf.h
/usr/local/php/include/php/main/build-defs.h
/usr/local/php/include/php/main/fopen_wrappers.h
/usr/local/php/include/php/main/spprintf.h
/usr/local/php/include/php/main/php_config.h
/usr/local/php/include/php/main/win95nt.h
/usr/local/php/include/php/main/rfc1867.h
/usr/local/php/include/php/sapi
/usr/local/php/include/php/sapi/cli
/usr/local/php/include/php/sapi/cli/cli.h
/usr/local/php/include/php/Zend
/usr/local/php/include/php/Zend/zend_indent.h
/usr/local/php/include/php/Zend/zend_objects_API.h
/usr/local/php/include/php/Zend/zend_constants.h
/usr/local/php/include/php/Zend/zend_language_scanner.h
/usr/local/php/include/php/Zend/zend_multiply.h
/usr/local/php/include/php/Zend/zend_build.h
/usr/local/php/include/php/Zend/zend_types.h
/usr/local/php/include/php/Zend/zend_variables.h
/usr/local/php/include/php/Zend/zend_multibyte.h
/usr/local/php/include/php/Zend/zend_vm_opcodes.h
/usr/local/php/include/php/Zend/zend_vm_def.h
/usr/local/php/include/php/Zend/zend_config.h
/usr/local/php/include/php/Zend/zend_closures.h
/usr/local/php/include/php/Zend/zend_ptr_stack.h
/usr/local/php/include/php/Zend/zend_language_scanner_defs.h
/usr/local/php/include/php/Zend/zend_config.nw.h
/usr/local/php/include/php/Zend/zend_stack.h
/usr/local/php/include/php/Zend/zend_API.h
/usr/local/php/include/php/Zend/zend_operators.h
/usr/local/php/include/php/Zend/zend_hash.h
/usr/local/php/include/php/Zend/zend_static_allocator.h
/usr/local/php/include/php/Zend/zend_extensions.h
/usr/local/php/include/php/Zend/zend_highlight.h
/usr/local/php/include/php/Zend/zend_vm.h
/usr/local/php/include/php/Zend/zend_globals_macros.h
/usr/local/php/include/php/Zend/zend_signal.h
/usr/local/php/include/php/Zend/zend_modules.h
/usr/local/php/include/php/Zend/zend_errors.h
/usr/local/php/include/php/Zend/zend_ini_parser.h
/usr/local/php/include/php/Zend/zend.h
/usr/local/php/include/php/Zend/zend_ts_hash.h
/usr/local/php/include/php/Zend/zend_ini.h
/usr/local/php/include/php/Zend/zend_language_parser.h
/usr/local/php/include/php/Zend/zend_globals.h
/usr/local/php/include/php/Zend/zend_compile.h
/usr/local/php/include/php/Zend/zend_strtod.h
/usr/local/php/include/php/Zend/zend_builtin_functions.h
/usr/local/php/include/php/Zend/zend_alloc.h
/usr/local/php/include/php/Zend/zend_qsort.h
/usr/local/php/include/php/Zend/zend_objects.h
/usr/local/php/include/php/Zend/zend_stream.h
/usr/local/php/include/php/Zend/zend_dtrace.h
/usr/local/php/include/php/Zend/zend_string.h
/usr/local/php/include/php/Zend/zend_execute.h
/usr/local/php/include/php/Zend/zend_iterators.h
/usr/local/php/include/php/Zend/zend_list.h
/usr/local/php/include/php/Zend/zend_config.w32.h
/usr/local/php/include/php/Zend/zend_float.h
/usr/local/php/include/php/Zend/zend_ini_scanner.h
/usr/local/php/include/php/Zend/zend_llist.h
/usr/local/php/include/php/Zend/zend_object_handlers.h
/usr/local/php/include/php/Zend/zend_generators.h
/usr/local/php/include/php/Zend/zend_istdiostream.h
/usr/local/php/include/php/Zend/zend_interfaces.h
/usr/local/php/include/php/Zend/zend_gc.h
/usr/local/php/include/php/Zend/zend_vm_execute.h
/usr/local/php/include/php/Zend/zend_exceptions.h
/usr/local/php/include/php/Zend/zend_dynamic_array.h
/usr/local/php/include/php/Zend/zend_ini_scanner_defs.h
/usr/local/php/include/php/ext
/usr/local/php/include/php/ext/filter
/usr/local/php/include/php/ext/filter/php_filter.h
/usr/local/php/include/php/ext/iconv
/usr/local/php/include/php/ext/iconv/php_iconv.h
/usr/local/php/include/php/ext/iconv/php_have_libiconv.h
/usr/local/php/include/php/ext/iconv/php_have_glibc_iconv.h
/usr/local/php/include/php/ext/iconv/php_iconv_broken_ignore.h
/usr/local/php/include/php/ext/iconv/php_iconv_aliased_libiconv.h
/usr/local/php/include/php/ext/iconv/php_have_iconv.h
/usr/local/php/include/php/ext/iconv/php_have_bsd_iconv.h
/usr/local/php/include/php/ext/iconv/php_php_iconv_h_path.h
/usr/local/php/include/php/ext/iconv/php_php_iconv_impl.h
/usr/local/php/include/php/ext/iconv/php_iconv_supports_errno.h
/usr/local/php/include/php/ext/iconv/php_have_ibm_iconv.h
/usr/local/php/include/php/ext/mysqlnd
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_block_alloc.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_result_meta.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_portability.h
/usr/local/php/include/php/ext/mysqlnd/config-win.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_net.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_result.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_libmysql_compat.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_reverse_api.h
/usr/local/php/include/php/ext/mysqlnd/php_mysqlnd.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_structs.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_priv.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_enum_n_def.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_alloc.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_wireprotocol.h
/usr/local/php/include/php/ext/mysqlnd/mysql_float_to_double.h
/usr/local/php/include/php/ext/mysqlnd/php_mysqlnd_config.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_charset.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_statistics.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_ext_plugin.h
/usr/local/php/include/php/ext/mysqlnd/mysqlnd_debug.h
/usr/local/php/include/php/ext/sqlite3
/usr/local/php/include/php/ext/sqlite3/libsqlite
/usr/local/php/include/php/ext/sqlite3/libsqlite/sqlite3.h
/usr/local/php/include/php/ext/date
/usr/local/php/include/php/ext/date/php_date.h
/usr/local/php/include/php/ext/date/lib
/usr/local/php/include/php/ext/date/lib/timelib.h
/usr/local/php/include/php/ext/date/lib/timelib_config.h
/usr/local/php/include/php/ext/date/lib/timelib_structs.h
/usr/local/php/include/php/ext/mbstring
/usr/local/php/include/php/ext/mbstring/mbstring.h
/usr/local/php/include/php/ext/mbstring/php_mbregex.h
/usr/local/php/include/php/ext/mbstring/php_onig_compat.h
/usr/local/php/include/php/ext/mbstring/libmbfl
/usr/local/php/include/php/ext/mbstring/libmbfl/config.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/mbfl_encoding.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/mbfl_consts.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/eaw_table.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/mbfl_language.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/mbfl_convert.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/mbfl_string.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/mbfilter_pass.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/mbfl_filter_output.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/mbfl_allocators.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/mbfl_memory_device.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/mbfl_ident.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/mbfilter_wchar.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/mbfilter.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/mbfilter_8bit.h
/usr/local/php/include/php/ext/mbstring/libmbfl/mbfl/mbfl_defs.h
/usr/local/php/include/php/ext/mbstring/oniguruma
/usr/local/php/include/php/ext/mbstring/oniguruma/oniguruma.h
/usr/local/php/include/php/ext/phar
/usr/local/php/include/php/ext/phar/php_phar.h
/usr/local/php/include/php/ext/hash
/usr/local/php/include/php/ext/hash/php_hash_crc32.h
/usr/local/php/include/php/ext/hash/php_hash_ripemd.h
/usr/local/php/include/php/ext/hash/php_hash_whirlpool.h
/usr/local/php/include/php/ext/hash/php_hash_joaat.h
/usr/local/php/include/php/ext/hash/php_hash_types.h
/usr/local/php/include/php/ext/hash/php_hash_sha.h
/usr/local/php/include/php/ext/hash/php_hash_gost.h
/usr/local/php/include/php/ext/hash/php_hash_md.h
/usr/local/php/include/php/ext/hash/php_hash_adler32.h
/usr/local/php/include/php/ext/hash/php_hash_haval.h
/usr/local/php/include/php/ext/hash/php_hash_tiger.h
/usr/local/php/include/php/ext/hash/php_hash_fnv.h
/usr/local/php/include/php/ext/hash/php_hash_snefru.h
/usr/local/php/include/php/ext/hash/php_hash.h
/usr/local/php/include/php/ext/pdo
/usr/local/php/include/php/ext/pdo/php_pdo.h
/usr/local/php/include/php/ext/pdo/php_pdo_driver.h
/usr/local/php/include/php/ext/json
/usr/local/php/include/php/ext/json/php_json.h
/usr/local/php/include/php/ext/standard
/usr/local/php/include/php/ext/standard/php_crypt_r.h
/usr/local/php/include/php/ext/standard/html.h
/usr/local/php/include/php/ext/standard/cyr_convert.h
/usr/local/php/include/php/ext/standard/php_type.h
/usr/local/php/include/php/ext/standard/php_metaphone.h
/usr/local/php/include/php/ext/standard/php_browscap.h
/usr/local/php/include/php/ext/standard/php_dir.h
/usr/local/php/include/php/ext/standard/php_array.h
/usr/local/php/include/php/ext/standard/php_smart_str.h
/usr/local/php/include/php/ext/standard/dl.h
/usr/local/php/include/php/ext/standard/exec.h
/usr/local/php/include/php/ext/standard/html_tables.h
/usr/local/php/include/php/ext/standard/pack.h
/usr/local/php/include/php/ext/standard/basic_functions.h
/usr/local/php/include/php/ext/standard/url_scanner_ex.h
/usr/local/php/include/php/ext/standard/php_http.h
/usr/local/php/include/php/ext/standard/php_link.h
/usr/local/php/include/php/ext/standard/php_rand.h
/usr/local/php/include/php/ext/standard/info.h
/usr/local/php/include/php/ext/standard/credits_sapi.h
/usr/local/php/include/php/ext/standard/credits_ext.h
/usr/local/php/include/php/ext/standard/scanf.h
/usr/local/php/include/php/ext/standard/sha1.h
/usr/local/php/include/php/ext/standard/php_smart_str_public.h
/usr/local/php/include/php/ext/standard/php_ext_syslog.h
/usr/local/php/include/php/ext/standard/file.h
/usr/local/php/include/php/ext/standard/php_mail.h
/usr/local/php/include/php/ext/standard/css.h
/usr/local/php/include/php/ext/standard/quot_print.h
/usr/local/php/include/php/ext/standard/php_versioning.h
/usr/local/php/include/php/ext/standard/php_string.h
/usr/local/php/include/php/ext/standard/fsock.h
/usr/local/php/include/php/ext/standard/md5.h
/usr/local/php/include/php/ext/standard/php_assert.h
/usr/local/php/include/php/ext/standard/datetime.h
/usr/local/php/include/php/ext/standard/base64.h
/usr/local/php/include/php/ext/standard/php_math.h
/usr/local/php/include/php/ext/standard/crypt_blowfish.h
/usr/local/php/include/php/ext/standard/head.h
/usr/local/php/include/php/ext/standard/crc32.h
/usr/local/php/include/php/ext/standard/php_lcg.h
/usr/local/php/include/php/ext/standard/php_var.h
/usr/local/php/include/php/ext/standard/proc_open.h
/usr/local/php/include/php/ext/standard/credits.h
/usr/local/php/include/php/ext/standard/php_filestat.h
/usr/local/php/include/php/ext/standard/php_password.h
/usr/local/php/include/php/ext/standard/php_crypt.h
/usr/local/php/include/php/ext/standard/php_incomplete_class.h
/usr/local/php/include/php/ext/standard/php_standard.h
/usr/local/php/include/php/ext/standard/php_fopen_wrappers.h
/usr/local/php/include/php/ext/standard/streamsfuncs.h
/usr/local/php/include/php/ext/standard/php_iptc.h
/usr/local/php/include/php/ext/standard/php_image.h
/usr/local/php/include/php/ext/standard/pageinfo.h
/usr/local/php/include/php/ext/standard/php_uuencode.h
/usr/local/php/include/php/ext/standard/microtime.h
/usr/local/php/include/php/ext/standard/winver.h
/usr/local/php/include/php/ext/standard/php_dns.h
/usr/local/php/include/php/ext/standard/uniqid.h
/usr/local/php/include/php/ext/standard/crypt_freesec.h
/usr/local/php/include/php/ext/standard/url.h
/usr/local/php/include/php/ext/standard/flock_compat.h
/usr/local/php/include/php/ext/standard/php_ftok.h
/usr/local/php/include/php/ext/pcre
/usr/local/php/include/php/ext/pcre/php_pcre.h
/usr/local/php/include/php/ext/pcre/pcrelib
/usr/local/php/include/php/ext/pcre/pcrelib/config.h
/usr/local/php/include/php/ext/pcre/pcrelib/pcreposix.h
/usr/local/php/include/php/ext/pcre/pcrelib/ucp.h
/usr/local/php/include/php/ext/pcre/pcrelib/pcre.h
/usr/local/php/include/php/ext/pcre/pcrelib/pcre_internal.h
/usr/local/php/include/php/ext/gd
/usr/local/php/include/php/ext/gd/php_gd.h
/usr/local/php/include/php/ext/gd/gdcache.h
/usr/local/php/include/php/ext/gd/gd_compat.h
/usr/local/php/include/php/ext/dom
/usr/local/php/include/php/ext/dom/xml_common.h
/usr/local/php/include/php/ext/session
/usr/local/php/include/php/ext/session/php_session.h
/usr/local/php/include/php/ext/session/mod_files.h
/usr/local/php/include/php/ext/session/mod_user.h
/usr/local/php/include/php/ext/mysqli
/usr/local/php/include/php/ext/mysqli/php_mysqli_structs.h
/usr/local/php/include/php/ext/mysqli/mysqli_mysqlnd.h
/usr/local/php/include/php/ext/ereg
/usr/local/php/include/php/ext/ereg/regex
/usr/local/php/include/php/ext/ereg/regex/regex2.h
/usr/local/php/include/php/ext/ereg/regex/utils.h
/usr/local/php/include/php/ext/ereg/regex/cname.h
/usr/local/php/include/php/ext/ereg/regex/regex.h
/usr/local/php/include/php/ext/ereg/regex/cclass.h
/usr/local/php/include/php/ext/ereg/php_regex.h
/usr/local/php/include/php/ext/ereg/php_ereg.h
/usr/local/php/include/php/ext/xml
/usr/local/php/include/php/ext/xml/php_xml.h
/usr/local/php/include/php/ext/xml/expat_compat.h
/usr/local/php/include/php/ext/sockets
/usr/local/php/include/php/ext/sockets/php_sockets.h
/usr/local/php/include/php/ext/spl
/usr/local/php/include/php/ext/spl/spl_heap.h
/usr/local/php/include/php/ext/spl/spl_fixedarray.h
/usr/local/php/include/php/ext/spl/spl_dllist.h
/usr/local/php/include/php/ext/spl/spl_observer.h
/usr/local/php/include/php/ext/spl/spl_iterators.h
/usr/local/php/include/php/ext/spl/spl_engine.h
/usr/local/php/include/php/ext/spl/spl_array.h
/usr/local/php/include/php/ext/spl/spl_directory.h
/usr/local/php/include/php/ext/spl/spl_exceptions.h
/usr/local/php/include/php/ext/spl/spl_functions.h
/usr/local/php/include/php/ext/spl/php_spl.h
/usr/local/php/include/php/ext/libxml
/usr/local/php/include/php/ext/libxml/php_libxml.h
/usr/local/php/php/man
/usr/local/php/php/man/man8
/usr/local/php/php/man/man8/php-fpm.8
/usr/local/php/php/man/man1
/usr/local/php/php/man/man1/phar.phar.1
/usr/local/php/php/man/man1/php-config.1
/usr/local/php/php/man/man1/phar.1
/usr/local/php/php/man/man1/php-cgi.1
/usr/local/php/php/man/man1/phpize.1
/usr/local/php/php/man/man1/php.1
/usr/local/php/lib
/usr/local/php/lib/php
/usr/local/php/lib/php/extensions
/usr/local/php/lib/php/extensions/no-debug-non-zts-20121212
/usr/local/php/lib/php/extensions/no-debug-non-zts-20121212/opcache.so
/usr/local/php/lib/php/extensions/no-debug-non-zts-20121212/opcache.a
/usr/local/php/lib/php/build
/usr/local/php/lib/php/build/acinclude.m4
/usr/local/php/lib/php/build/ltmain.sh
/usr/local/php/lib/php/build/scan_makefile_in.awk
/usr/local/php/lib/php/build/libtool.m4
/usr/local/php/lib/php/build/run-tests.php
/usr/local/php/lib/php/build/config.guess
/usr/local/php/lib/php/build/shtool
/usr/local/php/lib/php/build/config.sub
/usr/local/php/lib/php/build/phpize.m4
/usr/local/php/lib/php/build/Makefile.global
/usr/local/php/lib/php/build/mkdep.awk
/usr/local/php/etc
/usr/local/php/etc/php-fpm.conf.default
/usr/local/php/sbin
/usr/local/php/sbin/php-fpm
/usr/local/php/bin
/usr/local/php/bin/php-cgi
/usr/local/php/bin/php
/usr/local/php/bin/phar.phar
/usr/local/php/bin/phar
/usr/local/php/bin/php-config
/usr/local/php/bin/phpize
/usr/local/php/var
/usr/local/php/var/run
/usr/local/php/var/log
# Install extra %doc stuff
%doc README.*
