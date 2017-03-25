Name:       libiconv
Version:    1.13.1
Release:    1
Vendor:     Huanqiu
Summary:    GUN iconv X86_64
License:    GPL
Source:     libiconv-1.13.1.tar.gz
Group:      System Enviroment/Daemons
URL:        http://oss.aliyuncs.com/aliyunecs/onekey/libiconv-1.13.1.tar.gz
Packager:   gk.wl@qq.com
%description
Huanqiu iconv package
%prep
%setup -q
./configure --prefix=/usr/local

make
%install
make DESTDIR=$RPM_BUILD_ROOT install
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
make clean
%files
%defattr (-,root,root)
/usr/local/
