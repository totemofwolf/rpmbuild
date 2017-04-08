%define _user www
%define _group www
%define _prefix /usr/local/php

Name: php  #软件包名称
Version: 5.5.38  #版本号（不能使用-）
Release: 1%{?dist}   #release号，对应下面的changelog，如php-5.4.45-1.el6.x86_64.rpm

Summary: PHP is a server-side scripting language for creating dynamic Web pages  #简要描述信息，最好不要超过50个字符，如要详述，使用下面的%description
Group: Development/Languages   #要全用这里面的一个组：less /usr/share/doc/rpm-version/GROUPS
License: GPLv2  #软件授权方式
URL: http://www.php.net  #源码相关网站
Packager: yeho <lj2007331@gmail.com>  #打包人的信息
Vendor: OneinStack  #发行商或打包组织的信息

Source0: %{name}-%{version}.tar.gz  #源代码包，可以带多个用Source1、Source2等源，后面也可以用%{source1}、%{source2}引用
BuildRoot: %_topdir/BUILDROOT  #安装或编译时使用的“虚拟目录”

Requires: libcurl
Requires: libmcrypt
Requires: mhash
Requires: mcrypt
Requires: libiconv #定义php依赖的包，需要yum安装(此处使用epel源)

%description  #软件包详述
PHP is a widely-used general-purpose scripting language that is especially suited for Web development and can be embedded into HTML.

%prep  #软件编译之前的处理，如解压
%setup -q  #这个宏的作用静默模式解压并cd
%build  #开始编译软件
%configure \
  --prefix=%{_prefix} \
  --with-config-file-path=%{_prefix}/etc \
  --disable-debug \
  --disable-ipv6 \
  --disable-rpath \
  --enable-bcmath \
  --enable-calendar \
  --enable-exif \
  --enable-fileinfo \
  --enable-fpm \
  --enable-ftp \
  --enable-gd-native-ttf \
  --enable-inline-optimization \
  --enable-mbregex \
  --enable-mbstring \
  --enable-pcntl \
  --enable-shmop \
  --enable-soap \
  --enable-sockets \
  --enable-sysvsem \
  --enable-xml \
  --enable-zip \
  --with-curl \
  --with-fpm-group=%{_group} \
  --with-fpm-user=%{_user} \
  --with-freetype-dir \
  --with-gd \
  --with-gettext \
  --with-iconv-dir=/usr/local \
  --with-jpeg-dir \
  --with-libxml-dir=/usr \
  --with-mcrypt \
  --with-mhash \
  --with-mysql=mysqlnd \
  --with-mysqli=mysqlnd \
  --with-openssl \
  --with-pdo-mysql=mysqlnd \
  --with-png-dir \
  --with-xmlrpc \
  --with-zlib

make ZEND_EXTRA_LIBS='-liconv' %{?_smp_mflags}  #%{?_smp_mflags} 的意思是：如果就多处理器的话make时并行编译

%install  #开始安装软件，如make install
rm -rf %{buildroot}
make INSTALL_ROOT=%{buildroot} install

rm -rf %{buildroot}/{.channels,.depdb,.depdblock,.filemap,.lock,.registry}
%{__install} -p -D -m 0755 sapi/fpm/init.d.php-fpm %{buildroot}/etc/init.d/php-fpm
%{__install} -p -D -m 0644 php.ini-production %{buildroot}/%{_prefix}/etc/php.ini

#rpm安装前执行的脚本
%pre
echo '/usr/local/lib' > /etc/ld.so.conf.d/local.conf
/sbin/ldconfig
if [ $1 == 1 -a -z "`grep ^%{_user} /etc/passwd`" ]; then    # $1有3个值，代表动作，安装类型，处理类型
    groupadd %{_group} -g 10000                              # 1：表示安装
    useradd -u 10000 -g 10000 -m %{_user}                    # 2：表示升级
fi                                                           # 0：表示卸载

