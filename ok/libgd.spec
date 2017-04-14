%define version    2.2.2

Name:       libgd
Version:    %{version}
Release:    1
Summary:    GUN libgd X86_64
License:    GPL
Source:     %{name}-%{version}.tar.gz
Group:      System Enviroment/Base
URL:        github.com/libgd/libgd/releases/download/gd-%{version}/libgd-%{version}.tar.gz
#Packager:   gk.wl@qq.com
#Vendor:     Taobao

%description
Libgd package

%if 0%{?fedora} < 17 && 0%{?rhel} < 6
%global  with_vpx  0
%else
%global  with_vpx  1
%endif

#yum install libwebp-devel libtiff-devel libXpm-devel libmcrypt-devel

BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: freetype-devel
BuildRequires: libXpm-devel
BuildRequires: libzlib-devel
BuildRequires: t1lib-devel

Requires: zlib
Requires: libXpm
Requires: libjpeg-turbo
Requires: libpng

%if %{with_vpx}
BuildRequires: libvpx-devel
%endif

%prep
%setup -q

./configure \
  --prefix=/usr \
  --bindir=/usr/bin \
  --includedir=/usr/include \
  --libdir=/usr/lib64 \
  --with-freetype \
  --with-png \
  --with-jpeg \
  --with-xpm=/usr/lib64

make %{?_smp_mflags}

# --target=x86_64-redhat-linux-gnu \
# --build=x86_64-redhat-linux-gnu \
# --host=x86_64-redhat-linux-gnu \

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
make clean

%post
ldconfig

%postun
ldconfig

exit 0

%files
%defattr (-,root,root)
/usr
#/usr/bin
#/usr/include
#/usr/lib64

%changelog
