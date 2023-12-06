# Documentation of fun fact development

## Bash execution behavior

Commonly, bash process execute command in foreground mode in default.
However, in rare case, the bash execute command in background instead.
One reproducible is when the bash IO is redirected to pipe instead of TTY device.
Example:

```
bash -c "<COMMAD>" 2>&1 | cat
```

In this case, **[COMMAND]** is executed as background process but not foreground.
It is interesting to consider this case
because some program behave differently between background and foreground mode.
For instance, container runtime **runc** is hang in background mode
but not in foreground.
