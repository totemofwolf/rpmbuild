Name:       libiconv
Version:    1.13.1
Release:    1
Summary:    character set conversion
License:    GPL
Source:     %{name}-%{version}.tar.gz
Group:      System Enviroment/Base
URL:        http://oss.aliyuncs.com/aliyunecs/onekey/%{name}-%{version}.tar.gz

#BuildRequires:
#Requires:

%description
The iconv program converts text from one encoding to another encoding
More precisely, it converts from the encoding given for the -f option
to the encoding given for the -t option. Either of these encodings defaults
to the encoding of the current locale. All the inputfiles are read and converted
in turn; if no inputfile is given the standard input is used. The converted text
is printed to standard output.

The encodings permitted are system dependent. For the libiconv implementation
they are listed in the iconv_open(3) manual page.

%prep
%setup -q
./configure \
  --prefix=/usr/local

make

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
make clean

%files
%defattr (-,root,root)
#%doc
/usr/local/

%changelog
