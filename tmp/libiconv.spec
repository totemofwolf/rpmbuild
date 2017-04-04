%define version 1.15

Summary:    GUN libiconv X86_64
Name:       libiconv
Version:    %{version}
Release:    1
URL:        http://oss.aliyuncs.com/aliyunecs/onekey/libiconv-%{version}.tar.gz
Source:     %{name}-%{version}.tar.gz

License:    GPL
Group:      System Enviroment/Base
#Packager:
#Vendor:
BuildRoot:      %{_tmppath}/%{name}-%(id -un)

#
# Include dependencies manually
#

#
# Description
#

%description
Libiconv package

#
# Build libiconv binary
#

%prep
%setup -q

%build
./configure --prefix=/usr/local
%__make
%__strip %{name}

#make

#
# Installation section
#

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}
libtool --finish /usr/local/lib
make DESTDIR=${buildroot} install

#
# Clean section
#

%clean
[ %{buildroot} != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/local/

%changelog
