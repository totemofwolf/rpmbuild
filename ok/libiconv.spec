%define version 1.13.1

Name:       libiconv
Version:    %{version}
Release:    1
Summary:    GUN libiconv X86_64
License:    GPL
Source:     %{name}-%{version}.tar.gz
Group:      System Enviroment/Base
URL:        http://oss.aliyuncs.com/aliyunecs/onekey/libiconv-%{version}.tar.gz

#
# Description
#

%description
Libiconv package

#
# Include dependencies manually
#

#
# Build libiconv binary
#

%prep
%setup -q
./configure --prefix=/usr/local
make %{?_smp_mflags}

#
# Installation section
#

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#
# Clean section
#

%clean
[ %{buildroot} != "/" ] && rm -rf %{buildroot}
make clean

%post
ldconfig

%postun
ldconfig

%files
%defattr(-,root,root)
/usr/local

%changelog
