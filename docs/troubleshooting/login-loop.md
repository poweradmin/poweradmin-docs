# Login Keeps Returning to the Login Page

You enter a correct username and password, the page reloads, and you are back at the login form, sometimes with "Invalid CSRF token". In almost every case the browser did not send the session cookie back, or PHP could not keep the session between two requests. The login form stores a token in the session, and when the session is empty on the next request the login is refused.

Work through the causes below in order.

## 1. The session cookie is marked Secure on a plain HTTP page

Poweradmin sets the `Secure` flag on its session cookie when the request looks like HTTPS: either PHP sees `$_SERVER['HTTPS']` set, or the request carries `X-Forwarded-Proto: https`. Browsers never send a `Secure` cookie over plain HTTP, so the session is lost on the next page.

Check this when:

- you open Poweradmin over `http://`, but the web server or PHP-FPM always passes `HTTPS=on` (a `fastcgi_param HTTPS on;` or similar copied from an HTTPS block);
- a reverse proxy sends `X-Forwarded-Proto: https` while users reach Poweradmin over HTTP.

Fix it by serving Poweradmin over HTTPS end to end (recommended), or by making sure `HTTPS` and `X-Forwarded-Proto` describe the connection the browser really uses.

In the browser's developer tools (Application or Storage tab), look at the `PHPSESSID` cookie: if it has the Secure flag and the address bar shows `http://`, this is the cause.

## 2. PHP cannot store the session

The session lives on the server, by default as a file in `session.save_path`. If the PHP process cannot write there, every request starts with an empty session.

- Find the path with `php -i | grep session.save_path` (for PHP-FPM, check the pool configuration, which can override it).
- Make sure the directory exists and is writable by the user the PHP-FPM pool or web server runs as.
- Look in the PHP or web server error log for `session_start(): Failed to read session data` or `Permission denied`.

## 3. Several Poweradmin instances without shared sessions

Behind a load balancer, the login request and the next request can land on different instances. With file-based sessions each instance only knows its own sessions. Enable sticky sessions on the load balancer, or point every instance at shared session storage (for example a common Redis or Memcached through PHP's `session.save_handler`).

## 4. The address changes between requests

Cookies belong to one host name. If the login form is served from one name (`poweradmin.example.com`) and the redirect after login goes to another (`www.poweradmin.example.com` or an IP address), the browser does not send the cookie.

- Use one canonical URL and redirect the others to it.
- When Poweradmin runs in a subdirectory, set `interface.base_url_prefix` (for example `/poweradmin`) so its links and redirects stay inside that path.

## 5. The session timeout is set to 0

`interface.session_timeout` is the idle time in seconds. `0` does not disable the timeout: it expires every session immediately, so each login is followed straight away by another login page. Use a large value instead, for example `86400` for one day. From 4.5.0 the configuration check refuses `0`; earlier releases accept it silently.

## Still stuck?

Enable PHP error logging as described in [Debugging](debugging.md), try the login once, and check the PHP error log and the browser's developer tools (Network tab: is a `Set-Cookie` header sent, and is the cookie sent back on the next request?). Include both when you open an issue.