#rpm安装后执行的脚本
%post
if [ $1 == 1 ];then
    [ -z "`grep ^'export PATH=' /etc/profile`" ] && echo "export PATH=%{_prefix}/bin:\$PATH" >> /etc/profile
    [ -n "`grep ^'export PATH=' /etc/profile`" -a -z "`grep '%{_prefix}' /etc/profile`" ] && sed -i "s@^export PATH=\(.*\)@export PATH=%{_prefix}/bin:\1@" /etc/profile
    /sbin/chkconfig --add php-fpm
    /sbin/chkconfig php-fpm on
    Mem=`free -m | awk '/Mem:/{print $2}'`  #下面主要是参数的优化
    if [ $Mem -le 640 ];then
        Mem_level=512M
        Memory_limit=64
    elif [ $Mem -gt 640 -a $Mem -le 1280 ];then
        Mem_level=1G
        Memory_limit=128
    elif [ $Mem -gt 1280 -a $Mem -le 2500 ];then
        Mem_level=2G
        Memory_limit=192
    elif [ $Mem -gt 2500 -a $Mem -le 3500 ];then
        Mem_level=3G
        Memory_limit=256
    elif [ $Mem -gt 3500 -a $Mem -le 4500 ];then
        Mem_level=4G
        Memory_limit=320
    elif [ $Mem -gt 4500 -a $Mem -le 8000 ];then
        Mem_level=6G
        Memory_limit=384
    elif [ $Mem -gt 8000 ];then
        Mem_level=8G
        Memory_limit=448
    fi
    sed -i "s@^memory_limit.*@memory_limit = ${Memory_limit}M@" %{_prefix}/etc/php.ini
    sed -i 's@^output_buffering =@output_buffering = On\noutput_buffering =@' %{_prefix}/etc/php.ini
    sed -i 's@^;cgi.fix_pathinfo.*@cgi.fix_pathinfo=0@' %{_prefix}/etc/php.ini
    sed -i 's@^short_open_tag = Off@short_open_tag = On@' %{_prefix}/etc/php.ini
    sed -i 's@^expose_php = On@expose_php = Off@' %{_prefix}/etc/php.ini
    sed -i 's@^request_order.*@request_order = "CGP"@' %{_prefix}/etc/php.ini
    sed -i 's@^;date.timezone.*@date.timezone = Asia/Shanghai@' %{_prefix}/etc/php.ini
    sed -i 's@^post_max_size.*@post_max_size = 50M@' %{_prefix}/etc/php.ini
    sed -i 's@^upload_max_filesize.*@upload_max_filesize = 50M@' %{_prefix}/etc/php.ini
    sed -i 's@^;upload_tmp_dir.*@upload_tmp_dir = /tmp@' %{_prefix}/etc/php.ini
    sed -i 's@^max_execution_time.*@max_execution_time = 5@' %{_prefix}/etc/php.ini
    sed -i 's@^disable_functions.*@disable_functions = chgrp,chown,chroot,dl,exec,fsocket,ini_alter,ini_restore,openlog,passthru,phpinfo,popen,popepassthru,proc_get_status,proc_open,readlink,shell_exec,stream_socket_server,symlink,syslog,system@' %{_prefix}/etc/php.ini
    sed -i 's@^session.cookie_httponly.*@session.cookie_httponly = 1@' %{_prefix}/etc/php.ini
    sed -i 's@^mysqlnd.collect_memory_statistics.*@mysqlnd.collect_memory_statistics = On@' %{_prefix}/etc/php.ini

    cat > %{_prefix}/etc/php-fpm.conf <<EOF
;;;;;;;;;;;;;;;;;;;;;
; FPM Configuration ;
;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;
; Global Options ;
;;;;;;;;;;;;;;;;;;
[global]
pid = run/php-fpm.pid
error_log = log/php-fpm.log
log_level = warning
emergency_restart_threshold = 30
emergency_restart_interval = 60s
process_control_timeout = 10s
daemonize = yes
;;;;;;;;;;;;;;;;;;;;
; Pool Definitions ;
;;;;;;;;;;;;;;;;;;;;
[%{_user}]
;listen = /dev/shm/php-cgi.sock
listen = 127.0.0.1:9000
listen.backlog = -1
;listen.allowed_clients = 127.0.0.1
listen.owner = %{_user}
listen.group = %{_group}
listen.mode = 0666
user = %{_user}
group = %{_group}

