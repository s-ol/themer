set $mod Mod4

set $background {{ black }}
set $foreground {{ white }}
set $gray       {{ alt_black }}
set $primary    {{ primary }}
set $secondary  {{ secondary }}
set $tertiary   {{ tertiary }}
set $warning    {{ special }}

set $ws1  "1: web"
set $ws2  "2: music"
set $ws3  "3: irc"
set $ws4  "4: term"
set $ws5  "5: misc"
set $ws6  "6: 6"
set $ws7  "7: 7"
set $ws8  "8: 8"
set $ws9  "9: 9"
set $ws10 "10: 10"

font pango:DejaVu Sans Mono 8

exec_always feh --bg-scale ~/.wallpaper.png

floating_modifier $mod

bindsym $mod+Shift+q kill

bindsym $mod+Return exec i3-sensible-terminal
bindsym $mod+d exec dmenu_run -w 1000 -h 38 -x 183 -y 300 -nb "{{ black }}" -nf "{{ tertiary }}" -sb "{{ secondary }}" -sf "{{ black }}"

bindsym $mod+j focus left
bindsym $mod+k focus down
bindsym $mod+l focus up
bindsym $mod+odiaeresis focus right
bindsym $mod+Left focus left
bindsym $mod+Down focus down
bindsym $mod+Up focus up
bindsym $mod+Right focus right

bindsym $mod+Shift+j move left
bindsym $mod+Shift+k move down
bindsym $mod+Shift+l move up
bindsym $mod+Shift+odiaeresis move right
bindsym $mod+Shift+Left move left
bindsym $mod+Shift+Down move down
bindsym $mod+Shift+Up move up
bindsym $mod+Shift+Right move right

bindsym $mod+h split h
bindsym $mod+v split v

bindsym $mod+f fullscreen

bindsym $mod+s layout stacking
bindsym $mod+w layout tabbed
bindsym $mod+e layout toggle split

bindsym $mod+space focus mode_toggle
bindsym $mod+Shift+space floating toggle

bindsym $mod+a focus parent
#bindsym $mod+d focus child

bindsym $mod+1 workspace $ws1
bindsym $mod+2 workspace $ws2
bindsym $mod+3 workspace $ws3
bindsym $mod+4 workspace $ws4
bindsym $mod+5 workspace $ws5
bindsym $mod+6 workspace $ws6
bindsym $mod+7 workspace $ws7
bindsym $mod+8 workspace $ws8
bindsym $mod+9 workspace $ws9
bindsym $mod+0 workspace $ws10
bindsym $mod+Tab workspace back_and_forth

workspace_auto_back_and_forth yes

bindsym $mod+Control+Shift+Left move window to workspace prev
bindsym $mod+Control+Shift+Right move window to workspace next

bindsym $mod+Control+Shift+Prior move container to output left
bindsym $mod+Control+Shift+Next move container to output right

bindsym $mod+Shift+1 move container to workspace number $ws1
bindsym $mod+Shift+2 move container to workspace number $ws2
bindsym $mod+Shift+3 move container to workspace number $ws3
bindsym $mod+Shift+4 move container to workspace number $ws4
bindsym $mod+Shift+5 move container to workspace number $ws5
bindsym $mod+Shift+6 move container to workspace number $ws6
bindsym $mod+Shift+7 move container to workspace number $ws7
bindsym $mod+Shift+8 move container to workspace number $ws8
bindsym $mod+Shift+9 move container to workspace number $ws9
bindsym $mod+Shift+0 move container to workspace number $ws10


# colors                BORDER      BACKGROUND TEXT        INDICATOR
client.focused          $primary    $primary   $background $primary
client.focused_inactive $background $primary   $foreground $background
client.unfocused        $gray       $gray      $background $secondary
client.urgent           $warning    $warning   $foreground $warning

# Start i3bar to display a workspace bar (plus the system information i3status
# finds out, if available)
bar {
    status_command    i3status
    position          bottom
    workspace_buttons yes
    
    font {{ font }}
 
    colors {
        background $background
        statusline $primary
        
        # Colors go <border> <background> <text> <indicator>
        focused_workspace $secondary $background $foreground
        active_workspace $primary $background $foreground
        inactive_workspace $primary $background $foreground
        urgent_workspace $foreground $warning
    }
}


for_window [window_role="pop-up"] floating enable
for_window [window_role="task_dialog"] floating enable
for_window [instance="float"] floating enable

bindsym $mod+Shift+c reload
bindsym $mod+Shift+r restart
bindsym $mod+Shift+e exec "i3-nagbar -t warning -m 'You pressed the exit shortcut. Do you really want to exit i3? This will end your X session.' -b 'Yes, exit i3' 'i3-msg exit'"

mode "resize" {
        bindsym j resize shrink width 10 px or 10 ppt
        bindsym k resize grow height 10 px or 10 ppt
        bindsym l resize shrink height 10 px or 10 ppt
        bindsym odiaeresis resize grow width 10 px or 10 ppt

        bindsym Left resize shrink width 10 px or 10 ppt
        bindsym Down resize grow height 10 px or 10 ppt
        bindsym Up resize shrink height 10 px or 10 ppt
        bindsym Right resize grow width 10 px or 10 ppt

        bindsym Return mode "default"
        bindsym Escape mode "default"
}

bindsym $mod+r mode "resize"

bindsym $mod+shift+minus move scratchpad
bindsym $mod+minus scratchpad show
