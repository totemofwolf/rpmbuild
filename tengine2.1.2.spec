# This is a sample spec file for test rpm package
%define _prefix    /usr/local/nginx
%define _user      www
%define _user_uid  599
%define _group     www
%define _group_uid 599
%define _sbin_path      /usr/sbin

%define name      Tengine
%define summary   Tengine for Webserver
%define version   2.1.2
%define release   1
%define license   GPL
%define group     Application/WebServer
%define source    tengine-%{version}.tar.gz
%define url       http://tengine.taobao.org/
%define vendor    Taobao
%define packager  webuser

Name:           tengine
Version:        2.1.2
#Vendor:        Taobao
Release:        1
Summary:        GUN Tengine2.1.2

Group:          Application/WebServer
License:        GPL
URL:            http://tengine.taobao.org/
Source0:        %{name}-%{version}.tar.gz
Source1:        index.html
Source2:        nginx
Source3:        fastcgi_params
Source4:        nginx.conf

BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: openssl-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: jemalloc-devel
Requires: jemalloc


%description
The GNU Tengine WEB Server program.


%prep
%setup -q -n tengine-%{version}

%build
./configure \
  --prefix=/usr/local/nginx \
  --with-cc-opt='-O2 -fstack-protector --param=ssp-buffer-size=4 -Wformat -Werror=format-security -D_FORTIFY_SOURCE=2' \
  --with-ld-opt='-Wl,-Bsymbolic-functions -Wl,-z,relro' \
  --user=www \
  --group=www \
  --with-jemalloc \
  --with-http_stub_status_module \
  --with-http_ssl_module \
  --with-http_gzip_static_module \
  --with-http_concat_module \
  --with-http_realip_module \
  --with-http_v2_module \
  --with-http_sysguard_module \
  --with-syslog \
  --with-http_secure_link_module \
  --without-http-cache \
  --without-poll_module \
  --without-select_module \
  --without-mail_pop3_module \
  --without-mail_imap_module \
  --without-mail_smtp_module

#--with-openssl=/usr/local/src/sh-1.5.5/openssl-1.0.2j \
#--with-http_spdy_module replaced by httpv2

make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
#%{__install} -p -D %{SOURCE1} %{buildroot}/usr/local/nginx/html/index.html
#%{__install} -p -D -m 0755 %{SOURCE2} %{buildroot}/etc/rc.d/init.d/nginx
#%{__install} -p -D %{SOURCE3} %{buildroot}/usr/local/nginx/conf/fastcgi_params
#%{__install} -p -D %{SOURCE4} %{buildroot}/usr/local/nginx/conf/nginx.conf

mkdir -p %{buildroot}/%{_initrddir}
(
cat <<'EOF'
#!/bin/bash
# tengine Startup script for the tengine HTTP Server
# this script create it by Luo Hui at 2008.11.11.
# if you find any errors on this scripts,please contact Luo Hui.
# and send mail to farmer.luo at gmail dot com.
#
# chkconfig: - 85 15
# description: tengine is a high-performance web and proxy server.
# processname: tengine
# tengine pidfile: /var/run/tengine.pid
# tengine config: /usr/local/tengine/conf/nginx.conf


nginxd=%{_prefix}/sbin/nginx
nginx_config=%{_prefix}/conf/nginx.conf
nginx_pid=/var/run/tengine.pid

RETVAL=0
prog="nginx"

# Source function library.
. /etc/rc.d/init.d/functions

# Source networking configuration.
. /etc/sysconfig/network

# Check that networking is up.
[ ${NETWORKING} = "no" ] && exit 0

[ -x $nginxd ] || exit 0

ulimit -HSn 65535


# Start tengine daemons functions.
nginx_start() {

        if [ -e $nginx_pid ];then
                echo "tengine already running...."
                exit 1
        fi

        if [ ! -d %{_prefix}/logs ];then
                mkdir -p %{_prefix}/logs
        fi

        if [ ! -d %{_prefix}/tmp ]; then
                mkdir -p %{_prefix}/tmp
        fi

        if [ -e $nginx_pid ];then
                echo "tengine already running...."
                exit 1
        fi

        echo -n $"Starting $prog: "
        daemon $nginxd -c ${nginx_config}
        RETVAL=$?
        echo
        [ $RETVAL = 0 ] && touch /var/lock/subsys/tengine
        return $RETVAL

}


# Stop tengine daemons functions.
nginx_stop() {
        echo -n $"Stopping $prog: "
        killproc $nginxd
        RETVAL=$?
        echo
        [ $RETVAL = 0 ] && rm -f /var/lock/subsys/tengine $nginx_pid
}


# reload tengine service functions.
nginx_reload() {

        echo -n $"Reloading $prog: "
        #kill -HUP `cat ${nginx_pid}`
        killproc $nginxd -HUP
        RETVAL=$?
        echo

}

# See how we were called.
case "$1" in
start)
        nginx_start
        ;;

