# Using Regex Search and Replace

Today I was presented with an issue that I needed to convert this piece of Python code:

```python
packages = ['autoconf',
            'automake',
            'a2ps',
            'cscope',
            'curl',
            'dkms',
            'emacs',
            'enscript',
            'glibc-doc',
            'gpg',
            'graphviz',
            'gthumb',
            'libreadline-dev',
            'manpages-posix',
            'manpages-posix-dev',
            'meld',
            'nfs-common',
            'openssh-client',
            'openssh-server',
            'seahorse',
            'synaptic',
            'vim',
            'vim-gtk3']
```

Into this list separated with commas for a control file for a Debian installer:

```
Depends: ansible, autoconf, automake, a2ps, cscope, curl, dkms, emacs, enscript, git, glibc-doc, gpg, graphviz, gthumb, libreadline-dev, manpages-posix, manpages-posix-dev, meld, nfs-common, openssh-client, openssh-server, python3, python3-pip, seahorse, synaptic, wget, vim, vim-gtk3
```

**NOTE:** there were some pre-existing dependencies that were there before but not included in this process.


Doing this by hand would be:

1. Terrible
2. Tedious

This is how I employed the power of `sed` regexes ([regular expressions](https://en.wikipedia.org/wiki/Regular_expression)) and [vim](https://www.vim.org/).

## Step One

Get the piece of text you are interested in.

For us, that is the code *inside* the brackets.

We can get that in one keystroke by using `vi[`; where each character is sequentially pressed.

Then you can press the `y` key to "yank" or copy the contents of the visual selection.

You can then open a temporary buffer using `:vnew` and switch over to the pane with `ctrl-h`.

Paste the contents of the register by simply pressing `p`.


## Step Two

Edit the text *programmatically*.

This can be done by using the search and replace function for vim.

Vim uses the `sed` regex engine, which can be learned about [here](https://www.gnu.org/software/sed/manual/html_node/Regular-Expressions.html).

For us, the regex is this:

```
%s/\v\'(.*)\'\,?\n/\1\,\ /g
```

This string has a multiple components:

1. `\,`: will match string literal comma (,)
2. `\'`: will match string literal single apostrophe (')
3. `?`: will match either if the character is present or not (in this case it's a newline)
4. `/\v\'(.*)\'\,?\n/`: will match an expression that looks like this 'hello world' and will mark the contents inside of the apostrophes as a group that can be transplanted somewhere else.
5. `/\1\,\ /g`: will replace the above match with this format: `hello world, ` and the `g` means that it applies to all matches

The result now looks like this:

```
autoconf, automake, a2ps, cscope, curl, dkms, emacs, enscript, glibc-doc, gpg, graphviz, gthumb, libreadline-dev, manpages-posix, manpages-posix-dev, meld, nfs-common, openssh-client, openssh-server, seahorse, synaptic, vim, vim-gtk3, 
```

Notice the trailing comma at the end, you can simply just remove it.
