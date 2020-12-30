## What is this?


Crypto is a simple plugin for the [gedit]( http://projects.gnome.org/gedit/ )
editor, allowing you to quickly encrypt/decrypt text documents with GPG.

Once installed and activated (through the "Preferences" window, "Plugin" tab),
it will add a submenu to the "Gear" menu, with two options allowing you to
encrypt or decrypt the currently open document.

Notice that to encrypt/decrypt, you should have already set up your key using
gpg or seahorse.

### How to install?


If you are a user of Debian (or any derivative such as Ubuntu or Mint),
the simplest way is to download and install the .deb package above.

Otherwise, to install for a single user, extract the archive and then:

```python
cd gedit-plugin-crypto-*
mkdir -p ~/.local/share/gedit/plugins/
ln -s `pwd`/crypto.plugin ~/.local/share/gedit/plugins/crypto.plugin
ln -s `pwd`/crypto ~/.local/share/gedit/plugins/crypto
```

To install systemwise (as root):

```python
cd gedit-plugin-crypto-*
ln -s `pwd`/crypto.plugin /usr/lib/gedit/plugins/crypto.plugin
ln -s `pwd`/crypto /usr/lib/gedit/plugins/crypto
mkdir /usr/share/gedit/plugins/crypto
ln -s `pwd`/crypto/crypto.glade /usr/share/gedit/plugins/crypto/crypto.glade
```

### Who should I blame if this sucks?

Pietro Battiston - <me@pietrobattiston.it>

### Technicalities

This plugin relies on the [Seahorse](https://projects.gnome.org/seahorse) dbus
service, which does the real work.

### Requirements

Gedit version 3 or later and the Seahorse daemon (package ``seahorse-daemon``
on debian-based systems) must be installed for the plugin to work.

In particular, current versions need gedit 3.12 or later; if you're using a
previous version of gedit,
[download version 0.3 of gedit-crypto](https://pietrobattiston.it/wiki/_media/gedit-crypto:gedit-plugin-crypto-0.3.tar.gz).

If your version of gedit is even older than 3.8, you need
[version 0.2 of gedit-crypto](https://pietrobattiston.it/wiki/_media/gedit-crypto:gedit-plugin-crypto-0.2.tar.gz).

### Code

You can browse/clone/fork the git repo at
https://github.com/toobaz/gedit_crypto . I'm willing to integrate
enhancements/bug fixes, so feel free to open PRs.
