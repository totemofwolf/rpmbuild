Name:       libgd
Version:    2.2.2
Release:    1
Summary:    GUN libgd X86_64
License:    GPL
Source:     %{name}-%{version}.tar.gz
Group:      System Enviroment/Base
URL:        github.com/libgd/libgd/releases/download/gd-2.2.2/libgd-2.2.2.tar.gz
#Packager:   gk.wl@qq.com
#Vendor:     Taobao

%description
Libgd package

%if 0%{?fedora} < 17 && 0%{?rhel} < 6
%global  with_vpx  0
%else
%global  with_vpx  1
%endif

BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: freetype-devel
BuildRequires: libXpm-devel
BuildRequires: libzlib-devel
BuildRequires: t1lib-devel
BuildRequires: zlib
%if %{with_vpx}
BuildRequires: libvpx-devel
%endif

%prep
%setup -q
./configure --prefix=/usr/local/libgd --with-freetype --with-png --with-jpeg --with-xpm=/usr/lib64
make %{_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
make clean

%files
%defattr (-,root,root)
#%doc
/usr/local/libgd/

%changelog
