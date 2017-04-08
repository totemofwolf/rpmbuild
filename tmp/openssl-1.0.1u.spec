%define _unpackaged_files_terminate_build 0
#%define debug_package %{nil}
%define _exec_prefix /usr/local/ssl
#%define _bindir /usr/local/ssl
%define _libdir /usr/local/ssl/lib
%define _includedir /usr/local/ssl/include
Release: 1

#%define openssldir /etc/pki/tls
#%define openssldir /var/ssl
#OPENSSLDIR: "/etc/pki/tls"
# engines:  rdrand dynamic
# options:  bn(64,64) md2(int) rc4(16x,int) des(idx,cisc,16,int) idea(int) blowfish(idx)
# compiler: gcc -fPIC -DOPENSSL_PIC -DZLIB -DOPENSSL_THREADS -D_REENTRANT -DDSO_DLFCN -DHAVE_DLFCN_H -DKRB5_MIT
# -m64 -DL_ENDIAN -DTERMIO -Wall -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2
# -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -Wa,--noexecstack -DPURIFY -DOPENSSL_IA32_SSE2 -DOPENSSL_BN_ASM_MONT -DOPENSSL_BN_ASM_MONT5
# -DOPENSSL_BN_ASM_GF2m -DSHA1_ASM -DSHA256_ASM -DSHA512_ASM -DMD5_ASM -DAES_ASM -DVPAES_ASM -DBSAES_ASM -DWHIRLPOOL_ASM -DGHASH_ASM

Summary: Secure Sockets Layer and cryptography libraries and tools
Name: openssl
Version: 1.0.1u
Source0: ftp://ftp.openssl.org/source/%{name}-%{version}.tar.gz
License: OpenSSL
Group: System Environment/Libraries
Provides: SSL
URL: http://www.openssl.org/
# Packager: Damien Miller <djm@mindrot.org>
BuildRoot:   /var/tmp/%{name}-%{version}-root

%description
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, fully featured, and Open Source toolkit implementing the
Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS v1)
protocols as well as a full-strength general purpose cryptography library.
The project is managed by a worldwide community of volunteers that use the
Internet to communicate, plan, and develop the OpenSSL tookit and its related
documentation.

OpenSSL is based on the excellent SSLeay library developed from Eric A.
Young and Tim J. Hudson.  The OpenSSL toolkit is licensed under an
Apache-style licence, which basically means that you are free to get and
use it for commercial and non-commercial purposes.

This package contains the base OpenSSL cryptography and SSL/TLS
libraries and tools.

%package devel
Summary: Secure Sockets Layer and cryptography static libraries and headers
Group: Development/Libraries
Requires: openssl
%description devel
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, fully featured, and Open Source toolkit implementing the
Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS v1)
protocols as well as a full-strength general purpose cryptography library.
The project is managed by a worldwide community of volunteers that use the
Internet to communicate, plan, and develop the OpenSSL tookit and its related
documentation.

OpenSSL is based on the excellent SSLeay library developed from Eric A.
Young and Tim J. Hudson.  The OpenSSL toolkit is licensed under an
Apache-style licence, which basically means that you are free to get and
use it for commercial and non-commercial purposes.

This package contains the the OpenSSL cryptography and SSL/TLS
static libraries and header files required when developing applications.

%package doc
Summary: OpenSSL miscellaneous files
Group: Documentation
Requires: openssl
%description doc
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, fully featured, and Open Source toolkit implementing the
Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS v1)
protocols as well as a full-strength general purpose cryptography library.
The project is managed by a worldwide community of volunteers that use the
Internet to communicate, plan, and develop the OpenSSL tookit and its related
documentation.

OpenSSL is based on the excellent SSLeay library developed from Eric A.
Young and Tim J. Hudson.  The OpenSSL toolkit is licensed under an
Apache-style licence, which basically means that you are free to get and
use it for commercial and non-commercial purposes.

This package contains the the OpenSSL cryptography and SSL/TLS extra
documentation and POD files from which the man pages were produced.

%prep

%setup -q

%build

#%define CONFIG_FLAGS -DSSL_ALLOW_ADH --prefix=%{_exec_prefix} --openssldir=%{openssldir} zlib
%define CONFIG_FLAGS -DSSL_ALLOW_ADH --prefix=%{_exec_prefix} zlib

perl util/perlpath.pl /usr/bin/perl

%ifarch i386 i486 i586 i686
./Configure %{CONFIG_FLAGS} linux-elf shared
%endif
%ifarch ppc
./Configure %{CONFIG_FLAGS} linux-ppc shared
%endif
%ifarch alpha
./Configure %{CONFIG_FLAGS} linux-alpha shared
%endif
%ifarch x86_64
./Configure %{CONFIG_FLAGS} linux-x86_64 shared
%endif
LD_LIBRARY_PATH=`pwd` make
LD_LIBRARY_PATH=`pwd` make rehash
LD_LIBRARY_PATH=`pwd` make test

%install
rm -rf $RPM_BUILD_ROOT
make MANDIR=%{_mandir} MANSUFFIX=ssl INSTALL_PREFIX="$RPM_BUILD_ROOT" install

# Make backwards-compatibility symlink to ssleay
# ln -sf /usr/bin/openssl $RPM_BUILD_ROOT/usr/bin/ssleay
#

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc CHANGES CHANGES.SSLeay LICENSE NEWS README

%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_libdir}/*.so*
%attr(0755,root,root) %{_libdir}/engines/*.so*
%attr(0755,root,root) %{_libdir}/pkgconfig/*
#%attr(0755,root,root) %{openssldir}/misc/*
%attr(0644,root,root) %{_mandir}/man[157]/*
#%attr(0644,root,root) %{_docdir}/man[157]/*

%files devel
%defattr(0644,root,root,0755)
%doc CHANGES CHANGES.SSLeay LICENSE NEWS README

%attr(0644,root,root) %{_libdir}/*.a
%attr(0644,root,root) %{_libdir}/pkgconfig/openssl.pc
%attr(0644,root,root) %{_includedir}/openssl/*
%attr(0644,root,root) %{_mandir}/man[3]/*

%files doc
%defattr(0644,root,root,0755)
%doc CHANGES CHANGES.SSLeay LICENSE NEWS README
%doc doc

%post
ldconfig

%postun
ldconfig

%changelog
