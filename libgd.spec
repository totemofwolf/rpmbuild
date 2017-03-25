Name:       libgd
Version:    2.2.2
Release:    1
Vendor:     Taobao
Summary:    GUN libgd X86_64
License:    GPL
Source:     libgd-2.2.2.tar.gz
Group:      System Enviroment/Daemons
URL:        github.com/libgd/libgd/releases/download/gd-2.2.2/libgd-2.2.2.tar.gz
Packager:   gk.wl@qq.com
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
%if %{with_vpx}
BuildRequires: libvpx-devel
%endif


%prep
%setup -q
./configure --prefix=/usr/local/libgd --with-freetype --with-png --with-jpeg --with-xpm=/usr/lib64

make
%install
make DESTDIR=$RPM_BUILD_ROOT install
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
make clean
%files
%defattr (-,root,root)
/usr/local/libgd/

