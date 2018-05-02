#!/usr/bin/env elvish
initialized = $false
blocks = [&]

i3blocks -c /etc/i3blocks.conf | each [line]{
  if $initialized {
    for block (echo $line[1:] | from-json) {
      if (has-key $block label) {
	blocks[$block[label]] = $block[name]
      }
    }
  } else { initialized = $true }
} &

sxhkd | each [line]{
  notify-send $line $blocks[line]
}