pm = dynamic
pm.max_children = 12
pm.start_servers = 8
pm.min_spare_servers = 6
pm.max_spare_servers = 12
pm.max_requests = 2048
pm.process_idle_timeout = 10s

request_terminate_timeout = 120
request_slowlog_timeout = 0
slowlog = log/slow.log
rlimit_files = 51200
rlimit_core = 0
catch_workers_output = yes
;env[HOSTNAME] = $HOSTNAME
env[PATH] = /usr/local/bin:/usr/bin:/bin
env[TMP] = /tmp
env[TMPDIR] = /tmp
env[TEMP] = /tmp
EOF
    if [ $Mem -le 3000 ];then
        sed -i "s@^pm.max_children.*@pm.max_children = $(($Mem/2/20))@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.start_servers.*@pm.start_servers = $(($Mem/2/30))@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.min_spare_servers.*@pm.min_spare_servers = $(($Mem/2/40))@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.max_spare_servers.*@pm.max_spare_servers = $(($Mem/2/20))@" %{_prefix}/etc/php-fpm.conf
    elif [ $Mem -gt 3000 -a $Mem -le 4500 ];then
        sed -i "s@^pm.max_children.*@pm.max_children = 80@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.start_servers.*@pm.start_servers = 50@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.min_spare_servers.*@pm.min_spare_servers = 40@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.max_spare_servers.*@pm.max_spare_servers = 80@" %{_prefix}/etc/php-fpm.conf
    elif [ $Mem -gt 4500 -a $Mem -le 6500 ];then
        sed -i "s@^pm.max_children.*@pm.max_children = 90@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.start_servers.*@pm.start_servers = 60@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.min_spare_servers.*@pm.min_spare_servers = 50@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.max_spare_servers.*@pm.max_spare_servers = 90@" %{_prefix}/etc/php-fpm.conf
    elif [ $Mem -gt 6500 -a $Mem -le 8500 ];then
        sed -i "s@^pm.max_children.*@pm.max_children = 100@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.start_servers.*@pm.start_servers = 70@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.min_spare_servers.*@pm.min_spare_servers = 60@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.max_spare_servers.*@pm.max_spare_servers = 100@" %{_prefix}/etc/php-fpm.conf
    elif [ $Mem -gt 8500 ];then
        sed -i "s@^pm.max_children.*@pm.max_children = 120@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.start_servers.*@pm.start_servers = 80@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.min_spare_servers.*@pm.min_spare_servers = 70@" %{_prefix}/etc/php-fpm.conf
        sed -i "s@^pm.max_spare_servers.*@pm.max_spare_servers = 120@" %{_prefix}/etc/php-fpm.conf
    fi
fi

#rpm卸载前执行的脚本
%preun
if [ $1 == 0 ];then
    /etc/init.d/php-fpm stop > /dev/null 2>&1
    /sbin/chkconfig --del php-fpm
    if [ -e '/etc/profile.d/custom_profile_new.sh' ];then
        sed -i 's@%{_prefix}/bin:@@' /etc/profile.d/custom_profile_new.sh
    else
        sed -i 's@%{_prefix}/bin:@@' /etc/profile
    fi
fi

#%postun rpm卸载后执行的脚本
%clean    #clean的主要作用就是删除BUILD
rm -rf %{buildroot}

%files  #指定哪些文件需要被打包，如/usr/local/php
%defattr(-,root,root,-)
%{_prefix}
%attr(0755,root,root) /etc/init.d/php-fpm

%changelog  #日志改变段， 这一段主要描述软件的开发记录
* Sat Oct 24 2015 yeho <lj2007331@gmail.com> 5.4.45-1
- Initial version