stop)
        nginx_stop
        ;;

reload)
        nginx_reload
        ;;

restart)
        nginx_stop
        nginx_start
        ;;

status)
        status $prog
        RETVAL=$?
        ;;
*)
        echo $"Usage: tengine {start|stop|restart|reload|status|help}"
        exit 1
esac

exit $RETVAL
EOF
) >%{buildroot}/%{_initrddir}/tengine

chmod 755 %{buildroot}/%{_initrddir}/tengine

%clean
rm -rf %{buildroot}

%pre
grep -q ^%{_group}: /etc/group || %{_sbin_path}/groupadd -g %{_group_gid} %{_group}
grep -q ^%{_user}: /etc/passwd || %{_sbin_path}/useradd -g %{_group} -u %{_user_uid} -d %{_prefix} -s /sbin/nologin -M %{_user}

%post
chkconfig --add tengine
chkconfig --level 345 tengine on


%preun
chkconfig --del tengine


#%postun
#if [ $1 = 0 ]; then
#        userdel %{_user} > /dev/null 2>&1 || true
#fi

%files
%defattr(-,root,root,-)
%dir %{_prefix}/
%attr(0755,%{_user},%{_group}) %dir %{_prefix}/logs
%dir %{_prefix}/modules
%dir %{_prefix}/sbin
%dir %{_prefix}/conf
%dir %{_prefix}/html
%{_prefix}/sbin/nginx
%{_prefix}/sbin/dso_tool
%{_prefix}/conf/module_stubs
%{_prefix}/conf/fastcgi.conf
%{_prefix}/conf/fastcgi_params.default
%{_prefix}/conf/win-utf
%{_prefix}/conf/koi-utf
%{_prefix}/conf/nginx.conf.default
%{_prefix}/conf/fastcgi.conf.default
%config(noreplace) %{_prefix}/conf/fastcgi_params
%{_prefix}/conf/koi-win
%{_prefix}/conf/mime.types
%config(noreplace) %{_prefix}/conf/nginx.conf
%{_prefix}/conf/mime.types.default
%{_prefix}/conf/scgi_params
%{_prefix}/conf/scgi_params.default
%{_prefix}/conf/uwsgi_params
%{_prefix}/conf/uwsgi_params.default
%{_prefix}/html/50x.html
%{_prefix}/html/index.html
/usr/lib64/perl5/perllocal.pod
/usr/local/lib64/perl5/auto/nginx/.packlist
/usr/local/lib64/perl5/auto/nginx/nginx.bs
/usr/local/lib64/perl5/auto/nginx/nginx.so
/usr/local/lib64/perl5/nginx.pm
%{_prefix}/conf/browsers
%{_prefix}/include/nginx.h
%{_prefix}/include/ngx_alloc.h
%{_prefix}/include/ngx_array.h
%{_prefix}/include/ngx_atomic.h
%{_prefix}/include/ngx_auto_config.h
%{_prefix}/include/ngx_auto_headers.h
%{_prefix}/include/ngx_buf.h
%{_prefix}/include/ngx_channel.h
%{_prefix}/include/ngx_conf_file.h
%{_prefix}/include/ngx_config.h
%{_prefix}/include/ngx_connection.h
%{_prefix}/include/ngx_core.h
%{_prefix}/include/ngx_crc.h
%{_prefix}/include/ngx_crc32.h
%{_prefix}/include/ngx_crypt.h
%{_prefix}/include/ngx_cycle.h
%{_prefix}/include/ngx_errno.h
%{_prefix}/include/ngx_event.h
%{_prefix}/include/ngx_event_busy_lock.h
%{_prefix}/include/ngx_event_connect.h
%{_prefix}/include/ngx_event_openssl.h
%{_prefix}/include/ngx_event_pipe.h
%{_prefix}/include/ngx_event_posted.h
%{_prefix}/include/ngx_event_timer.h
%{_prefix}/include/ngx_file.h
%{_prefix}/include/ngx_files.h
%{_prefix}/include/ngx_gcc_atomic_x86.h
%{_prefix}/include/ngx_hash.h
%{_prefix}/include/ngx_http.h
%{_prefix}/include/ngx_http_busy_lock.h
%{_prefix}/include/ngx_http_cache.h
%{_prefix}/include/ngx_http_config.h
%{_prefix}/include/ngx_http_core_module.h
%{_prefix}/include/ngx_http_perl_module.h
%{_prefix}/include/ngx_http_reqstat.h
%{_prefix}/include/ngx_http_request.h
%{_prefix}/include/ngx_http_script.h
%{_prefix}/include/ngx_http_spdy.h
%{_prefix}/include/ngx_http_spdy_module.h
%{_prefix}/include/ngx_http_ssi_filter_module.h
%{_prefix}/include/ngx_http_ssl_module.h
%{_prefix}/include/ngx_http_upstream.h
%{_prefix}/include/ngx_http_upstream_round_robin.h
%{_prefix}/include/ngx_http_v2.h
%{_prefix}/include/ngx_http_v2_module.h
%{_prefix}/include/ngx_http_variables.h
%{_prefix}/include/ngx_inet.h
%{_prefix}/include/ngx_linux.h
%{_prefix}/include/ngx_linux_config.h
%{_prefix}/include/ngx_list.h
%{_prefix}/include/ngx_log.h
%{_prefix}/include/ngx_md5.h
%{_prefix}/include/ngx_murmurhash.h
%{_prefix}/include/ngx_open_file_cache.h
%{_prefix}/include/ngx_os.h
%{_prefix}/include/ngx_palloc.h
%{_prefix}/include/ngx_parse.h
%{_prefix}/include/ngx_pipe.h
%{_prefix}/include/ngx_proc.h
%{_prefix}/include/ngx_process.h
%{_prefix}/include/ngx_process_cycle.h
%{_prefix}/include/ngx_proxy_protocol.h
%{_prefix}/include/ngx_queue.h
%{_prefix}/include/ngx_radix_tree.h
%{_prefix}/include/ngx_rbtree.h
%{_prefix}/include/ngx_regex.h
%{_prefix}/include/ngx_resolver.h
%{_prefix}/include/ngx_segment_tree.h
%{_prefix}/include/ngx_setaffinity.h
%{_prefix}/include/ngx_setproctitle.h
%{_prefix}/include/ngx_sha1.h
%{_prefix}/include/ngx_shmem.h
%{_prefix}/include/ngx_shmtx.h
%{_prefix}/include/ngx_slab.h
%{_prefix}/include/ngx_socket.h
%{_prefix}/include/ngx_string.h
%{_prefix}/include/ngx_sysinfo.h
%{_prefix}/include/ngx_syslog.h
%{_prefix}/include/ngx_thread.h
%{_prefix}/include/ngx_time.h
%{_prefix}/include/ngx_times.h
%{_prefix}/include/ngx_trie.h
%{_prefix}/include/ngx_user.h
/usr/local/share/man/man3/nginx.3pm
%{_initrddir}/tengine
%doc /usr/local/nginx/html/index.html
%attr(0775,root,root) /etc/rc.d/init.d/nginx

%changelog
* Mon Jul 4 2016 Beijing <schangech@gmail.com>
- ver 2.1.2
</schangech@gmail.com>
